# Guida Pratica a Claude Code CLI

> **Versione 4.30 — maggio 2026** — verificata su Claude Code v2.1.123
> Licenza [Creative Commons BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

> ← [12. Subagent](12-subagent.md) | [Index](README.md) | [14. Plugin](14-plugin.md) →

---

## 13. Hook: automatizzare il lifecycle di Claude Code

I **Hook** sono il terzo meccanismo di estensione di Claude Code, e quello che opera al livello più basso. Mentre Subagent e Skill influenzano *cosa* il main agent fa, gli Hook intercettano *quando* succedono certi eventi — l'avvio di una sessione, il momento prima di eseguire un tool, la fine di una risposta — e possono validare, modificare, bloccare, registrare quegli eventi prima o dopo che accadano.

Sono lo strumento giusto quando l'estensione non è "fagli sapere come si lavora" (Skill) o "delega questo task" (Subagent), ma "intervieni automaticamente in questo punto preciso del flusso, senza che io debba ricordarmi di chiederlo".

### 13.1 Cosa sono e a cosa servono

Un Hook è uno script — bash, HTTP, prompt verso un altro modello, subagent, o tool MCP — configurato per scattare a un determinato evento del ciclo di vita di Claude Code. Lo script riceve in input un payload JSON che descrive l'evento (es. quale tool sta per essere eseguito, con quali argomenti) e produce un output che può:

- **bloccare** l'azione (es. impedire `rm -rf` su una cartella protetta)
- **validare** e lasciar passare (es. controllare che ogni edit di un file `.php` rispetti regole di style)
- **registrare** in un log strutturato (audit trail di tutte le modifiche)
- **iniettare contesto** automatico (es. ricordare a Claude le convenzioni del progetto a ogni session start)

A prima vista somigliano a un linter o a un git hook, ma con una differenza importante: il linter agisce *dopo* che il codice è stato scritto da te, gli Hook agiscono *durante* l'esecuzione di Claude Code, prima che le sue azioni diventino effettive. È un livello di automazione interno, non un controllo esterno.

> Una buona regola: se la cosa che vuoi fare è "ogni volta che Claude X, devi Y", probabilmente è un Hook. Se è "Claude deve sapere che il progetto usa X", è una Skill o un `CLAUDE.md`. Se è "delega questo lavoro specifico a un altro agent", è un Subagent.

### 13.2 Anatomia di un hook

Gli Hook si configurano nel file `settings.json` insieme a permissions e altre direttive (vedi [sezione 9.2](#configurare-i-permessi-in-settings.json) per il setup base e per la riga `$schema` che abilita autocomplete e validazione anche dei blocchi `hooks`). La sintassi base è la stessa per tutti gli eventi:

```json
{
  "hooks": {
    "<EventName>": [
      {
        "matcher": "<pattern>",
        "hooks": [
          {
            "type": "command",
            "command": "<percorso-script>"
          }
        ]
      }
    ]
  }
}
```

I file di configurazione vivono in tre livelli (più due location di scope ridotto):

- **`~/.claude/settings.json`** — utente, valido su tutte le macchine. Personale, non condivisibile.
- **`.claude/settings.json`** del progetto — committato in Git, condiviso col team.
- **`.claude/settings.local.json`** del progetto — gitignored di default. Per Hook specifici della tua copia locale.
- **Frontmatter di Skill o Agent** (campo `hooks`) — Hook che girano solo quando quella Skill/Agent è attiva.
- **`hooks/hooks.json`** dei plugin installati — Hook che vengono con un plugin.

Esistono **cinque tipi di Hook**, scelti tramite il campo `type`:

| **Tipo** | **Quando usarlo** | **Esempio di scenario** |
|---|---|---|
| `command` (default) | Logica deterministica, accesso file, parsing JSON | Bloccare un comando, scrivere un log, lanciare uno script |
| `http` | Audit centralizzato, integrazione cloud (introdotto Feb 2026) | POST a un endpoint aziendale per log immutabili |
| `prompt` | Decisione "sì/no" che richiede capacità di giudizio LLM | "Tutti i task del prompt sono completati prima di terminare?" |
| `agent` | Verifica complessa che richiede tool e ricerca codebase | Un subagent che lancia la test suite prima dello Stop |
| `mcp_tool` | Integrazione con un server MCP già configurato | Salvare il contesto in una memoria MCP esterna |

Per il 90% dei casi pratici si usa `command`. Gli altri tipi sono per scenari avanzati o quando la decisione richiede capacità che un semplice script non ha.

### 13.3 Eventi del lifecycle

Claude Code espone più di venti eventi intercettabili, raggruppabili in sette categorie. Tabella sintetica degli eventi più usati nella pratica:

| **Categoria** | **Evento** | **Quando si attiva** | **Può bloccare?** |
|---|---|---|---|
| Sessione | `SessionStart` | Avvio o ripresa sessione | No — può iniettare contesto |
| Sessione | `SessionEnd` | Termine sessione | No — solo cleanup |
| Sessione | `UserPromptSubmit` | Utente invia un prompt | Sì — può modificare/bloccare il prompt |
| Sessione | `Stop` | Claude finisce una risposta | Sì — può forzare a continuare |
| Tool | `PreToolUse` | Prima dell'esecuzione di un tool | Sì — può negare/modificare l'input |
| Tool | `PostToolUse` | Dopo l'esecuzione di un tool | No — l'azione è già fatta |
| Tool | `PostToolUseFailure` | Dopo un tool fallito | No |
| Permessi | `PermissionRequest` | Mostra dialog permessi | Sì — può decidere allow/deny/ask |
| Subagent | `SubagentStart` | Spawn di un subagent | No |
| Subagent | `SubagentStop` | Subagent termina | Sì — può forzare un retry |
| Compaction | `PreCompact` | Prima di `/compact` | No — può salvare backup |
| Compaction | `PostCompact` | Dopo `/compact` | No — può re-iniettare contesto |
| File | `FileChanged` | File watchato modificato | No |

Esistono altri eventi più specialistici (`UserPromptExpansion`, `ConfigChange`, `CwdChanged`, `WorktreeCreate/Remove`, `Notification`, `Elicitation`, e gli eventi di Agent Teams come `TaskCreated`, `TaskCompleted`, `TeammateIdle`). Per la lista completa la fonte canonica è [code.claude.com/docs/en/hooks](https://code.claude.com/docs/en/hooks).

I due eventi che userai più spesso sono `PreToolUse` e `PostToolUse`. Tutto il pattern "guardiano dei tool" si costruisce su di loro.

### 13.4 Matcher e ispezione (`/hooks`)

Il campo `matcher` filtra **quali invocazioni** dell'evento devono attivare l'Hook. Quattro pattern supportati:

- **Wildcard** `"*"` o stringa vuota — match su tutti
- **Exact** `"Bash"` — solo invocazioni del tool `Bash`
- **Pipe** `"Edit|Write"` — alternazione, match su `Edit` oppure `Write`
- **Regex** `"mcp__.*"` — sintassi regex standard, qui per matchare tutti i tool MCP

Il significato del matcher dipende dall'evento: per `PreToolUse`/`PostToolUse` è il nome del tool; per `SessionStart` è la fonte (`startup`, `resume`, `clear`, `compact`); per `SubagentStart`/`SubagentStop` è il nome dell'agent. Senza matcher (o con `"*"`), l'Hook scatta sempre.

Dalla v2.1.85+ esiste anche il campo `if` per filtri secondari sugli **argomenti** del tool, non solo sul nome:

```json
{
  "matcher": "Bash",
  "hooks": [
    {
      "type": "command",
      "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/validate-git.sh",
      "if": "Bash(git *)"
    }
  ]
}
```

Questo Hook scatta solo per `git ...` e ignora gli altri comandi Bash — utile per restringere ulteriormente.

**Comando `/hooks`.** Una volta scritto un Hook è facile chiedersi se la configurazione è stata effettivamente caricata. `/hooks` apre un browser interattivo (read-only) della configurazione attiva: per ogni evento mostra quanti Hook sono registrati, da quale file di settings provengono, con quale matcher. Non permette di **editare** o **disabilitare** Hook al volo: per quello devi modificare il `settings.json` e attendere che venga ricaricato (o riavviare la sessione). Il flusso tipico di sviluppo è: edit `settings.json` → `/hooks` per verifica del caricamento → invocare un tool target per testare il comportamento.

### 13.5 Input e output

Un Hook di tipo `command` riceve via **stdin** un oggetto JSON che descrive l'evento. Campi comuni a tutti gli eventi:

```json
{
  "session_id": "abc123",
  "cwd": "/home/user/wp-plugins/access-control",
  "hook_event_name": "PreToolUse",
  "transcript_path": "/home/user/.claude/projects/.../transcript.jsonl"
}
```

Per `PreToolUse` si aggiungono `tool_name` e `tool_input`:

```json
{
  "session_id": "abc123",
  "hook_event_name": "PreToolUse",
  "tool_name": "Bash",
  "tool_input": { "command": "rm -rf wp-content/uploads" }
}
```

Il **comportamento di output** è governato da:

- **Exit code dello script**:
  - `0` — successo. Se stdout è JSON valido, viene interpretato come output strutturato; se è plain text, viene aggiunto al contesto come `additionalContext`.
  - `2` — **blocco**: l'azione non procede. stderr viene mostrato a Claude come motivo del blocco.
  - Altri valori — errore non-bloccante, l'azione procede ma viene registrato in transcript.

- **JSON output strutturato** (su stdout, exit 0):

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "rm -rf su wp-content è vietato",
    "updatedInput": { "command": "echo 'comando bloccato'" },
    "additionalContext": "Per cancellare upload usa lo script di backup."
  }
}
```

Campi più usati:

- **`permissionDecision`** (PreToolUse): `allow` / `deny` / `ask` / `defer`
- **`decision`** (PostToolUse, Stop): `allow` / `block`
- **`additionalContext`**: testo iniettato a Claude come system reminder
- **`updatedInput`**: modifica dell'input del tool prima dell'esecuzione (es. forzare flag sicuri)
- **`continue`** / **`stopReason`**: controllo del flusso negli eventi `Stop`

**Più Hook sullo stesso evento? "Most restrictive wins".** Se due Hook su `PreToolUse` ritornano uno `allow` e l'altro `deny`, vince `deny`. Tutti gli `additionalContext` vengono concatenati. Se due Hook impostano `updatedInput`, l'ordine non è garantito: evita configurazioni in cui due Hook diversi modificano lo stesso input.

### 13.6 Esempi pratici

Quattro esempi in ambito WordPress, dal più semplice al più articolato. Per ognuno: scenario, configurazione, script, comportamento osservato.

#### Esempio A — Bloccare `rm -rf` in `wp-content/`

**Scenario.** Stai lavorando a un plugin e vuoi una rete di sicurezza che impedisca a Claude di lanciare `rm -rf` su qualunque path che contenga `wp-content/`. Una svista in un comando shell potrebbe distruggere upload, cache o backup di un sito di produzione.

**`.claude/settings.json`:**

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/block-rm-wpcontent.sh"
          }
        ]
      }
    ]
  }
}
```

**`.claude/hooks/block-rm-wpcontent.sh`:**

```bash
#!/bin/bash
INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // ""')

if echo "$COMMAND" | grep -qE 'rm\s+(-[a-z]*r[a-z]*\s+|-r\s+).*wp-content'; then
  echo "Bloccato: rm ricorsivo su wp-content vietato dal hook" >&2
  exit 2
fi
exit 0
```

**Comportamento.** Quando Claude prova a lanciare `rm -rf wp-content/uploads`, l'Hook intercetta, rileva il pattern e ritorna exit 2 con un messaggio in stderr. Claude vede il blocco, riceve la motivazione, e decide come procedere (chiedendoti conferma o cambiando approccio). Comandi `rm` su altri path passano normalmente.

#### Esempio B — Audit log JSON Lines su Edit/Write

**Scenario.** Vuoi un audit trail di tutte le modifiche fatte da Claude ai file PHP del plugin, in formato JSON Lines per analisi successiva (grep, jq, dashboard).

**`.claude/settings.json`:**

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/audit-php.sh"
          }
        ]
      }
    ]
  }
}
```

**`.claude/hooks/audit-php.sh`:**

```bash
#!/bin/bash
INPUT=$(cat)
FILE=$(echo "$INPUT" | jq -r '.tool_input.file_path // ""')

