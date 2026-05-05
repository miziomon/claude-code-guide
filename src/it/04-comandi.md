# Guida Pratica a Claude Code CLI

> **Versione 4.30 — maggio 2026** — verificata su Claude Code v2.1.123
> Licenza [Creative Commons BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

> ← [3. Il primo progetto end-to-end](03-primo-progetto.md) | [Index](README.md) | [5. Plan Mode](05-plan-mode.md) →

---

## 4. Comandi e scorciatoie essenziali

Claude Code è un'applicazione **comando-first**: niente menu a discesa, niente palette di pulsanti, niente preferenze nascoste in finestre di dialogo. Tutto si fa con tre tipi di sintassi che imparerai una volta e userai migliaia di volte. Questo capitolo spiega prima la filosofia, poi entra nel dettaglio dei comandi più usati nel quotidiano.

### 4.1 La sintassi a comandi: perché funziona così

Chi viene da un'applicazione desktop si aspetta menu, icone, scorciatoie con etichetta sotto al pulsante. Claude Code non ha niente di tutto questo: si comanda **scrivendo**. Tre famiglie di sintassi:

- **Flag CLI** (passati a `claude` da terminale): `claude --continue`, `claude -p "prompt"`, `claude --model sonnet`. Definiscono **come si avvia** una sessione.
- **Slash command** (digitati dentro la sessione interattiva): `/init`, `/clear`, `/plan`, `/agents`. Cambiano lo stato o eseguono azioni **durante** la sessione.
- **Scorciatoie da tastiera**: `Shift+Tab`, `Esc Esc`, `Alt+P`. Modificano comportamento e modi **al volo**.

A prima vista può spaventare: senza un menu dove "guardare", come si fa a scoprire cosa esiste? Risposta: c'è un picker. Digita `/` da solo nella sessione e si apre l'elenco filtrabile di tutti gli slash command disponibili — quelli built-in, quelli installati da plugin, quelli aggiunti da te. Digita `/co` e filtri a `/compact`, `/config`, `/copy`, `/continue`, `/cost`. Lo stesso vale per `claude --help` da terminale per i flag.

Il principio è quello adottato da git, vim, SQL, e da quasi tutti gli strumenti professionali del terminale: **efficienza maggiore della scopribilità**. Imparare un comando costa più di cliccare un pulsante la prima volta; ma il comando lo digiti in mezzo secondo per cento volte di seguito, e su una sessione di lavoro intensa fa la differenza. Una volta interiorizzato che `/clear` resetta il contesto, non torni più a cercare un pulsante "nuova chat" perché due caratteri sono più veloci di qualunque click.

> **Una mentalità utile**. Pensa al prompt come a una shell potenziata. In bash digiti `git status`, in Claude Code digiti `/context`. La differenza non è cosmetica: il modello legge il tuo input e decide cosa fare, ma i comandi che iniziano con `/` o le scorciatoie con modificatore sono **deterministici** — agiscono sull'ambiente della sessione, non sull'agente. È la stessa distinzione fra un comando shell e una richiesta linguistica al modello.

Tre prefissi speciali rendono l'esperienza ancora più fluida: `@` per riferire un file o un subagent (vedi [sezione 12](#subagent-orchestrare-lavoro-specializzato)), `!` per eseguire una riga di shell senza interpretazione del modello, `/` per il picker comandi. Li approfondisco in 4.8.

> **Disclaimer di evoluzione.** Claude Code introduce nuovi slash command quasi a ogni release: dai ~30 di metà 2025 ai 90+ di aprile 2026. Questa guida documenta i comandi più stabili e usati al momento della stesura. Per la lista viva e completa: `claude --help` da terminale, `/help` o `/` dentro la sessione, e la [CLI reference ufficiale](https://code.claude.com/docs/en/cli-reference).

### 4.2 Flag CLI essenziali

Sono i flag che userai ogni giorno. Tabella stretta, poi approfondimento per i più importanti:

| Flag | Forma breve | Cosa fa |
|---|---|---|
| `claude` | — | Avvia una sessione interattiva |
| `claude "prompt"` | — | Avvia con un prompt iniziale già scritto |
| `claude --continue` | `-c` | Riprende la sessione più recente nella directory |
| `claude --resume` | `-r` | Apre un picker delle sessioni passate per scegliere |
| `claude --print "prompt"` | `-p` | Modalità non-interattiva (headless): esegue, stampa, esce |
| `claude --model <nome>` | — | Sceglie il modello (es. `sonnet`, `opus`, `haiku`, `opusplan`) |
| `claude --permission-mode <modo>` | — | Avvia in un modo di permessi specifico (`default`, `acceptEdits`, `plan`, `auto`, `bypassPermissions`) |
| `claude --output-format <fmt>` | — | Formato output: `text`, `json`, `stream-json` (per pipeline CI/CD) |
| `claude --add-dir <path>` | — | Aggiunge directory di lavoro accessibili oltre alla `cwd` |
| `claude --dangerously-skip-permissions` | — | Salta tutte le conferme. Solo in ambienti isolati (vedi sezione 10) |
| `claude --version` | `-v` | Mostra la versione installata |
| `claude --help` | `-h` | Lista i flag principali |

#### `-p` / `--print`: modalità headless

Il flag che apre Claude Code al mondo dell'automazione. Esegue un singolo prompt, stampa l'output e esce — niente sessione interattiva. È il pilastro di ogni integrazione CI/CD:

```bash
# Esempio: review automatica delle modifiche di una PR
claude -p "Review the changes in this PR and flag any security issues" \
       --output-format json > review.json

# Pipeline: passare un file via stdin
cat changelog.md | claude -p "Riassumi questo changelog in 5 bullet points"
```

Combinato con `--output-format json` produce output strutturato parsabile da step successivi della pipeline. Vedi anche `--max-turns` e `--max-budget-usd` in 5.3 per limitare l'esecuzione.

#### `-c` / `--continue` e `-r` / `--resume`

Le due sintassi per riprendere una conversazione. La differenza è semplice:

- `claude -c` apre **l'ultima sessione** in questa directory. Caso d'uso: hai chiuso 10 minuti fa, vuoi riprendere da lì.
- `claude -r` apre un **picker interattivo** che mostra tutte le sessioni passate (con nome, data, primo prompt). Caso d'uso: vuoi tornare a quella conversazione di tre giorni fa sul refactor del modulo auth.

Entrambi accettano anche un prompt aggiuntivo per ripartire con una richiesta nuova:

```bash
claude -c "Continua dal punto del refactor: ora aggiungi i test"
```

#### `--model` e i suoi alias

Tre alias principali (`sonnet`, `opus`, `haiku`) più la modalità ibrida `opusplan` (vedi [sezione 5](#plan-mode-pensare-prima-di-scrivere)) e la sintassi con ID completo (`claude-sonnet-4-6`, `claude-opus-4-7`, ecc.). Gli alias si aggiornano automaticamente al modello più recente: scrivere `--model sonnet` oggi e domani può puntare a versioni diverse. Per riproducibilità in CI/CD usa l'ID completo.

### 4.3 Flag CLI avanzati

Una selezione di flag specialistici, raggruppati per scenario. Per la lista viva e completa: [`claude --help`](https://code.claude.com/docs/en/cli-reference).

| Categoria | Flag principali | Quando ti servono |
|---|---|---|
| Esecuzione bounded | `--max-turns N`, `--max-budget-usd X` | Limitare costo o profondità in modalità headless |
| Output strutturato | `--output-format json\|stream-json`, `--json-schema <schema>`, `--include-hook-events` | Parsing automatico in pipeline, validazione schema |
| Sessioni avanzate | `--fork-session`, `--session-id <UUID>`, `--name "<nome>"`, `--no-session-persistence` | Branching, ID controllato, sessioni effimere |
| MCP e plugin | `--mcp-config <path>`, `--strict-mcp-config`, `--plugin-dir <path>`, `--tools "Read,Edit"`, `--allowedTools`, `--disallowedTools` | Configurazione fine di tool e integrazioni |
| Sessioni web | `--remote "task"`, `--rc [name]`, `--teleport`, `--from-pr <numero>` | Portare la sessione su claude.ai e viceversa |
| Worktree e team | `--worktree <name>` (`-w`), `--tmux`, `--teammate-mode` | Lavoro parallelo su branch isolati con git worktree |
| System prompt | `--system-prompt "..."`, `--append-system-prompt "..."`, `--system-prompt-file <path>` | Personalizzare o estendere le istruzioni di sistema |
| Subagent inline | `--agent <nome>`, `--agents '{"name":{"prompt":"..."}}'` | Definire subagent al volo senza creare file |
| Diagnostica | `--debug`, `--verbose`, `--debug-file <path>` | Troubleshooting di hook, MCP, comportamenti anomali |
| Performance | `--bare`, `--exclude-dynamic-system-prompt-sections` | Startup veloce per script, ottimizzazione cache |
| Effort/thinking | `--effort low\|medium\|high\|xhigh\|max` | Trade-off velocità vs profondità |

A questi si aggiungono i comandi separati che non usano il prefisso `claude` come argomento di sessione: `claude doctor` (diagnostica), `claude install [versione]`, `claude update`, `claude auth login|logout|status`, `claude agents` (lista subagent), `claude plugin <subcommand>`, `claude mcp <subcommand>`, `claude setup-token` (token long-lived per CI). La logica è semplice: i **flag** modificano l'avvio di una sessione, i **subcomandi** eseguono azioni amministrative senza aprirla.

### 4.4 Slash command: il cuore della sessione interattiva

Una volta dentro la sessione, gli **slash command** sono il modo per dire a Claude Code "fai questa cosa specifica" senza ambiguità. La distinzione importante è fra:

- **Slash command built-in**: parte del prodotto base (`/init`, `/clear`, `/compact`, `/plan`, `/agents`, `/hooks`, ecc.). Sono i mattoni di sistema.
- **Skill** invocate come slash command (`/security-review`, `/simplify`, `/loop`, `/ultrareview`, ecc.). Sono playbook documentati nel [capitolo 10](#skill-il-meccanismo-di-estensione) e si comportano come slash command perché Anthropic ha scelto la stessa sintassi: digiti `/`, vedi tutto insieme.
- **Comandi custom** che puoi definire tu in `.claude/commands/` (vedi [sezione 15](#workflow-avanzati-e-tips) "Custom slash command") — appariranno nello stesso picker.
- **Prompt MCP**: server MCP installati possono esporre comandi in formato `/mcp__<server>__<prompt>`.

Tutti finiscono nello stesso picker quando digiti `/`. Filtralo a tastiera scrivendo le prime lettere.

### 4.5 Slash command essenziali

Anthropic ha già superato i 50 slash command built-in (più quelli aggiunti da skill, plugin e MCP), e l'elenco cresce a ogni release. Questa tabella è una **selezione curata** dei comandi che incontrerai più spesso nel quotidiano: per la lista viva e completa lancia `/help` in sessione o consulta la [reference ufficiale](https://code.claude.com/docs/en/commands).

| Comando | Cosa fa |
|---|---|
| `/help` | Lista tutti i comandi disponibili |
| `/init` | Genera `CLAUDE.md` analizzando il progetto |
| `/plan [descrizione]` | Entra in Plan Mode (read-only) |
| `/clear` | Azzera il contesto della conversazione (alias: `/reset`, `/new`) |
| `/compact [istruzioni]` | Comprime la conversazione in un sommario |
| `/context` | Visualizza l'uso del contesto con suggerimenti di ottimizzazione |
| `/memory` | Gestione di Auto Memory e file `CLAUDE.md` caricati |
| `/agents` | Lista, crea, gestisci subagent |
| `/hooks` | Browser read-only della configurazione hook attiva |
| `/model [nome]` | Cambia modello durante la sessione |
| `/effort [livello]` ★ | Imposta effort: `low`, `medium`, `high`, `xhigh`, `max`, `auto` |
| `/fast [on\|off]` | Abilita/disabilita fast mode |
| `/undo` | Annulla l'ultima azione di Claude |
| `/rewind` | Riavvolge a un punto precedente (alias: `/checkpoint`) |
| `/branch [nome]` | Crea un branch della conversazione corrente (alias: `/fork`) |
| `/rename [nome]` ★ | Rinomina la sessione corrente per ritrovarla in `/resume` |
| `/resume [sessione]` | Riprende una conversazione (alias: `/continue`) |
| `/diff` | Diff viewer interattivo (modifiche non committate + per-turn diff) |
| `/copy [N]` | Copia l'ultima risposta nella clipboard |
| `/usage` | Costo sessione, limiti del piano, statistiche (alias: `/cost`, `/stats`) |
| `/btw <domanda>` ★ | Domanda laterale che non inquina la history (no tool use) |
| `/ultrareview [PR]` ★ | Review multi-agente cloud del branch o di una PR GitHub |
| `/recap` | Riepilogo della sessione corrente |
| `/config` | Pannello settings (tema, modello, output style, ecc.) |
| `/exit` o `/quit` | Chiude la sessione |

> ★ Comandi introdotti nelle release recenti (v2.1.110+ di Claude Code, primavera 2026). Se non li trovi, aggiorna con `claude update`.

#### `/init` — generare CLAUDE.md per un progetto nuovo

Vedi sezione [7 — Memoria persistente](#memoria-persistente-claude.md-e-auto-memory). In sintesi: lanciato dalla root del progetto, analizza struttura, file di config e dipendenze e produce una bozza di `CLAUDE.md` da rifinire a mano. È il primo comando da lanciare su un repo nuovo.

#### `/plan` e Plan Mode

Vedi sezione [5 — Plan Mode](#plan-mode-pensare-prima-di-scrivere). Entra in modalità read-only: Claude analizza, propone un piano, ma non scrive niente finché non approvi. La feature più importante per un uso sicuro della CLI.

#### `/clear`, `/compact`, `/context` — gestione del contesto

Vedi sezione [8 — Gestione del contesto](#gestione-del-contesto). In tre comandi:

- `/clear` azzera tutto, sessione fresh.
- `/compact` riassume la conversazione mantenendo le decisioni chiave, libera token.
- `/context` mostra quanto stai consumando e ti dice se è il momento di intervenire.

Esempio concreto:

```
[Dopo aver letto 30 file e fatto un refactor pesante]
/context
> Context usage: 78% (156k / 200k token)
>   Tool results: 112k (file letti, output di build)
>   Conversation: 38k

/compact mantenendo la decisione di usare Repository pattern
> [conversazione compressa, contesto liberato]
```

#### `/memory` — Auto Memory

Vedi sezione [7 — Memoria persistente](#memoria-persistente-claude.md-e-auto-memory). Mostra i file `CLAUDE.md` caricati nella sessione corrente, permette di togglare Auto Memory on/off, apre la cartella delle memory.

#### `/agents` — subagent

Vedi sezione [13 — Subagent](#subagent-orchestrare-lavoro-specializzato). Apre un'interfaccia tabbed: tab "Running" elenca i subagent attivi, tab "Library" mostra quelli disponibili e permette di crearne di nuovi.

#### `/hooks` — ispezione configurazione hook

Vedi sezione [14 — Hook](#hook-automatizzare-il-lifecycle-di-claude-code). Mostra la configurazione hook attiva: per ogni evento, quanti hook sono registrati e da quale file di settings. **Read-only**: per modificare gli hook devi editare `settings.json` direttamente.

#### `/model` ed `/effort` — scegliere il modello giusto

Vedi sezione [5 — Plan Mode](#plan-mode-pensare-prima-di-scrivere) (paragrafo `opusplan`). `/model` apre il picker e ti permette di switchare a runtime; `/effort` regola il "livello di sforzo" del modello (più alto = più tempo di ragionamento, output potenzialmente migliore, costo maggiore). `auto` lascia decidere a Claude.

#### `/undo`, `/rewind`, `/branch` — checkpoint conversazionale

Tre comandi correlati per gestire il "tempo" nella sessione:

- `/undo` annulla l'**ultima azione** di Claude (es. l'ultimo edit di file).
- `/rewind` riavvolge a un **punto precedente** della conversazione e ripristina lo stato (codice e contesto). Comando potente per chi sperimenta — lo usi quando un percorso si è dimostrato sbagliato e vuoi tornare indietro di N step.
- `/branch [nome]` crea un **fork** della conversazione nel punto corrente. La conversazione originale resta intatta, tu prosegui in una linea parallela. Caso d'uso: hai un'idea alternativa e vuoi esplorarla senza perdere il filo principale. Torni all'originale con `/resume`.

#### `/btw` — la domanda laterale

Comando poco conosciuto ma utile. Fai una domanda che **non vuoi nella history** della sessione: Claude la vede, risponde basandosi sul contesto attuale, ma la conversazione non si sporca. Niente tool use. Esempio:

```
/btw che differenza c'è tra @wordpress/scripts e @wordpress/create-block?
> [Claude risponde da knowledge, niente file letti, niente edit]
```

Perfetto per chiarimenti veloci durante un task lungo, senza farne deragliare il filo.

### 4.6 Slash command per workflow specifici

Tabella raggruppata, una riga per categoria. Tutti questi comandi sono documentati in dettaglio nella [reference ufficiale](https://code.claude.com/docs/en/commands).

| Categoria | Comandi |
|---|---|
| Skill cloud (review distribuita) | `/ultrareview [PR]`, `/ultraplan <prompt>`, `/autofix-pr [prompt]` |
| Code review locale | `/review [PR]`, `/security-review`, `/simplify [focus]` |
| Esecuzione e batch | `/batch <istruzione>`, `/loop [interval] [prompt]`, `/schedule [descr]` (alias `/routines`) |
| Diagnostica e troubleshooting | `/doctor`, `/debug [descrizione]`, `/heapdump`, `/usage` |
| Esportazione | `/export [filename]`, `/copy [N]` |
| Esperienza terminale | `/theme`, `/keybindings`, `/terminal-setup`, `/tui [default\|fullscreen]`, `/focus` |
| Integrazione IDE/web | `/ide`, `/desktop` (alias `/app`), `/teleport` (alias `/tp`), `/web-setup` |
| MCP e plugin | `/mcp`, `/plugin` (alias `/plugins`), `/reload-plugins` |
| Permessi e sicurezza | `/permissions` (alias `/allowed-tools`), `/sandbox` |
| Stato e statistiche | `/status`, `/insights`, `/release-notes`, `/team-onboarding` |
| Auth e profilo | `/login`, `/logout`, `/privacy-settings`, `/upgrade` |
| Accessibilità e input | `/voice [hold\|tap\|off]` |
| Background tasks | `/tasks` (alias `/bashes`) |
| Skill di apprendimento | `/powerup`, `/feedback` (alias `/bug`) |

### 4.7 Scorciatoie da tastiera

Raggruppate per ambito d'uso.

#### Modi di permesso (il ciclo principale)

`Shift+Tab` **cicla** tra i modi di permesso: `default → acceptEdits → plan → modi custom → default`. Non è un binding "Plan Mode": è un selettore di modo. Per arrivare a Plan Mode da `default` premi due volte; per uscirne, premi finché non torni a `default`. Lo stato corrente è sempre indicato nella prompt bar.

#### Modello e thinking

| Scorciatoia | Azione |
|---|---|
| `Alt+P` (`Option+P` su macOS) | Apre il picker modello senza cancellare il prompt in corso |
| `Alt+T` | Toggle extended thinking |
| `Alt+O` | Toggle fast mode |

Su macOS richiedono la configurazione *Option as Meta key* nel terminale.

#### Sessione e flusso

| Scorciatoia | Azione |
|---|---|
| `Ctrl+C` | Cancella input corrente o interrompe la generazione |
| `Ctrl+D` | Esce dalla sessione |
| `Ctrl+L` | Pulisce lo schermo e ridisegna (la conversazione resta) |
| `Esc Esc` | Riavvolge/riassume la conversazione (rewind/summarize, vedi `/rewind`) |
| `Ctrl+B` | Mette in background le task running (utenti tmux: due volte) |
| `Ctrl+X Ctrl+K` | Termina tutti i background agent (due volte entro 3 secondi per confermare) |

#### Transcript e history

| Scorciatoia | Azione |
|---|---|
| `Ctrl+O` | Apre il transcript viewer (mostra tool use dettagliati, MCP call espansi) |
| `Ctrl+R` | Reverse search nella history dei prompt |
| `Frecce su/giù` (o `Ctrl+P`/`Ctrl+N`) | Naviga nella history |

Dentro il transcript viewer (`Ctrl+O`): `Ctrl+E` espande/contrae, `[` scrive l'intera conversazione nello scrollback per `Cmd+F`/copy, `v` apre in `$VISUAL`/`$EDITOR`, `q` o `Esc` chiude.

#### Editing del prompt (readline-style)

| Scorciatoia | Azione |
|---|---|
| `Ctrl+A` | Inizio riga |
| `Ctrl+E` | Fine riga |
| `Ctrl+K` | Cancella fino a fine riga |
| `Ctrl+U` | Cancella fino a inizio riga |
| `Ctrl+W` | Cancella la parola precedente |
| `Ctrl+Y` | Reincolla l'ultimo testo cancellato |
| `Alt+B` / `Alt+F` | Sposta cursore di una parola indietro / avanti |
| `Ctrl+G` o `Ctrl+X Ctrl+E` | Apri il prompt in `$EDITOR` per modifiche complesse |

Sono le stesse convenzioni di `bash`/`zsh`/Emacs. Se vieni dal terminale Unix, le conosci già.

#### Multiline

| Metodo | Disponibilità |
|---|---|
| `\` + `Enter` | Tutti i terminali (più affidabile) |
| `Shift+Enter` | iTerm2, WezTerm, Ghostty, Kitty, Warp, Apple Terminal (nativo) |
| `Option+Enter` (macOS) | Dopo configurazione *Option as Meta* |
| `Ctrl+J` | Qualsiasi terminale (sintassi readline-native) |

Su VS Code, Cursor, Windsurf, Alacritty, Zed serve eseguire `/terminal-setup` la prima volta.

#### Modalità Vi

Se vieni da Vim, attivala con `/config` → Editor mode → `vi`. Avrai NORMAL/INSERT/VISUAL completi con motions (`hjkl`, `w`/`e`/`b`, `0`/`$`, `f{char}`) e operatori (`d`, `c`, `y`, `>`/`<`). Documentazione completa in [interactive-mode#vim-editor-mode](https://code.claude.com/docs/en/interactive-mode).

### 4.8 La sintassi `@`, `!`, `/` — i tre prefissi che cambiano tutto

Tre singoli caratteri che, posti all'inizio dell'input o inline, attivano scorciatoie potenti. È la versione "Claude Code" delle dollar-substitution di bash o delle reference Markdown:

#### `/` — il picker comandi

Digitato a inizio riga apre il picker filtrabile di **tutti** gli slash command disponibili nella sessione: built-in, skill, comandi custom, prompt MCP. Continua a digitare per filtrare. È il modo per scoprire cosa c'è senza leggere documentazione.

```
/co
> /compact     Comprimi conversazione...
> /config      Apri pannello settings...
> /context     Visualizza uso contesto...
> /continue    Alias di /resume...
> /copy        Copia ultima risposta...
> /cost        Alias di /usage...
```

#### `!` — bash inline

Digitato a inizio riga, esegue **direttamente la riga come comando shell**, senza interpretazione del modello. L'output entra nella sessione come messaggio. Equivale a uscire un attimo dal terminale Claude per fare un comando rapido, senza perdere il filo:

```
!git status --short
> M  src/guida.md
> M  scripts/style.css

!ls -la output/
> total 2.6M
> -rw-r--r-- ... Guida_Claude_Code_CLI.pdf
> -rw-r--r-- ... Guida_Claude_Code_CLI_17x24.pdf
```

Perfetto per controlli rapidi (`git status`, `ls`, `pwd`, `echo $VAR`) senza dover dire a Claude *"esegui per favore..."*.

#### `@` — riferimenti a file e subagent

Digitato inline (in mezzo a una frase) apre un picker che autocompleta:

- **Path di file e cartelle** del progetto: scrivi `@src/` e tabbi a `src/guida.md`. Il path inserito viene letto da Claude come riferimento al file.
- **Subagent disponibili**: `@agent-wp-security-auditor` per invocare esplicitamente un subagent custom (vedi [sezione 12](#subagent-orchestrare-lavoro-specializzato)).

Esempio combinato:

```
Rivedi @src/guida.md per refusi nei capitoli 5 e 6.
Quando trovi una sezione che parla di sicurezza,
delega a @agent-wp-security-auditor per audit più approfondito.
```

I tre prefissi non sono "comandi avanzati": sono il **modo quotidiano** di lavorare velocemente in Claude Code una volta che li hai metabolizzati.

---


---

> ← [3. Il primo progetto end-to-end](03-primo-progetto.md) | [Index](README.md) | [5. Plan Mode](05-plan-mode.md) →
