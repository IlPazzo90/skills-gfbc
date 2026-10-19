"""Mail helper for the purchasing office (Microsoft Graph, app credentials).

Reads the mailboxes listed in CASELLE; sends only from MITTENTE.
Configuration: ~/.config/ufficio-acquisti/graph.env (or the file named by
UFFICIO_ACQUISTI_ENV), one KEY=value per line:

  GRAPH_TENANT, GRAPH_CLIENT, GRAPH_SECRET   app registration with Mail.Read/Mail.Send
  DOMINIO      = azienda.it
  MITTENTE     = acquisti            (local part, the only mailbox that sends)
  CASELLE      = acquisti,noreply    (default mailboxes for nuove/cerca)
  MAGAZZINO    = magazzino           (optional: always in cc on outgoing mail)
  FIRMA        = ~/.config/ufficio-acquisti/firma.html   (optional HTML signature)

  posta.py nuove [--dal 2026-10-06] [--caselle acquisti,noreply]
  posta.py cerca "123 - Richiesta offerta" [--casella acquisti]
  posta.py leggi <casella> <id>            # body without quoted history, attachment list
  posta.py allegati <casella> <id> <dir>   # download attachments into <dir>
  posta.py invia --a x@y.it [--a ...] --oggetto "..." --corpo file.html [--cc ...] [--senza-magazzino] [--allega f.pdf]
  posta.py inoltra <casella> <id> --a x@y.it --corpo nota.html
"""
import argparse, base64, datetime as dt, html, json, os, re, sys, urllib.parse, urllib.request

FIRMA_MARK = "<!--firma-ua-->"


def _env():
    p = os.path.expanduser(os.environ.get("UFFICIO_ACQUISTI_ENV", "~/.config/ufficio-acquisti/graph.env"))
    if not os.path.exists(p):
        raise SystemExit(f"manca la configurazione {p}: vedi l'intestazione di questo file")
    e = {}
    for line in open(p):
        if "=" in line and not line.lstrip().startswith("#"):
            k, v = line.strip().split("=", 1)
            e[k.strip()] = v.strip()
    return e


CFG = _env()
DOM = "@" + CFG["DOMINIO"]
MITTENTE = CFG.get("MITTENTE", "acquisti") + DOM
MAGAZZINO = CFG["MAGAZZINO"] + DOM if CFG.get("MAGAZZINO") else ""
CASELLE = CFG.get("CASELLE", CFG.get("MITTENTE", "acquisti"))
_firma = os.path.expanduser(CFG.get("FIRMA", ""))
# Every outgoing mail carries the company signature, forwards included.
FIRMA = FIRMA_MARK + (open(_firma).read() if _firma and os.path.exists(_firma) else "")


def _token():
    e = CFG
    data = urllib.parse.urlencode({"client_id": e["GRAPH_CLIENT"], "client_secret": e["GRAPH_SECRET"],
                                   "scope": "https://graph.microsoft.com/.default",
                                   "grant_type": "client_credentials"}).encode()
    url = f"https://login.microsoftonline.com/{e['GRAPH_TENANT']}/oauth2/v2.0/token"
    return json.load(urllib.request.urlopen(url, data))["access_token"]


TK = None


def call(path, body=None, method=None):
    global TK
    TK = TK or _token()
    url = (path if path.startswith("http") else "https://graph.microsoft.com/v1.0" + path).replace(" ", "%20")
    req = urllib.request.Request(url, data=json.dumps(body).encode() if body is not None else None,
                                 headers={"Authorization": "Bearer " + TK, "Content-Type": "application/json",
                                          "ConsistencyLevel": "eventual"},
                                 method=method or ("POST" if body is not None else "GET"))
    with urllib.request.urlopen(req) as r:
        raw = r.read()
        return json.loads(raw) if raw else {"status": r.status}


def box(name):
    return name if "@" in name else name + DOM


def testo(msg):
    b = msg["body"]["content"]
    if msg["body"]["contentType"] == "html":
        b = re.sub(r"(?is)<(style|script|head).*?</\1>", "", b)
        b = re.sub(r"(?i)<br\s*/?>|</p>|</div>|</li>", "\n", b)
        b = html.unescape(re.sub(r"<[^>]+>", "", b))
    b = re.sub(r"\n\s*\n+", "\n", b).strip()
    return re.split(r"\n(?:Da:|From:|-----Messaggio originale|Il giorno .{5,80} ha scritto|Il \d\d/\d\d/\d{4}.{0,60}ha scritto)", b)[0]


def impianto(subject):
    m = re.search(r"(?<![\d/])(\d{1,4})\s*(?:\+\s*\d{1,4}\s*)?[-:]\s*(?:richiesta|ordine|conferma|reso|ddt)", subject, re.I)
    if m:
        return m.group(1)
    m = re.search(r"\bIMP\.?\s*(\d{1,4})\b", subject, re.I)
    return m.group(1) if m else ""


def riga(m, nome=""):
    frm = m.get("from", {}).get("emailAddress", {}).get("address", "-")
    att = " 📎" if m.get("hasAttachments") else ""
    imp = impianto(m["subject"])
    return f"{m['receivedDateTime'][:16]} {nome:9} {frm:38} imp={imp or '-':5} {m['subject'][:90]}{att}  id={m['id']}"


SEL = "$select=id,subject,from,receivedDateTime,hasAttachments,conversationId"