if [[ "$FILE" == *.php ]]; then
  jq -nc --arg ts "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
         --arg session "$(echo "$INPUT" | jq -r '.session_id')" \
         --arg tool   "$(echo "$INPUT" | jq -r '.tool_name')" \
         --arg file   "$FILE" \
    '{ts: $ts, session: $session, tool: $tool, file: $file}' \
    >> "$CLAUDE_PROJECT_DIR/.claude/audit/php-edits.jsonl"
fi
exit 0
```

**Comportamento.** Ogni edit o write su un file `.php` aggiunge una riga al file `audit/php-edits.jsonl`. Le altre modifiche (CSS, MD, JSON) sono ignorate. Il log è strutturato e leggibile con `jq -s '.[] | select(.file | contains("admin"))' audit/php-edits.jsonl` per filtrare a posteriori.

#### Esempio C — `phpcs` con WordPress-Extra automatico, async

**Scenario.** Ogni file PHP modificato da Claude deve essere passato a `phpcs` con lo standard `WordPress-Extra`. Vuoi che il lint giri **in background** senza bloccare Claude (l'async è disponibile da gennaio 2026).

**`.claude/settings.json`:**

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/phpcs-wp.sh",
            "async": true
          }
        ]
      }
    ]
  }
}
```

**`.claude/hooks/phpcs-wp.sh`:**

