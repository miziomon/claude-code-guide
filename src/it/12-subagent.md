# Guida Pratica a Claude Code CLI

> **Versione 4.23 — maggio 2026** — verificata su Claude Code v2.1.123
> Licenza [Creative Commons BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

> ← [11. MCP](11-mcp.md) | [Index](README.md) | [13. Hook](13-hook.md) →

---

## 12. Subagent: orchestrare lavoro specializzato

I **subagent** sono uno dei meccanismi più potenti di Claude Code, e anche uno dei meno compresi. Non sono "agent secondari" che fanno cose minori: sono istanze di Claude con **proprio contesto, propri tool, propria personalità di prompt**, che la sessione principale può invocare per delegare lavoro specializzato. Un capitolo intero serve a inquadrarli bene perché cambiano il modo in cui imposti i workflow complessi.

### 12.1 Cosa sono e perché ti servono

L'analogia più utile è quella delle **schede del browser**. Quando lavori a un task complesso, il main agent è come una scheda principale che si riempie di tab figli (file letti, output di tool, ricerche): più va avanti, più la scheda si appesantisce. I subagent sono **schede separate**: hanno il loro contesto, fanno il loro lavoro, e quando finiscono passano alla scheda principale solo il risultato — non tutto quello che hanno letto per arrivarci.

Risolvono in pratica tre problemi distinti:

1. **Contesto saturo**. Una ricerca che richiede di leggere 50 file per trovare un pattern, fatta dal main agent, lascia 50 file nel contesto. Fatta da un subagent, lascia solo il sommario finale. Vedi anche la [sezione 8](#gestione-del-contesto) sulla gestione del contesto.
2. **Specializzazione**. Un main agent generalista può fare una code review, ma un subagent con un system prompt mirato a "code reviewer specializzato in sicurezza WordPress" lo fa meglio, con criteri stabili tra una sessione e l'altra.
3. **Delega multipla**. Su un task articolato — *"rivedi questa PR su sicurezza, performance e stile"* — puoi delegare i tre angoli di analisi a tre subagent diversi e ricevere tre summary indipendenti, invece di tenere tutto nella stessa scheda.

### 12.2 Subagent vs main agent: la differenza concreta

Tecnicamente, un subagent differisce dal main agent in quattro dimensioni:

- **Context window separato**: parte da zero, vede solo il prompt che la sessione principale gli passa.
- **Tool restrictions**: puoi limitargli i tool disponibili (es. solo `Read`, `Grep`, `Glob` per un agent in sola lettura).
- **System prompt dedicato**: ha la sua "personalità" istruzionale, indipendente da quella della sessione principale.
- **Model override**: può girare su un modello diverso (es. Haiku per velocità su task massivi mentre la sessione principale resta su Sonnet).

Il subagent non è invocabile direttamente da te: lo invoca Claude tramite il tool `Agent` (rinominato da `Task` in v2.1.63 — l'alias `Task(...)` è ancora attivo per retrocompatibilità). Tu chiedi al main agent un risultato, e il main agent decide se delegare a un subagent in base alla `description` di quest'ultimo.

### 12.3 I subagent built-in

Claude Code include alcuni subagent disponibili out-of-the-box. I tre rilevanti per l'uso quotidiano sono:

- **Explore** — gira su Haiku, è read-only (`Glob`, `Read`, `Grep`, `Bash`). Il main agent lo invoca per ricerche nel codebase quando una query richiede di leggere molti file. Accetta un livello di approfondimento: `quick` (lookup mirato), `medium` (esplorazione moderata), `very thorough` (ricerca esaustiva su più convenzioni di nome).
- **Plan** — usato in Plan Mode (vedi [sezione 5](#plan-mode-pensare-prima-di-scrivere)). Eredita il modello della sessione, è read-only, esiste perché in Plan Mode anche le ricerche devono restare nel perimetro non distruttivo.
- **general-purpose** — l'agent generalista per task multi-step quando non hai un agent specializzato. Eredita il modello e ha accesso a tutti i tool. È quello che il main agent invoca quando dici *"delega questa cosa a un subagent"* senza specificare quale.

Esistono altri due agent built-in di uso più interno: `statusline-setup` (configura la status line, attivato da `/statusline`) e `Claude Code Guide` (gira su Haiku, risponde a domande sulla CLI stessa). Li nomino solo per completezza.

### 12.4 Creare un subagent custom

Hai due strade per creare un subagent: **interattiva** col comando `/agents`, oppure **manuale** scrivendo il file.

**Via `/agents`.** Apre un'interfaccia tabbed: "Running" elenca gli agent attivi nella sessione, "Library" mostra quelli disponibili con la possibilità di crearne di nuovi. Il flusso di creazione ti chiede scope (Personal / Project), descrizione dell'agent, tool ammessi, modello, colore di display, memoria. Claude può anche **generare la prima bozza del system prompt** a partire dalla tua descrizione — utile come scaffolding, da rifinire a mano.

**Via file.** Un subagent è un file Markdown con frontmatter YAML. Il path determina lo scope:

- **Progetto**: `.claude/agents/<nome>.md` — committato nel repo, condiviso col team.
- **Utente**: `~/.claude/agents/<nome>.md` — personale, ti accompagna su tutti i progetti della macchina.

Esempio concreto in ambito WordPress, un subagent dedicato all'audit di sicurezza dei plugin:

```markdown
---
name: wp-security-auditor
description: |
  Use this agent to audit WordPress plugin code for security issues.
  Triggers on: PHP files in wp-content/plugins, mentions of nonce,
  capability checks, sanitize_*, esc_*, $wpdb queries, REST API
  endpoints, AJAX handlers.
tools: Read, Grep, Glob
model: sonnet
color: red
---

Sei un auditor di sicurezza specializzato in plugin WordPress.

Per ogni file PHP che analizzi, verifica nell'ordine:

1. **Nonce verification** su ogni handler che modifica stato
   (form submit, AJAX action, REST endpoint).
2. **Capability check** (`current_user_can()`) prima di azioni
   privilegiate.
3. **Sanitizzazione input**: tutti i `$_GET`, `$_POST`, `$_REQUEST`
   passati attraverso `sanitize_text_field`, `sanitize_email`,
   `absint`, ecc., a seconda del tipo atteso.
4. **Escaping output**: ogni stringa stampata deve passare per
   `esc_html`, `esc_attr`, `esc_url`, `wp_kses_post` a seconda
   del contesto.
5. **Query SQL**: usare sempre `$wpdb->prepare()` per query con
   variabili. Mai concatenazione diretta.
6. **File operations**: validare path, evitare path traversal.

Riferimenti normativi:

- Plugin Security Handbook: https://developer.wordpress.org/plugins/security/
- WordPress Coding Standards: https://developer.wordpress.org/coding-standards/

Output strutturato per ogni file:

- File e riga
- Severity: critical / high / medium / low
- Vulnerabilità identificata
- Fix consigliato con esempio di codice corretto

Non modificare codice. Limitati al report.
```

I tool sono limitati a `Read`, `Grep`, `Glob`: l'agent **non può** modificare file, lanciare comandi shell, accedere alla rete. È un revisore in sola lettura, per design — esattamente quello che vuoi da un audit di sicurezza.

I campi più rilevanti del frontmatter:

| Campo | Tipo | Funzione |
|---|---|---|
| `name` | string (required) | ID univoco, lowercase con trattini, max 64 caratteri |
| `description` | string (required) | Quando il main agent deve delegare a questo subagent |
| `tools` | lista | Allowlist di tool ammessi (default: eredita tutto) |
| `disallowedTools` | lista | Denylist di tool vietati (applicata prima di `tools`) |
| `model` | string | `haiku`, `sonnet`, `opus`, `inherit` o ID completo |
| `permissionMode` | string | `default`, `acceptEdits`, `auto`, `plan`, `bypassPermissions` |
| `color` | string | Colore di display nella sessione |
| `memory` | string | Scope Auto Memory: `user`, `project`, `local`, o assente |
| `isolation` | string | Imposta a `worktree` per isolare l'agent in un worktree git temporaneo |

### 12.5 Gerarchia di precedenza

Se esiste un subagent con lo stesso nome a più livelli, vince **quello più specifico**. L'ordine di precedenza, dal più alto al più basso:

1. **Managed settings** (configurazione organizzativa, rara nei setup individuali)
2. **`--agents` flag CLI** (subagent definiti per la singola sessione via flag al lancio)
3. **`.claude/agents/`** del progetto
4. **`~/.claude/agents/`** dell'utente
5. **Agent forniti da plugin installati**

Convenzione pratica: tieni in `~/.claude/agents/` gli agent **personali e generici** (es. `code-reviewer-style`, `commit-message-writer`), e in `.claude/agents/` del repo gli agent **specifici di quel progetto**, condivisi col team via Git. Gli agent dei plugin usano namespace `<plugin>:<agent-name>` quindi non collidono.

### 12.6 Invocazione automatica vs esplicita

Ci sono due modi per attivare un subagent.

**Automatica.** Il main agent legge la `description` di tutti i subagent disponibili e decide se delegare in base al match con il task corrente. Per questo la `description` è il campo più importante del frontmatter: scrivila pensando ai **trigger concreti** del workflow, non come paragrafo di marketing.

```yaml
# Brutto (vago, non triggera bene)
description: Agent for WordPress security.

# Buono (specifico, indica trigger reali)
description: |
  Use this agent to audit WordPress plugin code for security issues.
  Triggers on: PHP files in wp-content/plugins, mentions of nonce,
  capability checks, sanitize_*, esc_*, $wpdb queries.
```

**Esplicita.** Quando vuoi forzare l'uso di un agent specifico, lo menzioni con `@`:

```
@agent-wp-security-auditor analizza le ultime modifiche al
plugin in wp-content/plugins/access-control/
```

Digitando `@` apri un picker typeahead che ti mostra gli agent disponibili. Per agent forniti da plugin la sintassi è `@agent-<plugin>:<nome>`.

### 12.7 Parallelismo: pattern di delega multipla

Una nota di onestà su questo punto, perché in giro si vendono "agent paralleli" con leggerezza.

I subagent normali in Claude Code girano **sequenzialmente** in foreground: il main agent ne lancia uno, attende il risultato, ne lancia un altro. Non c'è concorrenza simultanea standard. Quello che chiamiamo "parallelismo" è quasi sempre una **delega multipla con context isolation**: lanci tre subagent indipendenti uno dopo l'altro, ognuno con la sua scheda, e ricevi tre summary indipendenti — il vantaggio è la separazione del contesto, non il tempo di esecuzione.

Pattern "deep review parallelo" (più correttamente: deep review delegato):

```
Tu: "Revisiona questa PR con tre angoli: sicurezza, performance,
     stile. Delega ciascun angolo a un subagent dedicato e
     riassumi i tre report alla fine."

Claude:
  → Agent(wp-security-auditor)    [analisi sicurezza]   ← 60s
    Risultato: 3 issue di sicurezza in 2 file

  → Agent(performance-reviewer)   [analisi performance] ← 45s
    Risultato: 2 query N+1, 1 cache mancante

  → Agent(style-reviewer)         [analisi stile]       ← 30s
    Risultato: 5 violazioni PSR-12, 2 commenti obsoleti

  Summary unificato per la PR.
```

Il vantaggio reale è che **il main agent non si è gonfiato** leggendo i file: ogni subagent l'ha fatto nella sua scheda, e nel main resta solo l'aggregazione finale. Tempo totale: somma dei tre.

**Se serve vero parallelismo simultaneo**, esiste la feature **Agent Teams**: più istanze indipendenti di Claude Code che girano davvero in concorrenza, coordinate via task list condivisa e mailbox di messaggi (i teammates si scrivono direttamente fra loro, non solo col lead come nei subagent). Richiede Claude Code v2.1.32+ e l'env `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` (o equivalente in `settings.json`).

> **⚠️ Feature sperimentale, da maneggiare con prudenza.** Anthropic dichiara Agent Teams *experimental and disabled by default* nella [pagina ufficiale](https://code.claude.com/docs/en/agent-teams). Limitazioni note rilevanti:
>
> - `/resume` e `/rewind` non ripristinano i teammates in-process — dopo un resume potresti dover rigenerare la team
> - lo stato dei task può "rimanere indietro": un task non marcato completato blocca i dipendenti
> - lo shutdown è lento (i teammates finiscono il turno corrente prima di uscire)
> - **una sola team per sessione**, niente team annidate, lead non riassegnabile
> - permessi settabili solo allo spawn (cambi successivi a teammate per teammate)
> - **split-pane richiede tmux o iTerm2**: non funziona in VS Code terminale, Windows Terminal, Ghostty
>
> Per la maggior parte dei workflow la delega multipla standard a subagent (descritta sopra) è sufficiente. Apri Agent Teams quando hai davvero bisogno di teammates che dialogano fra loro — code review parallele su prospettive diverse, debugging con ipotesi concorrenti, refactor cross-layer dove ogni teammate possiede un layer diverso.

Se decidi di usarli, gli eventi hook dedicati `TeammateIdle`, `TaskCreated` e `TaskCompleted` (vedi [sezione 13.3 — Eventi del lifecycle](#eventi-del-lifecycle)) permettono di applicare quality gate che la docs Anthropic suggerisce per disciplinare il comportamento dei teammates: bloccare task malformati alla creazione, rifiutare il "completato" se i test falliscono, riavviare un teammate idle quando ha ancora lavoro pendente.

### 12.8 Ottimizzazione costi via model routing

Il campo `model` del frontmatter abilita uno dei pattern più sottostimati di Claude Code: **routare task semplici a Haiku** invece che a Sonnet. Haiku costa una frazione di Sonnet (input/output) e su task ben definiti — pattern matching su molti file, classificazione, estrazione strutturata — la qualità è più che adeguata.

Caso tipico: devi auditare 50 file PHP per trovare quali usano `$wpdb->query()` con concatenazione invece di `$wpdb->prepare()`. È un task di pattern recognition, non di ragionamento architetturale.

```yaml
---
name: wp-sql-injection-scanner
description: |
  Use this agent to scan PHP files for direct concatenation in
  $wpdb queries (potential SQL injection). Triggers on: requests
  to audit SQL safety, mentions of $wpdb, manual SQL hardening.
tools: Read, Grep, Glob
model: haiku    # Haiku basta e avanza, costa molto meno
---

Sei uno scanner di SQL injection per WordPress.

Cerca tutti i file che chiamano $wpdb->query(),
$wpdb->get_results(), $wpdb->get_var(), $wpdb->get_row()
con stringhe SQL che concatenano variabili (`.` o interpolazione).

Per ogni occorrenza:
- File e riga
- Snippet della query incriminata
- Versione corretta usando $wpdb->prepare()

Ignora i casi in cui la query è 100% statica (nessuna variabile).
```

Il main agent (Sonnet) coordina e produce il report finale; il subagent (Haiku) fa il lavoro massivo di scan. La bolletta token cala sensibilmente. Lo stesso principio vale per estrazioni, riassunti, classificazioni — vedi anche la logica di [`opusplan` nella sezione 5](#plan-mode-pensare-prima-di-scrivere) per un'altra applicazione del pattern "modello giusto per la cosa giusta".

### 12.9 Quando NON usarli

I subagent non sono sempre la scelta giusta:

- **Task brevi**. Se il task richiede di leggere 2-3 file, il main agent fa direttamente in meno tempo. L'overhead di setup (descrizione del task al subagent, attesa, parsing del risultato) supera il beneficio.
- **Quando il summary perde informazioni**. Se hai bisogno che il main agent veda **il contenuto** di certi file — non solo un riassunto — la delega ti castra. Il subagent ti restituisce la sua sintesi, non i raw data.
- **Lavoro iterativo**. Se stai facendo refactor incrementale che richiede continuo back-and-forth (modifico, testo, modifico ancora), un subagent non aiuta: il main agent è già lo strumento giusto, semplicemente con `/compact` periodico per non gonfiare il contesto.
- **Task ad alto rischio dove vuoi controllo diretto**. Operazioni distruttive (delete, force push, migrazioni DB), errori di interpretazione del subagent costano caro. Tienile sul main agent in Plan Mode.

In dubbio: parti con il main agent. Se ti accorgi di aver letto 30 file solo per produrre 200 token di output, era un subagent.

### 12.10 Subagent, Skill e Hook a confronto

Claude Code ha **tre meccanismi di estensione** che è facile confondere. Vale la pena fissarli insieme perché fanno cose diverse e si combinano spesso.

| **Aspetto** | **Subagent** | **Skill** | **Hook** |
|---|---|---|---|
| Cos'è | Agent specializzato con context separato | Playbook riusabile inserito nel main context | Script che intercetta eventi del lifecycle |
| Chi lo scrive | Tu (file `.md` con frontmatter YAML) | Tu (file `SKILL.md` con frontmatter YAML) | Tu (script bash/HTTP/prompt) |
| Come si attiva | Delega del main agent o `@agent-name` esplicito | Match automatico sulla `description` o `/skill-name` | Automaticamente su evento |
| Scope contesto | Context window separato | Inline nel main context | Side effect, non aggiunge contesto |
| Output | Sommario al main agent | Contenuto integrato nella conversazione | Decisione `allow/deny/ask` o azione |
| Dove vivono | `.claude/agents/`, `~/.claude/agents/`, plugin | `.claude/skills/`, `~/.claude/skills/`, plugin | `settings.json` o `.claude/settings.json` |
| Caso d'uso tipico | Ricerca isolata, review specializzata, task massivi | Convenzioni di progetto, playbook ricorrenti, domain knowledge | Validazione comandi, audit, blocco operazioni rischiose |

Detto in una riga: **una Skill arricchisce il main agent, un Subagent lo sostituisce per il task delegato, un Hook fa qualcosa intorno al main agent senza farne parte**.

I tre meccanismi si **combinano** spesso: una Skill può istruire il main agent a delegare un certo task a un Subagent specifico, e quel Subagent può avere un Hook che valida i suoi tool call prima che vengano eseguiti.

Per la trattazione completa di Hook — eventi, tipi, esempi, sicurezza — vedi la [sezione 13](#hook-automatizzare-il-lifecycle-di-claude-code).

---


---

> ← [11. MCP](11-mcp.md) | [Index](README.md) | [13. Hook](13-hook.md) →