def nuove(a):
    dal = a.dal or (dt.date.today() - dt.timedelta(days=1)).isoformat()
    for c in a.caselle.split(","):
        url = f"/users/{box(c)}/mailFolders/inbox/messages?$filter=receivedDateTime ge {dal}T00:00:00Z&$orderby=receivedDateTime&$top=100&{SEL}"
        while url:
            r = call(url)
            for m in r["value"]:
                print(riga(m, c))
            url = r.get("@odata.nextLink")


def cerca(a):
    for c in a.casella.split(","):
        r = call(f"/users/{box(c)}/messages?$search=%22{urllib.parse.quote(a.testo)}%22&$top=50&{SEL}")
        for m in sorted(r["value"], key=lambda m: m["receivedDateTime"]):
            print(riga(m, c))


def leggi(a):
    m = call(f"/users/{box(a.casella)}/messages/{a.id}?$select=subject,from,toRecipients,ccRecipients,receivedDateTime,body,hasAttachments")
    to = ", ".join(x["emailAddress"]["address"] for x in m["toRecipients"] + m["ccRecipients"])
    print(f"{m['receivedDateTime']} {m['from']['emailAddress']['address']} -> {to}\n{m['subject']}\n\n{testo(m)}")
    if m["hasAttachments"]:
        for x in call(f"/users/{box(a.casella)}/messages/{a.id}/attachments?$select=name,size,contentType")["value"]:
            print(f"📎 {x['name']} ({x['size']} B, {x['contentType']})")


def allegati(a):
    os.makedirs(a.dir, exist_ok=True)
    for x in call(f"/users/{box(a.casella)}/messages/{a.id}/attachments")["value"]:
        if "contentBytes" in x:
            p = os.path.join(a.dir, os.path.basename(x["name"]))
            open(p, "wb").write(base64.b64decode(x["contentBytes"]))
            print(p)


def html_corpo(corpo):
    # Plain text sent as HTML collapses into one block: keep line breaks.
    if not re.search(r"<(p|br|div|table|ul|ol)\b", corpo, re.I):
        corpo = "".join(f"<p>{html.escape(b).replace(chr(10), '<br>')}</p>" for b in corpo.strip().split("\n\n"))
    return corpo


def con_firma(corpo):
    return corpo if FIRMA_MARK in corpo else corpo + FIRMA


def inoltra(a):
    corpo = con_firma(html_corpo(open(a.corpo).read()))
    cc = list(a.cc or [])
    path = f"/users/{MITTENTE}/messages/{a.id}" if box(a.casella) == MITTENTE else None
    if not path:
        raise SystemExit("inoltra: solo messaggi della casella mittente (Graph inoltra dalla casella che li contiene)")
    d = call(f"{path}/createForward", {})
    old = call(f"/users/{MITTENTE}/messages/{d['id']}?$select=body")["body"]["content"]
    call(f"/users/{MITTENTE}/messages/{d['id']}", {
        "body": {"contentType": "HTML", "content": corpo + "<hr>" + old},
        "toRecipients": [{"emailAddress": {"address": x}} for x in a.a],
        "ccRecipients": [{"emailAddress": {"address": x}} for x in cc]}, method="PATCH")
    call(f"/users/{MITTENTE}/messages/{d['id']}/send", {})
    print("inoltrata | a:", ", ".join(a.a), "| cc:", ", ".join(cc) or "-")


def invia(a):
    corpo = con_firma(html_corpo(open(a.corpo).read()))
    cc = list(a.cc or [])
    if MAGAZZINO and not a.senza_magazzino and MAGAZZINO not in cc:
        cc.append(MAGAZZINO)
    msg = {"subject": a.oggetto, "body": {"contentType": "HTML", "content": corpo},
           "toRecipients": [{"emailAddress": {"address": x}} for x in a.a],
           "ccRecipients": [{"emailAddress": {"address": x}} for x in cc]}
    if a.allega:
        msg["attachments"] = [{"@odata.type": "#microsoft.graph.fileAttachment", "name": os.path.basename(f),
                               "contentBytes": base64.b64encode(open(f, "rb").read()).decode()} for f in a.allega]
    r = call(f"/users/{MITTENTE}/sendMail", {"message": msg, "saveToSentItems": True})
    print("inviata", r.get("status", r), "| a:", ", ".join(a.a), "| cc:", ", ".join(cc) or "-", "|", a.oggetto)


def main():
    p = argparse.ArgumentParser()
    s = p.add_subparsers(dest="cmd", required=True)
    x = s.add_parser("nuove"); x.add_argument("--dal"); x.add_argument("--caselle", default=CASELLE); x.set_defaults(f=nuove)
    x = s.add_parser("cerca"); x.add_argument("testo"); x.add_argument("--casella", default=CASELLE); x.set_defaults(f=cerca)
    x = s.add_parser("leggi"); x.add_argument("casella"); x.add_argument("id"); x.set_defaults(f=leggi)
    x = s.add_parser("allegati"); x.add_argument("casella"); x.add_argument("id"); x.add_argument("dir"); x.set_defaults(f=allegati)
    x = s.add_parser("invia"); x.add_argument("--a", action="append", required=True); x.add_argument("--oggetto", required=True)
    x.add_argument("--corpo", required=True); x.add_argument("--cc", action="append"); x.add_argument("--senza-magazzino", action="store_true")
    x.add_argument("--allega", action="append"); x.set_defaults(f=invia)
    x = s.add_parser("inoltra"); x.add_argument("casella"); x.add_argument("id"); x.add_argument("--a", action="append", required=True)
    x.add_argument("--corpo", required=True); x.add_argument("--cc", action="append"); x.set_defaults(f=inoltra)
    a = p.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()