```bash
#!/bin/bash
INPUT=$(cat)
FILE=$(echo "$INPUT" | jq -r '.tool_input.file_path // ""')

if [[ "$FILE" == *.php ]] && command -v phpcs >/dev/null; then
  phpcs --standard=WordPress-Extra "$FILE" \
        > "$CLAUDE_PROJECT_DIR/.claude/lint/$(basename "$FILE").log" 2>&1 || true
fi
exit 0
```

**Comportamento.** `phpcs` gira in background dopo ogni edit, scrivendo il report in `.claude/lint/`. Claude non aspetta il completamento (è async, le decision fields verrebbero comunque ignorate). Tu rivedi i log a fine sessione o con un watcher in IDE. Per il blocco hard del commit usa un pre-commit hook Git separato — gli Hook di Claude Code non sostituiscono i Git hook, lavorano a un livello diverso.

#### Esempio D — Reminder convenzioni a `SessionStart`

**Scenario.** Ogni volta che apri Claude Code dentro il plugin, vuoi che il main agent riceva un reminder delle convenzioni del progetto (oltre a quanto già scritto in `CLAUDE.md`).

**`.claude/settings.json`:**

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/wp-session-reminder.sh"
          }
        ]
      }
    ]
  }
}
```

**`.claude/hooks/wp-session-reminder.sh`:**

```bash
#!/bin/bash
cat <<'REMINDER'
Reminder per questa sessione:
- Tutti gli hook PHP devono verificare nonce e capability.
- Output sempre escapato (esc_html, esc_attr, wp_kses_post).
- Query SQL solo via $wpdb->prepare().
- Stile codice: PSR-12 + WordPress-Extra dove le due divergono, vince WordPress.
REMINDER
exit 0
```

**Comportamento.** All'avvio della sessione (matcher `startup`, non su `resume`), il main agent riceve il reminder come `additionalContext`. È complementare a `CLAUDE.md`: il file Markdown copre le regole stabili, l'Hook può iniettare reminder dinamici (es. costruire il messaggio leggendo lo stato del plugin, la branch corrente, o eventi recenti).

#### Esempio E — Backup transcript prima di `/compact`

**Scenario.** `/compact` è lossy: il sommario conserva decisioni e contesto chiave, ma butta via i dettagli. In una sessione con molte decisioni architetturali o un debug complesso, perdere il dettaglio può costare ore. Un hook `PreCompact` salva il transcript prima che la compaction avvenga.

**`.claude/settings.json`:**

```json
{
  "hooks": {
    "PreCompact": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/backup-transcript.sh"
          }
        ]
      }
    ]
  }
}
```

**`.claude/hooks/backup-transcript.sh`:**

```bash
#!/bin/bash
INPUT=$(cat)
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // "unknown"')
TRANSCRIPT_DIR="${HOME}/.claude/transcripts"
mkdir -p "$TRANSCRIPT_DIR"
# Salva il contenuto grezzo del payload in un file datato per sessione
echo "$INPUT" \
  > "$TRANSCRIPT_DIR/${SESSION_ID}_$(date +%Y%m%d-%H%M%S).json" 2>/dev/null || true
