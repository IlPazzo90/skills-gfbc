# Brief — primo avvio e prontezza all'installazione (skills-gfbc)

Repository pubblico `IlPazzo90/skills-gfbc`: due skill per Claude Code/Codex su Unicò 3 (Futura SI), `unico3-gfbc` e `ufficio-acquisti-gfbc`, già ripulite dai dati dell'azienda d'origine (verifica precedente chiusa).

Richiesta del proprietario: «fai un nuovo passaggio per verificare che sia tutto pronto. all'installazione il nuovo utente dovrebbe fare il punto sulla sua organizzazione per imparare le cose della sua organizzazione.»

## Requisiti

1. **Primo avvio.** Un nuovo utente, alla prima sessione, viene guidato a fare il punto sulla propria organizzazione; la skill impara la configurazione della sua azienda (aziende Unicò e quali sono di prova, ruoli, catena CRM, tabelle di configurazione, fornitori, regola prezzi, autonomie concesse) e la scrive in file locali.
2. **Dati dell'azienda fuori dal repository**: i file imparati non devono finire nel repo pubblico né essere sovrascritti da `git pull`.
3. **Sicurezza invariata**: il primo avvio non scrive su Unicò; non allarga da solo sandbox o permessi (UNICO3_SANDBOX / UNICO3_AUTORIZZATE li decide una persona); credenziali mai in chat né nei file della skill; ordini ai fornitori sempre con ok del titolare.
4. **Pronto per l'installazione da terzi**: README seguibile alla lettera da clone pulito; nessun riferimento a file assenti; test verdi; `posta.py` con errori puliti; nessun dato residuo dell'azienda d'origine nei file nuovi o modificati.
5. Coerenza: i due SKILL.md, i primo-avvio, i modelli e gli altri references non si contraddicono su dove stanno i dati e su cosa la skill può fare da sola. Le skill funzionano sia in Claude Code sia in Codex.

## Artefatto

`git diff HEAD` più i file nuovi non tracciati (`git status --short`), nella radice del repo:
README.md, CHANGELOG.md, unico3-gfbc/SKILL.md, unico3-gfbc/references/{primo-avvio,apprendimento}.md, unico3-gfbc/modelli/organizzazione.md, ufficio-acquisti-gfbc/SKILL.md, ufficio-acquisti-gfbc/.gitignore, ufficio-acquisti-gfbc/references/{primo-avvio,ciclo,scrivere-ai-fornitori,strumenti}.md, ufficio-acquisti-gfbc/modelli/{fornitori,prezzi,ricorrenti,aperti,autonomie}.md (i primi quattro spostati da references/), ufficio-acquisti-gfbc/scripts/posta.py.
Il resto del repo è contesto (guardrail in unico3-gfbc/u3/guardrail.py, tabelle-rotte.md per i nomi delle rotte).
