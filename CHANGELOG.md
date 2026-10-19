# Changelog

## 2026-10-19

- Prima versione pubblica di `unico3-gfbc` e `ufficio-acquisti-gfbc`, ricavate dalle skill interne e ripulite dai dati dell'azienda d'origine (persone, clienti, fornitori, prezzi, codici, infrastruttura).
- `unico3-gfbc`: aziende sandbox e permessi permanenti da variabili d'ambiente (`UNICO3_SANDBOX`, `UNICO3_AUTORIZZATE`), vuote di default; profilo Chrome in `~/.unico3-profile`.
- `ufficio-acquisti-gfbc`: `posta.py` configurabile (dominio, caselle, firma) da `~/.config/ufficio-acquisti/graph.env`; fornitori, prezzi, ricorrenti e pratiche aperte come modelli da compilare.
- `unico3-gfbc`: `elimina_documento` ed `elimina_intervento` classificate irreversibili (vietate in produzione); helper di pagina non distribuiti dichiarati come tali.
- Verifiche: 156 test verdi, `u3.fatti` senza divergenze, gitleaks pulito; sei round di revisione adversariale cross-model (Codex), 25 finding tutti corretti, esito «verificato con riserve». Il verbale cita i dati rimossi e resta privato, fuori dal repository.