exit 0
```

**Comportamento.** Ogni volta che viene invocato `/compact` (o si raggiunge l'auto-compact), lo script salva il payload della sessione in `~/.claude/transcripts/` con session ID e timestamp. Lo script non blocca la compaction (exit 0): la sua unica funzione è il salvataggio laterale. I file restano disponibili per lettura manuale successiva.

#### Esempio F — Troncamento output verbosi da Bash

**Scenario.** Comandi come `find`, `npm install`, `composer update` e build verbosi producono decine di migliaia di token di output che entrano tutti nel contesto come tool result. Un hook `PostToolUse` su `Bash` può troncarli prima che il modello li veda, preservando testa e coda — dove di solito stanno l'informazione rilevante.

**`.claude/settings.json`:**

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/truncate-output.sh"
          }
        ]
      }
    ]
  }
}
```

**`.claude/hooks/truncate-output.sh`:**

```bash
#!/bin/bash
INPUT=$(cat)
OUTPUT=$(echo "$INPUT" | jq -r '.tool_result.output // ""')
LINE_COUNT=$(echo "$OUTPUT" | wc -l)
MAX_LINES=150

if [ "$LINE_COUNT" -gt "$MAX_LINES" ]; then
  HEAD=$(echo "$OUTPUT" | head -n 50)
  TAIL=$(echo "$OUTPUT" | tail -n 50)
  OMITTED=$(( LINE_COUNT - 100 ))
  TRUNCATED="${HEAD}

[... ${OMITTED} righe omesse — output totale: ${LINE_COUNT} righe ...]

${TAIL}"
  echo "$INPUT" | jq --arg out "$TRUNCATED" '.tool_result.output = $out'
else
  echo "$INPUT"
fi
exit 0
```

