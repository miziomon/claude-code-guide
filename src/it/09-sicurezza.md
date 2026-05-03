# Guida Pratica a Claude Code CLI

> **Versione 4.23 — maggio 2026** — verificata su Claude Code v2.1.123
> Licenza [Creative Commons BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

> ← [8. Gestione del contesto](08-contesto.md) | [Index](README.md) | [10. Skill](10-skill.md) →

---

## 9. Sicurezza e gestione dei permessi

Claude Code è un agente **autonomo** che esegue comandi nel tuo sistema. Senza le giuste precauzioni, è un vettore di rischio reale.

### 9.1 Il sistema dei permessi

Di default, Claude chiede conferma prima di eseguire qualsiasi operazione di modifica (scrittura file, comandi shell, chiamate MCP che modificano stato). Le operazioni di lettura sono auto-approvate:

- `Read`, `Glob`, `Grep`, `WebSearch`, `LSP` → nessuna conferma
- `Edit`, `Write`, `Bash`, MCP di scrittura → conferma richiesta

### 9.2 Configurare i permessi in `settings.json`

Puoi definire regole granulari nel file `.claude/settings.json` del progetto:

```json
{
  "permissions": {
    "allow": [
      "Bash(npm run test:*)",
      "Bash(npm run lint:*)",
      "Bash(git status)",
      "Bash(git diff)",
      "Read(**)"
    ],
    "deny": [
      "Read(.env*)",
      "Read(**/secrets/**)",
      "Read(**/.aws/credentials)",
      "Bash(rm -rf *)",
      "Bash(sudo *)",
      "Bash(curl * | bash)",
      "Bash(wget * | sh)"
    ]
  }
}
```

**Spiegazione passo passo:**

1. `allow` — operazioni che Claude può eseguire **senza chiedere conferma**
2. `deny` — operazioni **bloccate fisicamente**, anche se Claude ci prova non succede nulla
3. I pattern usano glob (`**` per qualsiasi percorso, `*` per segmento singolo)
4. `deny` ha **precedenza** su `allow`

#### Validare il file con lo schema JSON ufficiale

Anthropic pubblica uno schema JSON per `settings.json` ospitato su SchemaStore. Aggiungendo la riga `$schema` come prima chiave, editor JSON Schema-aware (VS Code, Cursor, JetBrains, Vim con coc-json, ecc.) ti danno autocomplete delle proprietà ammesse, validazione inline dei valori e tooltip con la descrizione di ogni campo:

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "permissions": {
    "allow": ["Bash(npm run test:*)"],
    "deny":  ["Read(.env*)"]
  }
}
```

La docs ufficiale ([code.claude.com/docs/en/settings](https://code.claude.com/docs/en/settings)) avverte che lo schema è aggiornato periodicamente: un warning di validazione su una proprietà appena introdotta in una release recente non significa necessariamente che la configurazione sia invalida. Lo stesso schema copre anche le altre sezioni di `settings.json`, inclusi `hooks` (vedi [sezione 13 — Hook](#hook-automatizzare-il-lifecycle-di-claude-code)), `env`, `model`, `availableModels`.

### 9.3 Proteggere i segreti

Nonostante `.claudeignore`, ci sono scenari in cui Claude potrebbe leggere file sensibili (prompt injection, errori di configurazione). Usa **sempre** `permissions.deny` per file `.env`, credenziali, chiavi private.

### 9.4 Modalità pericolose

**`--dangerously-skip-permissions`** salta tutte le conferme. È utile per:
- Esecuzione autonoma in ambienti sandbox/Docker
- Task lunghi dove non vuoi essere interrotto ogni 30 secondi

Il nome è esplicito: **non è un flag da usare alla leggera**. Linee guida:

- **Mai** su macchine che contengono credenziali produzione
- **Mai** con accesso a repository aziendali sensibili
- **Solo** in container isolati o VM dedicate allo scopo

Per un'automazione del blocco a livello di lifecycle (es. impedire `rm -rf` su path protetti anche dentro `--dangerously-skip-permissions`), gli Hook offrono uno strato programmatico aggiuntivo: vedi [sezione 13](#hook-automatizzare-il-lifecycle-di-claude-code).

### 9.5 Prompt injection

Un attaccante potrebbe inserire istruzioni malevole in:

- Commenti di codice che Claude legge
- File README scaricati da dipendenze
- Risposte di servizi MCP non fidati
- Nomi di file manipolati

**Difese pratiche:**

1. Usa sempre Plan Mode per task su codice di terze parti
2. Rivedi sempre il piano prima di approvarlo
3. Non eseguire Claude Code con privilegi di amministratore
4. Isola i progetti esterni in directory separate con `settings.json` restrittivi

---


---

> ← [8. Gestione del contesto](08-contesto.md) | [Index](README.md) | [10. Skill](10-skill.md) →
