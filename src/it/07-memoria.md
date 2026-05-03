# Guida Pratica a Claude Code CLI

> **Versione 4.23 — maggio 2026** — verificata su Claude Code v2.1.123
> Licenza [Creative Commons BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

> ← [6. Prompt engineering](06-prompt-engineering.md) | [Index](README.md) | [8. Gestione del contesto](08-contesto.md) →

---

## 7. Memoria persistente: CLAUDE.md e Auto Memory

Claude Code ha **due meccanismi di memoria persistente** che convivono e si completano: `CLAUDE.md` (contratto statico scritto da te) e Auto Memory (apprendimenti dinamici scritti dal modello). Capire come funzionano insieme è ciò che separa un uso casuale da uno professionale della CLI.

La prima parte di questo capitolo (7.1-7.5) copre `CLAUDE.md`: cos'è, come si genera, cosa contiene, esempi di progetto, gerarchia su monorepo. La seconda (7.6-7.12) copre Auto Memory: il sistema introdotto in v2.1.59 in cui Claude annota autonomamente ciò che impara dalle tue correzioni e lo riapplica nelle sessioni successive.

Il file `CLAUDE.md` nella root del progetto è il **contratto** tra te e Claude. Viene letto automaticamente a ogni sessione e fornisce il contesto persistente che altrimenti dovresti ripetere ogni volta. È anche la **destinazione naturale dei prompt che funzionano e si ripetono**: quando ti accorgi di scrivere la stessa istruzione in molte sessioni diverse, il suo posto è qui (vedi [sezione 6](#prompt-engineering-scrivere-prompt-efficaci) sul prompt engineering, in particolare il principio di "promozione" del prompt).

### 7.1 Generare CLAUDE.md con /init

Su un progetto nuovo in cui `CLAUDE.md` non esiste ancora, il modo più rapido per partire è il comando `/init`. Lanciato dalla root del progetto, Claude analizza il codebase (struttura cartelle, `package.json`/`composer.json`/`requirements.txt`, file di configurazione, README, eventuali test) e genera una bozza di `CLAUDE.md` con stack rilevato, comandi principali e convenzioni desunte.

```bash
# Dalla root del progetto
claude
> /init
```

L'output è un **buon punto di partenza**, non un file definitivo. Va sempre riletto e arricchito a mano per due ragioni:

- Claude può inferire male le convenzioni quando il codice esistente non è uniforme (es. metà del progetto in camelCase, metà in snake_case)
- Le **regole tribali** non scritte nel codice — "qui non si usa jQuery", "ogni endpoint deve avere uno schema Zod", "i test toccano il database vero, mai mock" — Claude non può inventarsele: vanno aggiunte tu.

Considera `/init` come uno scaffolding: ti risparmia 20 minuti di scrittura iniziale, poi tocca a te.

### 7.2 Cosa mettere in CLAUDE.md

Una buona struttura include:

1. **Descrizione del progetto** — cos'è, a chi serve
2. **Stack tecnologico** — linguaggi, framework, versioni
3. **Convenzioni di codice** — naming, pattern, stile commenti
4. **Comandi principali** — build, test, lint, deploy
5. **Architettura ad alto livello** — cartelle chiave, flusso dati
6. **Cosa NON fare** — anti-pattern, regole invalicabili

### 7.3 Esempio 1: Plugin WordPress

```markdown
# WP Access Control Block

## Descrizione
Plugin WordPress che aggiunge un Gutenberg block per controllare
la visibilità dei contenuti in base allo stato di login dell'utente.

## Stack
- PHP 8.1+
- WordPress 6.0+
- JavaScript con @wordpress/scripts (JSX)
- SCSS con metodologia BEM

## Convenzioni
- Commenti in codice: **italiano**
- README e documentazione utente: **inglese**
- Naming PHP: PSR-12, namespace `Mavida\WPAccessControl\`
- Naming JS: camelCase, componenti React in PascalCase
- CSS: BEM strict (`.block__element--modifier`)

## Comandi
- Build: `npm run build`
- Dev watch: `npm run start`
- Lint PHP: `composer lint`
- Lint JS: `npm run lint:js`
- Test PHP: `composer test`

## Struttura
- `src/` — sorgenti JS/SCSS (JSX, SCSS)
- `build/` — output compilato (non toccare manualmente)
- `includes/` — logica PHP lato server
- `block.json` — manifest del blocco

## Regole invalicabili
- NON usare jQuery nei nuovi componenti
- NON committare file in `build/`
- Ogni hook PHP deve avere nonce verification
- I render callback server-side devono essere **escaped** con le funzioni WP
```

### 7.4 Esempio 2: Progetto Node/TypeScript generico

```markdown
# API Analytics Service

## Descrizione
Microservizio REST per raccogliere e aggregare eventi di analytics.

## Stack
- Node.js 22 LTS
- TypeScript 5.4 (strict mode)
- Fastify 4
- PostgreSQL 16 + Prisma ORM
- Vitest per i test

## Convenzioni
- Tutti i tipi esportati devono essere in `src/types/`
- Schema Zod per validazione input (mai fidarsi del client)
- Commenti JSDoc per tutte le funzioni pubbliche
- Niente `any`, usa `unknown` e narrow

## Comandi
- Dev: `pnpm dev`
- Build: `pnpm build`
- Test: `pnpm test`
- Test coverage: `pnpm test:coverage`
- Migrazioni DB: `pnpm prisma migrate dev`

## Architettura
- `src/routes/` — endpoint HTTP
- `src/services/` — logica di business
- `src/repositories/` — accesso dati
- `src/schemas/` — validazione Zod

## Regole invalicabili
- NON importare direttamente Prisma client nei `routes/` — passare per `repositories/`
- Ogni endpoint deve avere uno schema Zod per body/params/query
- Test obbligatori per ogni nuovo service
```

### 7.5 CLAUDE.md gerarchici

Claude Code non legge un solo `CLAUDE.md`: ne legge **più di uno**, in ordine, dal generale al particolare. I file più specifici **integrano** (e quando serve sovrascrivono) quelli più generali. La gerarchia tipica è:

1. `~/.claude/CLAUDE.md` — **regole globali utente**
2. `<monorepo-root>/CLAUDE.md` — **regole del monorepo**
3. `<project>/CLAUDE.md` — **regole del singolo progetto**

#### Regole globali utente (`~/.claude/CLAUDE.md`)

È il tuo file personale, valido su **tutti i progetti** che apri da questa macchina. Lo trovi in:

- **Linux/macOS**: `~/.claude/CLAUDE.md`
- **Windows**: `C:\Users\<tuo-utente>\.claude\CLAUDE.md`

Ci metti dentro le tue **preferenze trasversali**: lingua dei commenti, stile delle risposte, tool che usi sempre, cose da non fare mai indipendentemente dal progetto. È il posto giusto per "io scrivo i commenti in italiano" o "non propormi mai soluzioni con jQuery se esiste un'alternativa vanilla".

#### Cos'è un monorepo

Un **monorepo** è un singolo repository Git che contiene **più progetti correlati** invece di averne uno per ognuno. È molto comune nello sviluppo moderno: un'azienda che mantiene insieme più plugin WordPress, oppure un team che tiene nello stesso repo un'API, un frontend e una libreria condivisa.

Una struttura tipica:

```
my-monorepo/
├── CLAUDE.md                    ← regole comuni a tutti i sotto-progetti
├── plugins/
│   ├── access-control/
│   │   └── CLAUDE.md            ← regole specifiche di questo plugin
│   └── analytics/
│       └── CLAUDE.md            ← regole specifiche di questo plugin
└── shared/
    └── utils/
```

Il `CLAUDE.md` a livello di monorepo cattura ciò che è **comune**: convenzioni di naming, stack di base, comandi di build orchestrati. I `CLAUDE.md` dei singoli progetti coprono le **specificità**: regole che valgono solo per quel sotto-progetto.

#### Differenze rispetto al singolo progetto

Quando lavori a un progetto isolato (non in monorepo), la gerarchia si riduce a due livelli: regole utente + regole progetto. Il `CLAUDE.md` del progetto contiene tutto quello che in un monorepo sarebbe spalmato su due file. Niente di sbagliato: la gerarchia esiste per evitare duplicazione, non per essere obbligatoria.

#### Esempio pratico a tre livelli

Supponiamo tu sviluppi plugin WordPress e tieni il tuo lavoro in un monorepo.

**`~/.claude/CLAUDE.md`** — preferenze personali, valide ovunque:

```markdown
# Preferenze personali

- Commenti nel codice: italiano
- Risposte: concise, vai dritto al punto, niente preamboli
- Quando proponi codice PHP, segui sempre PSR-12
- Non proporre soluzioni con jQuery se esiste una alternativa vanilla JS
- Prima di modifiche strutturali grandi, chiedi conferma
```

**`<monorepo-root>/CLAUDE.md`** — regole comuni a tutti i plugin del monorepo:

```markdown
# Monorepo Plugin WordPress

## Stack comune
- PHP 8.1+, WordPress 6.4+
- Build con @wordpress/scripts (npm)
- Test con PHPUnit + WP Test Suite

## Convenzioni comuni
- Namespace radice: `MyCompany\`
- Tutti i plugin sono prefissati `mc-` (es. `mc-access-control`)
- I file di traduzione vivono in `<plugin>/languages/`

## Comandi orchestrati
- Build di tutti i plugin: `npm run build:all`
- Test di tutti i plugin: `composer test:all`

## Regole invalicabili
- Ogni hook deve verificare nonce e capability
- Nessun output non escapato: usare `esc_html`, `esc_attr`, `wp_kses_post`
```

**`<monorepo-root>/plugins/access-control/CLAUDE.md`** — regole solo di questo plugin:

```markdown
# Plugin: Access Control

## Descrizione
Gutenberg block per controllare la visibilità dei contenuti
in base allo stato di login dell'utente.

## Specificità
- Block name: `mycompany/access-control`
- Render server-side via `render_callback` (no JS in frontend)
- Le regole di visibilità sono in `includes/Visibility/Rules.php`

## Cosa NON toccare
- Non modificare `block.json` senza rigenerare l'asset manifest
- I filtri `mc_access_control_can_view` sono API pubblica: niente breaking change
```

Quando apri Claude Code dentro `plugins/access-control/`, vede tutti e tre i livelli combinati: preferenze tue + convenzioni del monorepo + specificità del plugin. Tu scrivi ogni regola **una volta sola, al livello giusto**, e la riusi automaticamente ovunque abbia senso.

`CLAUDE.md` è la metà **statica** della memoria persistente di Claude Code: la scrivi tu, contiene le regole. Esiste anche una metà **dinamica** che Claude alimenta da solo nel tempo — è la Auto Memory, introdotta nella v2.1.59 e trattata nella seconda parte di questo capitolo.

---

A partire dalla **versione 2.1.59** Claude Code ha introdotto un secondo meccanismo di memoria persistente, complementare a `CLAUDE.md`: la **Auto Memory**. La differenza è netta:

- **`CLAUDE.md`** è **statico** — lo scrivi tu una volta, viene letto a ogni sessione, contiene regole e istruzioni.
- **Auto Memory** è **dinamica** — Claude la scrive da solo mentre lavora, accumulando ciò che ha imparato dalle tue correzioni e dalle sessioni passate.

Sono due meccanismi che convivono: uno è il **contratto** che imposti tu, l'altra è il **diario di apprendimento** che il modello tiene per conto suo.

### 7.6 Auto Memory: cos'è e cosa cambia

L'idea è semplice: oggi se correggi Claude tre volte sulla stessa cosa — *"non usare `var`, qui usiamo `let`/`const`"* — alla quarta volta, in una sessione diversa, lo rifà. Senza memoria persistente, ogni sessione parte da zero. Auto Memory chiude questo loop: Claude annota autonomamente la regola e la riapplica alle sessioni successive.

Quando Claude decide di salvare qualcosa, lo fa in base a un criterio interno: l'informazione sarà utile in conversazioni future? Comandi di build ricorrenti, convenzioni di naming che hai corretto, pattern architetturali del progetto, errori tipici da evitare. La documentazione Anthropic non descrive il meccanismo nel dettaglio; in pratica funziona meglio sui pattern ricorrenti che sulle singole occorrenze.

> **Esempio concreto.** Lavori su un codebase PHP che usa `snake_case` per i nomi di funzione. Claude propone inizialmente `camelCase` (default JavaScript-style). Tu correggi una volta, due, tre. Auto Memory annota la convenzione del progetto. Alla quarta sessione, prima ancora che tu apra bocca, Claude propone già `snake_case`. La correzione esplicita non serve più: il modello ha imparato.

### 7.7 Requisiti e abilitazione

- **Versione minima**: Claude Code 2.1.59. Verifica con `claude --version` e aggiorna se necessario.
- **Stato di default**: **attiva**. Non devi fare nulla per abilitarla.
- **Comando di gestione**: `/memory` mostra tutti i file `CLAUDE.md`, `CLAUDE.local.md` e regole caricati nella sessione corrente, permette di togglare Auto Memory on/off e fornisce un link diretto per aprire la cartella delle memory nell'editor.
- **Disabilitazione persistente**: in `settings.json` (utente o locale, **non** progetto, per ragioni di sicurezza):

  ```json
  { "autoMemoryEnabled": false }
  ```

- **Disabilitazione via env**: la variabile d'ambiente `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1` spegne la feature per la singola sessione. Utile in CI/CD o sessioni una-tantum.
- **Spostare la cartella**: il setting `autoMemoryDirectory` (sempre in user/local settings) ti permette di salvare le memory in un percorso custom — per esempio una directory sincronizzata con un altro device tramite cloud, o una location cifrata.

### 7.8 Dove vivono le memorie

Path standard:

- **Linux/macOS**: `~/.claude/projects/<project>/memory/`
- **Windows**: `C:\Users\<tuo-utente>\.claude\projects\<project>\memory\`

Il segmento `<project>` è derivato dal **repository Git** (URL del remote). Fuori da un repo Git, viene usata la root del working directory. Conseguenza importante: **worktree e subdirectory dello stesso repo condividono la stessa memory**. Se tieni due copie del repo per lavorare in parallelo su due branch, Claude impara da entrambe le sessioni come se fosse una sola.

### 7.9 Anatomia della cartella memory

Dentro `memory/` non c'è un singolo file: c'è un **indice** più dei **file tematici**.

```
~/.claude/projects/myproject/memory/
├── MEMORY.md              ← indice, caricato a ogni sessione
├── debugging.md           ← topic file: pattern di debug ricorrenti
├── api-conventions.md     ← topic file: regole API del progetto
└── build-commands.md      ← topic file: comandi di build orchestrati
```

- **`MEMORY.md`** è l'indice. Viene caricato **a ogni sessione**, ma solo per le **prime 200 righe** (circa 25 KB). Anthropic consiglia di tenerlo entro questo limite per non sprecare contesto.
- **Topic file** (`debugging.md`, `api-conventions.md`, ecc.) sono caricati **on-demand**: solo quando il loro contenuto è rilevante per il task in corso. Possono essere arbitrariamente lunghi senza saturare il contesto della sessione.

Questa è la **differenza tecnica chiave rispetto a CLAUDE.md**, che invece viene letto sempre per intero. Auto Memory è progettata per **scalare**: puoi accumulare conoscenza nel tempo senza pagarla in token a ogni sessione.

### 7.10 Auto Memory e subagent

I subagent (vedi sezione 12) possono mantenere la **propria** Auto Memory, separata da quella della sessione principale. È pensato per subagent specializzati che eseguono task ricorrenti — per esempio un agent di code review che impara nel tempo lo stile di review preferito — senza inquinare la memoria del lavoro generale. La configurazione si imposta a livello di definizione del subagent.

### 7.11 Quando disabilitarla

Auto Memory non lascia il computer: tutto vive in `~/.claude/projects/...` sulla tua macchina locale, e le memory **non vengono inviate ad Anthropic per training**. La disabilitazione non è quindi una questione di privacy verso Anthropic, ma di **controllo locale** in scenari specifici:

- **Codebase con dati sensibili**: se in chat compaiono frammenti di dati reali (PII, segreti, dati clinici), preferisci non lasciarne traccia neppure in un file locale che potrebbe essere copiato per backup, sincronizzato altrove, o letto da chi ha accesso fisico alla macchina.
- **Progetti regolamentati**: in ambito sanità, finanza o GDPR, alcune policy aziendali vietano qualsiasi forma di memoria persistente al di fuori dei sistemi controllati. Disabilitare Auto Memory è la scelta sicura per restare conformi.
- **Sessioni esplorative**: stai sperimentando un approccio che probabilmente abbandonerai. Non vuoi che Claude impari pattern da una soluzione transitoria e te li riproponga in futuro come se fossero regole consolidate.

In dubbio, parti attiva e disabilita per sessione o progetto quando serve.

### 7.12 CLAUDE.md vs Auto Memory: quando usare cosa

| **Aspetto** | **CLAUDE.md** | **Auto Memory** |
|---|---|---|
| Chi lo scrive | Tu | Claude |
| Cosa contiene | Istruzioni e regole | Apprendimenti e pattern emersi lavorando |
| Scope | Progetto, utente, organizzazione | Per repository (un'unica cartella per repo) |
| Caricato in sessione | Sempre, per intero | `MEMORY.md` sempre (max 200 righe), topic file on-demand |
| Tipico contenuto | Stack, convenzioni, comandi, regole invalicabili | Comandi di build ricorrenti, sfumature di stile, errori già corretti |

**Pattern consigliato**: usa `CLAUDE.md` per le **regole invalicabili** — le cose che non vuoi rinegoziare ogni volta — e lascia Auto Memory per le **sfumature** che emergono lavorando. Se ti accorgi che una memoria appresa è importante e stabile, **promuovila** trasferendola manualmente in `CLAUDE.md`. Da quel momento è una regola contrattuale, non più solo un'osservazione che Claude potrebbe dimenticare se rivede il file.

> Per chi conosce già la distinzione, esiste una terza via complementare: **`CLAUDE.local.md`**, un file Markdown manuale come `CLAUDE.md` ma **gitignored** per default. Lo scrivi tu, è specifico della tua copia locale, non viene committato. È utile per preferenze personali del singolo dev su un progetto condiviso (percorsi di tool locali, scorciatoie tue), senza imporle al team.

---


---

> ← [6. Prompt engineering](06-prompt-engineering.md) | [Index](README.md) | [8. Gestione del contesto](08-contesto.md) →