**Comportamento.** Se l'output del comando supera 150 righe, lo script conserva le prime 50 e le ultime 50, inserendo un marcatore con il conteggio delle righe omesse. L'output modificato viene restituito al modello al posto di quello originale. Per output sotto soglia, lo script lo lascia passare intatto.

> **Attenzione.** Questo hook modifica l'output prima che il modello lo veda. Se il task richiede il conteggio preciso di righe o la presenza di un pattern in una parte centrale dell'output, l'hook può nascondere informazioni rilevanti. Valuta se attivarlo a livello di progetto o solo per sessioni specifiche.

### 13.7 Sicurezza

Gli Hook sono potenti perché eseguono **codice arbitrario** con i tuoi permessi utente. Non c'è sandbox: uno script Hook può leggere `.env`, fare richieste di rete, lasciare tracce sul filesystem. Questa potenza è la stessa che li rende un vettore di attacco se non gestiti con attenzione.

**CVE-2025-59536 (RCE via hook injection).** A inizio 2026 è stato documentato un caso di Remote Code Execution sfruttando il fatto che `.claude/settings.json` viene caricato automaticamente dalla root del progetto. Un repository malevolo può registrare un Hook che esegue script arbitrario al primo avvio di Claude Code in quella directory. Lo trovi tracciato come [CVE-2025-59536 su Check Point Research](https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/).

**Cinque regole pratiche di sicurezza.**

