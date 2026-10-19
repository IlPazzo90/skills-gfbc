#!/usr/bin/env python3
"""Fase 0: walk Unico with the user already logged in and dump what exists.

Read-only. Never clicks anything, never writes to a field, never submits
anything. Every probe below is a querySelectorAll or a property read.
Produces a JSON dump plus a screenshot under ricognizione/, from which the
UI map is written by hand.

Usage:
    python3 scripts/ricognizione.py            # attach and dump
    python3 scripts/ricognizione.py --avvia    # open Chrome first, then wait for login
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from u3 import chrome, sessione  # noqa: E402

URL_APP = "https://start.dc3.unico3.cloud/"
FRAMMENTO = "unico3.cloud"
USCITA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "ricognizione")

AVVISO_AZIENDA = (
    "STIMA INAFFIDABILE: costruita passando l'intero testo visibile della "
    "pagina a sessione.azienda_da_testo, non l'etichetta isolata "
    "dell'azienda attiva (il selettore giusto va ancora trovato durante "
    "questa ricognizione, vedi docstring in u3/sessione.py). Un menu che "
    "elenca le aziende puo' far scattare un falso positivo. Confermare "
    "sempre guardando lo screenshot prima di fidarsi di questo campo."
)

# Read-only probes. Each JS expression only reads the DOM: querySelectorAll,
# innerText, getAttribute, className, .value/.type/.name read (never set),
# .length. Nothing here clicks, assigns .value, or calls submit().
#
# "scalare"  -> value is used as-is, no truncation possible.
# "testo"    -> {totale_caratteri, testo} so a silent cut is detectable.
# "elenco"   -> {totale, elementi} so a silent cut is detectable.
SONDE = {
    "url": ("scalare", "location.href"),
    "titolo": ("scalare", "document.title"),
    "testo_visibile": (
        "testo",
        "(function(){"
        "var t=document.body.innerText.replace(/[\\uD800-\\uDFFF]/g,'');"
        "return {totale_caratteri:t.length, testo:t.slice(0,20000)};"
        "})()",
    ),
    "link": (
        "elenco",
        "(function(){"
        "var a=Array.from(document.querySelectorAll('a[href]'));"
        "var tot=a.length;"
        "var mostrati=a.slice(0,400).map(function(x){"
        "return {testo:(x.innerText||'').trim().slice(0,120), href:x.href};"
        "});"
        "return {totale:tot, elementi:mostrati};"
        "})()",
    ),
    "pulsanti": (
        "elenco",
        "(function(){"
        "var b=Array.from(document.querySelectorAll(\"button,[role='button'],input[type='button'],input[type='submit']\"));"
        "var tot=b.length;"
        "var mostrati=b.slice(0,400).map(function(x){"
        "return {testo:(x.innerText||x.value||'').trim().slice(0,120),"
        "titolo:(x.getAttribute('title')||''), classe:(x.className||'').slice(0,160)};"
        "});"
        "return {totale:tot, elementi:mostrati};"
        "})()",
    ),
    "campi": (
        "elenco",
        "(function(){"
        "var c=Array.from(document.querySelectorAll('input,select,textarea'));"
        "var tot=c.length;"
        "var mostrati=c.slice(0,400).map(function(x){"
        "return {nome:x.name||'', id:x.id||'', tipo:x.type||x.tagName,"
        "etichetta:(x.getAttribute('aria-label')||x.getAttribute('placeholder')||''),"
        "obbligatorio:!!x.required};"
        "});"
        "return {totale:tot, elementi:mostrati};"
        "})()",
    ),
    "tabelle": (
        "elenco",
        "(function(){"
        "var t=Array.from(document.querySelectorAll(\"table,[role='grid'],[role='table']\"));"
        "var tot=t.length;"
        "var mostrati=t.slice(0,20).map(function(tab){"
        "var intestazioni=Array.from(tab.querySelectorAll(\"th,[role='columnheader']\"));"
        "return {"
        "intestazioni: intestazioni.slice(0,60).map(function(h){return (h.innerText||'').trim();}),"
        "intestazioni_totale: intestazioni.length,"
        "righe: tab.querySelectorAll(\"tr,[role='row']\").length"
        "};"
        "});"
        "return {totale:tot, elementi:mostrati};"
        "})()",
    ),
    "iframe": (
        "elenco",
        "(function(){"
        "var f=Array.from(document.querySelectorAll('iframe'));"
        "var tot=f.length;"
        "var mostrati=f.slice(0,20).map(function(x){return x.src;});"
        "return {totale:tot, elementi:mostrati};"
        "})()",
    ),
}


def schermata(scheda: chrome.Scheda, nome: str) -> str:
    """Save a PNG of the current tab. Returns the path."""
    # Page.enable is idempotent, and captureScreenshot needs the Page domain
    # on. main() already enables it, but schermata() should not depend on
    # that — make it work standalone too.
    scheda._invia("Page.enable")
    risposta = scheda._invia("Page.captureScreenshot", {"format": "png"})
    dati = risposta.get("result", {}).get("data")
    if not dati:
        return ""
    os.makedirs(USCITA, exist_ok=True)
    percorso = os.path.join(USCITA, f"{nome}.png")
    with open(percorso, "wb") as file_png:
        file_png.write(base64.b64decode(dati))
    return percorso


def sonda(scheda: chrome.Scheda) -> dict:
    """Run every read-only probe against whatever is on screen.

    Returns the collected data plus a "troncamenti" map: for any probe that
    was cut off (more items/chars existed than were kept), it records how
    many there really were vs. how many made it into the dump, so a silent
    truncation is visible instead of just missing.
    """
    raccolto: dict = {}
    troncamenti: dict = {}
    for nome, (tipo, espressione) in SONDE.items():
        try:
            valore = scheda.valuta(espressione)
        except RuntimeError as errore:
            raccolto[nome] = f"ERRORE: {errore}"
            continue

        if tipo == "scalare":
            raccolto[nome] = valore
        elif tipo == "testo":
            valore = valore or {}
            testo = valore.get("testo", "") or ""
            totale = valore.get("totale_caratteri", len(testo))
            raccolto[nome] = testo
            if totale > len(testo):
                troncamenti[nome] = {
                    "totale": totale,
                    "mostrati": len(testo),
                    "unita": "caratteri",
                }
        elif tipo == "elenco":
            valore = valore or {}
            elementi = valore.get("elementi", []) or []
            totale = valore.get("totale", len(elementi))
            raccolto[nome] = elementi
            if totale > len(elementi):
                troncamenti[nome] = {
                    "totale": totale,
                    "mostrati": len(elementi),
                    "unita": "elementi",
                }

    raccolto["troncamenti"] = troncamenti
    return raccolto


def main() -> int:
    parser = argparse.ArgumentParser(description="Ricognizione Unico 3")
    parser.add_argument("--avvia", action="store_true", help="apri Chrome prima di agganciarti")
    parser.add_argument("--etichetta", default="corrente", help="nome del dump")
    parser.add_argument("--timeout", type=int, default=600, help="secondi di attesa del login")
    # La 9222 e' la porta di debug piu' usata, quindi capita che altri strumenti
    # l'abbiano gia' presa: quando due Chrome la chiedono, solo il primo la ottiene
    # e il flag del secondo resta inerte. Poterla cambiare evita di agganciarsi
    # al browser sbagliato.
    parser.add_argument(
        "--porta",
        type=int,
        default=chrome.PORTA_PREDEFINITA,
        help=f"porta di debug di Chrome (default {chrome.PORTA_PREDEFINITA})",
    )
    parser.add_argument(
        "--profilo",
        default=chrome.PROFILO_PREDEFINITO,
        help=f"profilo Chrome dedicato (default {chrome.PROFILO_PREDEFINITO})",
    )
    argomenti = parser.parse_args()

    if argomenti.avvia:
        chrome.avvia(URL_APP, profilo=argomenti.profilo, porta=argomenti.porta)
        print(f"Chrome aperto sulla porta {argomenti.porta}, profilo {argomenti.profilo}.")
        print("Fai il login sull'azienda di prova, poi torna qui.")

    target = chrome.attendi_target(
        FRAMMENTO, porta=argomenti.porta, timeout=argomenti.timeout
    )
    scheda = chrome.Scheda(target["webSocketDebuggerUrl"])
    try:
        scheda._invia("Page.enable")
        indirizzo = scheda.url()
        if not sessione.login_effettuato(indirizzo):
            print(f"Sei ancora sulla pagina di login ({indirizzo}). Fai il login e rilancia.")
            return 1

        raccolto = sonda(scheda)
        raccolto["azienda_indovinata_dal_testo"] = sessione.azienda_da_testo(
            raccolto.get("testo_visibile") or ""
        )
        raccolto["azienda_avviso"] = AVVISO_AZIENDA
        raccolto["schermata"] = schermata(scheda, argomenti.etichetta)

        os.makedirs(USCITA, exist_ok=True)
        percorso = os.path.join(USCITA, f"{argomenti.etichetta}.json")
        with open(percorso, "w", encoding="utf-8") as file_json:
            json.dump(raccolto, file_json, ensure_ascii=False, indent=2)

        print(f"Dump scritto in {percorso}")
        print(f"URL: {raccolto['url']}")
        print(
            "Azienda indovinata dal testo (DA CONFERMARE A VISTA, vedi "
            f"azienda_avviso nel dump): {raccolto['azienda_indovinata_dal_testo']}"
        )
        print(f"Link trovati: {len(raccolto.get('link') or [])}")
        print(f"Tabelle trovate: {len(raccolto.get('tabelle') or [])}")
        if raccolto["troncamenti"]:
            print(f"ATTENZIONE - dati troncati nel dump: {list(raccolto['troncamenti'].keys())}")
        return 0
    finally:
        scheda.chiudi()


if __name__ == "__main__":
    raise SystemExit(main())