1. **Code review obbligatoria su `.claude/settings.json`.** Trattalo come uno script eseguibile, non come un file di configurazione passivo. Cambiamenti a quel file richiedono revisione esattamente come una modifica al `Makefile` del progetto.
2. **Repository non fidati: clona, ispeziona, poi apri Claude Code.** Non lanciare `claude` dentro un repo appena clonato senza aver aperto `.claude/settings.json` e `.claude/hooks/` per controllare cosa contengono.
3. **HTTP hooks: whitelist esplicita di env var.** Il campo `allowedEnvVars` definisce quali variabili d'ambiente possono essere interpolate negli header. Non whitelistare segreti che non servono all'endpoint specifico.
4. **Sanitizza l'input prima di iniettarlo come `additionalContext`.** Il payload di un Hook contiene `tool_input` proveniente dalla sessione. Se passi quel testo crudo a Claude come contesto, apri la porta a prompt injection (un `tool_input` malevolo iniettato a sua volta da un file letto da Claude).
5. **Disabilitazione globale per debug.** Il flag `"disableAllHooks": true` nel `settings.json` spegne tutti gli Hook. Utile in fase di debug quando sospetti che un Hook stia interferendo, o se hai dubbi sulla provenienza di una configurazione caricata.

> Hook configurati a livello **utente** (`~/.claude/settings.json`) sono sotto il tuo controllo e ti seguono ovunque. Hook configurati a livello **progetto** (`.claude/settings.json`) sono sotto il controllo di chiunque possa committare nel repo. Tieni questa distinzione presente quando ricevi una pull request che tocca quel file.

### 13.8 Gotchas e quando NON usarli

I Hook hanno un certo numero di trappole comuni. Le sei più frequenti:

- **Path relativi negli script.** L'Hook gira con un cwd non garantito. Usa sempre `$CLAUDE_PROJECT_DIR` o path assoluti, mai path relativi tipo `./scripts/check.sh`.
- **JSON parsing con regex.** Il payload è JSON: usa `jq` o un parser vero. Tentare di estrarre campi con `grep`/`sed` produce script fragili che si rompono al primo carattere speciale.
- **Stop hook in loop.** Se un Hook su `Stop` ritorna `continue: true`, Claude continua e alla fine triggera di nuovo `Stop`, che triggera di nuovo l'Hook... loop infinito. Il payload contiene `stop_hook_active: true` quando sei nella ri-esecuzione: leggi quel flag e esci subito se è `true`.
- **`async: true` non blocca.** Gli Hook asincroni sono utili solo per side-effect (logging, lint, notifiche). Se ritornano `decision: "block"` o `permissionDecision: "deny"`, quei campi vengono **ignorati**. Per bloccare devi essere sincrono.
- **`PostToolUse` non può undo.** L'evento si chiama "Post" perché il tool è già stato eseguito. Puoi loggare, formattare, mandare notifiche, ma non puoi annullare l'azione. Per bloccare serve `PreToolUse`.
- **Output dei profili shell che inquina lo stdout.** Se il tuo `~/.bashrc` o `~/.zshrc` stampa qualcosa anche in modalità non-interattiva, quel testo finisce davanti al JSON di output dell'Hook e fa fallire il parser. Avvolgi gli `echo` di profilo in `if [[ $- == *i* ]]; then ... fi`.

**Quando NON usare un Hook.**

- **Logica complessa che richiede ragionamento LLM**. Un Hook di tipo `command` è uno script deterministico. Se la decisione richiede capacità di giudizio ("questo edit è una buona idea?"), serve un subagent dedicato (vedi [sezione 12](#subagent-orchestrare-lavoro-specializzato)) o un Hook di tipo `prompt`.
- **Stile e formattazione post-edit**. Per applicare uno style guide a tutti i file modificati, un linter normale (Prettier, phpcs, eslint) lanciato da pre-commit o IDE è quasi sempre più trasparente e debuggabile di un Hook PostToolUse.
- **Workflow esplorativi una-tantum**. L'overhead di scrivere uno script + configurarlo + testare il matcher + verificare con `/hooks` non è giustificato se il workflow lo userai una volta sola.

In dubbio: **Hook per comportamenti automatici e ripetuti che vuoi siano invisibili e infallibili**. Per tutto il resto, esistono strumenti più adeguati.

---


---

> ← [12. Subagent](12-subagent.md) | [Index](README.md) | [14. Plugin](14-plugin.md) →
