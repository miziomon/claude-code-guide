# Guida Pratica a Claude Code CLI

> **Versione 4.23 — maggio 2026** — verificata su Claude Code v2.1.123
> Licenza [Creative Commons BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

> ← [7. Memoria persistente](07-memoria.md) | [Index](README.md) | [9. Sicurezza e permessi](09-sicurezza.md) →

---

## 8. Gestione del contesto

La finestra di contesto è la risorsa più preziosa di Claude Code, e quella che la maggior parte degli utenti gestisce peggio. Capire cosa la riempie, come si degrada quando è troppo piena, e come intervenire prima che diventi un problema, è la differenza tra un uso casuale e un uso professionale della CLI.

### 8.1 Cos'è il contesto e perché conta

Il **contesto** è la quantità totale di informazioni che il modello vede in un singolo turno: il system prompt di Claude Code, i file `CLAUDE.md` caricati, la cronologia della conversazione, l'output dei tool eseguiti, i contenuti dei file letti, le definizioni delle skill e dei tool MCP attivi. Tutto questo viene misurato in **token** — unità di testo (un token corrisponde grosso modo a 4 caratteri in inglese, un po' meno in italiano).

I modelli Claude di aprile 2026 hanno due dimensioni di finestra:

- **200.000 token** — il default. Sufficiente per la stragrande maggioranza dei task.
- **1.000.000 token** — disponibile su modelli specifici (vedi 9.7), pensato per analisi di codebase grandi e contesti molto ampi.

Avere una finestra grande non significa avere prestazioni costanti su tutta la lunghezza. Anthropic ha documentato esplicitamente un fenomeno chiamato **context rot**: man mano che il numero di token cresce, accuratezza e capacità di richiamo del modello degradano. Non è un bug: è una conseguenza architetturale della struttura attention-based dei transformer (relazioni paritarie tra token che esplodono quadraticamente con la dimensione). In pratica, un modello con il contesto al 90% di occupazione **non lavora come uno fresco al 10%**, anche se la finestra è la stessa.

Concretamente, questo significa che il contesto va trattato come una **risorsa scarsa, non come una pattumiera**. La buona pratica non è "carico tutto e vediamo cosa succede": è scegliere con cura cosa entra, cosa esce, e quando azzerare e ripartire.

### 8.2 Cosa pesa nel contesto

Una sessione Claude Code, prima ancora che tu scriva il primo prompt, ha già caricato un certo numero di token. Sapere quali sono le categorie ti aiuta a capire dove intervenire.

| Categoria | Peso indicativo | Quando si carica |
|---|---|---|
| **System prompt** | ~4.200 token | Sempre, all'avvio |
| **Environment info** (cwd, OS, shell, git status) | ~280 token | Sempre, all'avvio |
| **MCP tools (deferred)** | ~120 token (solo nomi, schemi on-demand) | Sempre, all'avvio |
| **MEMORY.md (Auto Memory indice)** | fino a ~6.500 token (max 200 righe / 25 KB) | Sempre, se Auto Memory attiva |
| **CLAUDE.md (gerarchici)** | dipende dalla lunghezza | Sempre, **per intero**, ogni sessione |
| **Skill descriptions** | ~1% della finestra (~2.000 token, default 8 KB caratteri) | Sempre per ogni skill attiva non disabilitata |
| **Tool results** (file letti, output Bash, ecc.) | molto variabile, spesso la voce più grossa | Dinamicamente, durante il lavoro |
| **Conversation** (tuoi prompt + risposte) | variabile | Dinamicamente |

> I valori sono indicativi e ricavati dalla pagina [Explore the context window](https://code.claude.com/docs/en/context-window) della documentazione Claude Code. Variano per sessione, modello, configurazione. Per misurare i tuoi reali, usa `/context`.

Tre punti che vale la pena fissare:

**1. I `CLAUDE.md` vengono caricati per intero ogni sessione.** Non ci sono caching o indici: tutto il contenuto entra nel contesto. Anthropic raccomanda di tenere ogni `CLAUDE.md` sotto le **200 righe**: oltre, sia perché il modello ha più difficoltà a seguirne tutte le istruzioni, sia perché consumi token inutilmente. Se ti ritrovi con un `CLAUDE.md` di 400 righe, probabilmente ci stai mettendo cose che dovrebbero stare in skill, documentazione di progetto, o `CLAUDE.local.md`.

**2. Le skill installate occupano contesto anche se non triggerate.** È il punto più sottostimato. Ogni skill attiva contribuisce al contesto con la propria **descrizione** (necessaria per permettere al modello di decidere se invocarla). Il contenuto completo della skill viene caricato solo quando triggerata, ma la descrizione è sempre lì. Un utente che ha 50 skill installate "perché non si sa mai" parte con un budget di contesto significativamente più ridotto rispetto a chi ne ha 10 ben scelte. **Installa solo le skill che effettivamente usi**: per le altre, valuta `disable-model-invocation: true` nel frontmatter (rimuove anche la descrizione dal contesto).

**3. I tool results sono la categoria che esplode.** Leggere 30 file PHP per cercare un pattern può facilmente significare 50.000+ token di tool results. Un `npm run build` con output verboso, ancora di più. È qui che si gioca la maggior parte della saturazione, ed è qui che i subagent (vedi 9.6) fanno la differenza maggiore.

### 8.3 Segnali di contesto saturo

Quando il contesto si avvicina al limite, il modello inizia a comportarsi in modo riconoscibile:

- **"Dimentica" cose dette prima** — risposte che ignorano una decisione presa due turni fa, o ripetono spiegazioni già date
- **Risposte più lente** — più token da elaborare = più tempo di risposta
- **Errori "stupidi"** che prima non faceva — usa la convenzione sbagliata, riferisce un nome di file inesistente, propone codice incoerente con il resto del progetto
- **Warning nella status line** se l'hai configurata con indicatore di contesto

> **Cosa NON fare quando vedi questi segnali.** Continuare a "spiegare di nuovo" è la reazione istintiva, ed è esattamente quella sbagliata: ogni nuova spiegazione gonfia ulteriormente il contesto. Allo stesso modo, ripetere il prompt più dettagliato non aiuta — peggiora. Il rimedio è strutturale, non linguistico: usa `/context`, leggi cosa pesa, agisci con `/compact` o `/clear`. Vedi 9.4 e 9.5.

### 8.4 Il comando `/context`: leggere ed agire

`/context` è il modo più diretto per **vedere quanto contesto stai consumando** prima che il problema diventi visibile dal comportamento del modello. Lanciato in qualsiasi momento, mostra:

- la **percentuale di contesto utilizzata** sul totale disponibile
- la **suddivisione per categoria**: system prompt, CLAUDE.md, skill, conversazione, file letti, output dei tool

Esempio di lettura:

```
/context

Context usage: 42% (84.000 / 200.000 token)

  System prompt:           ~4.200 token
  Environment + MCP:         ~400 token
  CLAUDE.md (3 livelli):   ~2.800 token
  Skills (8 attive):       ~3.100 token
  MEMORY.md:                 ~680 token
  Conversation:           ~18.000 token
  Tool results:           ~54.800 token
```

#### Lettura strategica per categoria

La parte utile è capire **dove sta il peso**, perché determina la cura giusta:

- **Tool results gonfio (>50% del totale)** → hai letto molti file o eseguito comandi verbosi. Soluzione: `/compact` riassume mantenendo decisioni e file chiave, butta via il rumore.
- **Conversation gonfia** → hai mescolato troppi task nella stessa sessione, o ti sei trascinato dietro chiarimenti vecchi non più rilevanti. Soluzione: valuta `/clear` se sei a un cambio di task.
- **System + CLAUDE.md + Skill alti** → la "tara" della sessione è troppo pesante. Non si risolve con `/compact` o `/clear`: è strutturale. Devi rivedere quante skill hai attive, quanto sono lunghi i tuoi `CLAUDE.md`, se Auto Memory ha accumulato troppo in `MEMORY.md`.

#### Soglie indicative

> **Nota sui numeri che seguono.** Le percentuali in questa tabella sono empiriche: riflettono pratica comune e l'esperienza dell'autore in sessioni reali con codebase PHP/JS di taglia media. Anthropic non pubblica soglie ufficiali oltre alla genericità di "context rot": prendi questi valori come punto di partenza, non come linea guida prescrittiva. Se lavori su monorepo da 1M+ token, su task sintetici, o con una pipeline molto particolare, le tue soglie utili saranno diverse.

- **Sotto il 50%** — rilassato, lavora normalmente.
- **50-75%** — inizia a valutare: chiudi il task in corso e poi `/compact` prima di aprirne uno nuovo.
- **Oltre il 75%** — è il momento di intervenire: `/compact` se vuoi conservare il filo, `/clear` se stai cambiando completamente argomento. Sopra l'85% considera anche di passare a un modello con finestra 1M (vedi 9.7) se il task lo giustifica.

#### Quando lanciarlo

`/context` è particolarmente utile in tre momenti:

- **Prima di un task pesante** — se stai per chiedere un Plan Mode su un'area grossa o un audit di molti file, sapere che parti dal 70% ti evita di scoprire a metà che il modello inizia a dimenticare.
- **Quando senti il modello "rallentare"** — prima di concludere che "Claude oggi è stupido", controlla il contesto. Spesso è solo saturo.
- **A sessione lunga, di routine** — anche senza segnali, lanciarlo ogni 30-40 minuti ti dà controllo proattivo invece di reattivo.

### 8.5 Compressione: `/compact` e `/clear`

Sono i due strumenti principali di compressione. Differenza importante:

- **`/compact`** comprime la conversazione in un sommario, mantenendo decisioni e contesto chiave. **Continui a lavorare con il filo del discorso**, ma con molti meno token. Ideale a metà sessione quando hai chiuso una fase e ne stai aprendo un'altra correlata.

  Sintassi opzionale per dare un focus al sommario:

  ```
  /compact mantenendo le decisioni architetturali del refactor auth
           e il pattern adottato per il rate limiting
  ```

  Senza istruzioni, Claude decide cosa è importante. Con istruzioni, gli dici tu su cosa concentrarsi e cosa può buttare via senza rimpianti.

- **`/clear`** azzera completamente il contesto. **Sessione fresca**, ma `CLAUDE.md`, skill, system prompt e Auto Memory restano (sono di sistema, non parte della conversazione). Usa quando cambi completamente task e non ti serve nulla del precedente.

Esempio di flusso tipico:

```
[Inizio mattina]
> Refactor del modulo auth per usare JWT
[2 ore di lavoro, /context dice 78%]

/compact mantenendo decisione di JWT con refresh token rotation

[Apertura nuova fase]
> Ora aggiungi i test unitari sul nuovo modulo auth

[Pomeriggio, task completamente diverso]
/clear

> Aggiorna la documentazione API per riflettere il cambio di endpoint
```

### 8.6 Subagent: la strategia strutturale

`/compact` e `/clear` sono **rimedi reattivi**: agisci quando il contesto è già pieno. I subagent sono lo strumento **preventivo**: lavorano in modo che il main agent non si gonfi mai per cose che non gli servono.

La documentazione Anthropic lo dichiara esplicitamente: i subagent permettono di *"preservare il contesto mantenendo esplorazione e implementazione fuori dalla conversazione principale"*. Il meccanismo, già visto in dettaglio nella [sezione 12](#subagent-orchestrare-lavoro-specializzato), è semplice:

- Il main agent **delega** un task specifico a un subagent (built-in come `Explore`, oppure custom).
- Il subagent gira nel suo **context window separato**, con tool e istruzioni dedicati.
- Quando ha finito, restituisce al main agent **solo un sommario** del risultato — non i 30 file letti, non l'output di build da 80 KB, solo il distillato.

Tre casi in cui il pattern paga di più:

- **Ricerca di pattern in molti file**. *"Trova tutte le funzioni PHP che non hanno nonce verification nel plugin"* — fatto dal main agent significa leggere ~50 file e tenerli in contesto per sempre. Delegato a un subagent significa ricevere un sommario di 7 funzioni vulnerabili con riga e file, e basta.
- **Audit massivi**. Code review automatica su un intero plugin: tre subagent paralleli (sicurezza, performance, stile) producono tre sommari indipendenti, il main agent li aggrega senza vedere il dettaglio dei singoli file letti.
- **Esplorazione di un'area sconosciuta**. Prima di iniziare un refactor, *"capisci come è strutturato il modulo notifiche"* dato a un `Explore` subagent restituisce un sommario architetturale — 1.500 token — anziché 60.000 token di file di codice nel main context.

Una buona euristica: **se ti accorgi di aver letto 30 file solo per produrre 200 token di output, era un subagent**.

### 8.7 Modelli con finestra 1M token: quando passarci

Per la maggior parte dei task, 200K token sono più che sufficienti. Esistono però scenari in cui il salto a 1M cambia qualitativamente cosa si può fare. La cosa importante: nei piani API e nei piani Pro/Max abilitati, **non costa di più per token** — il pricing è identico tra 200K e 1M, paghi solo i token che usi.

#### Sintassi di attivazione

Tre modi documentati ufficialmente:

```bash
# Durante una sessione
/model sonnet[1m]
/model opus[1m]
/model claude-opus-4-7[1m]

# All'avvio dal terminale
claude --model "sonnet[1m]"
claude --model "opus[1m]"

# Variabile d'ambiente (default per ogni nuova sessione)
ANTHROPIC_DEFAULT_SONNET_MODEL=claude-sonnet-4-6[1m]
ANTHROPIC_DEFAULT_OPUS_MODEL=claude-opus-4-7[1m]
```

Il suffisso `[1m]` è la sintassi ufficiale e appare nel picker `/model` quando il modello supporta 1M.

#### Modelli con 1M nativo (aprile 2026)

| Modello | Finestra | Note |
|---|---|---|
| `claude-opus-4-7` | 200K / 1M | Stable, default |
| `claude-opus-4-6` | 200K / 1M | Stable |
| `claude-sonnet-4-6` | 200K / 1M | Stable |

> **Stato attuale (verificato 30 aprile 2026 sulla [docs ufficiale](https://platform.claude.com/docs/en/build-with-claude/context-windows))**: la finestra 1M è disponibile su Opus 4.7, Opus 4.6 e Sonnet 4.6. Sonnet 4.5 ha context 200K, e Sonnet 4 risulta esplicitamente *deprecated*. La beta 1M che era disponibile su Sonnet 4 / 4.5 è stata ritirata: chi avesse pipeline che la richiedono deve migrare a Sonnet 4.6 o Opus 4.6/4.7. Per lo stato sempre aggiornato, fare riferimento alla [tabella modelli ufficiale](https://platform.claude.com/docs/en/about-claude/models/overview).

#### Quando ha senso passare a 1M

Scenari concreti:

- **Audit di un plugin con oltre 80 file PHP** dove serve tenere insieme buona parte del codice per ragionare su pattern incrociati (es. tutti i punti dove si accede al database, mappati in una sola passata).
- **Confronto strutturato tra due branch grandi** prima di un merge complesso.
- **Migrazione cross-modulo** dove le decisioni in un'area dipendono da come lavorano altre 5-6 aree del codebase.
- **Documentazione legacy estesa** che vuoi tenere completa nel contesto per generare una guida nuova coerente con tutto.

#### Quando NON serve

- **Task focalizzati su pochi file** (3-10): 200K bastano e avanzano.
- **Debug puntuali** o fix di un bug isolato.
- **Refactor incrementale** dove lavori una funzione alla volta.
- **Sessioni esplorative** dove cambi spesso direzione: meglio un `/clear` ogni tanto che una finestra mostre da gestire.

Anche con 1M, il [context rot](#cosè-il-contesto-e-perché-conta) resta. Non è una scusa per "buttarci dentro tutto": è uno strumento per scenari dove davvero serve ampiezza, da usare con la stessa disciplina dei 200K.

### 8.8 Regola pratica e mentalità

> Se ti accorgi di aver fatto tre cose diverse nella stessa sessione, probabilmente avresti dovuto usare `/clear` due volte.

Sessioni focalizzate producono output migliori e consumano meno token. Il principio sotto a tutto: il contesto è **una risorsa scarsa, non una pattumiera**. Ogni cosa che ci entra deve guadagnarsi il posto.

#### Strumenti di gestione del contesto: dove sono nella guida

La gestione del contesto attraversa tutta la guida, non vive solo qui. Ecco dove approfondire:

- **Modello giusto per il task** — [sezione 5](#plan-mode-pensare-prima-di-scrivere) (`opusplan`, scelta del modello)
- **`CLAUDE.md` ben dimensionato** — [sezione 7](#memoria-persistente-claude.md-e-auto-memory) (sotto le 200 righe)
- **Auto Memory non gonfia** — [sezione 7](#memoria-persistente-claude.md-e-auto-memory) (`MEMORY.md` come indice, topic file on-demand)
- **Skill solo quelle che servono** — [sezione 10](#skill-il-meccanismo-di-estensione)
- **Subagent come strategia strutturale** — [sezione 12](#subagent-orchestrare-lavoro-specializzato)
- **Hook per ridurre rumore in sessione** — [sezione 13](#hook-automatizzare-il-lifecycle-di-claude-code) (es. filtri su tool output)

### 8.9 Scegliere l'architettura giusta: tabella decisionale

I cinque meccanismi di estensione di Claude Code (`CLAUDE.md`, Auto Memory, Skill, Subagent, Hook) si sovrappongono nei casi d'uso e generano facilmente la domanda *"quale uso per cosa?"*. Le decisioni progettuali si intrecciano: una convenzione di codice va in `CLAUDE.md` o in una skill? Un'automazione va in un hook o in un custom slash command? Un'esplorazione di un'area sconosciuta va fatta dal main agent o delegata a un subagent? La tabella seguente è la mappa unificata.

| Strumento | Caso d'uso tipico | Costo contesto | Quando usarlo | Limite |
|-----------|-------------------|----------------|----------------|--------|
| **`CLAUDE.md`** | Convenzioni, stack, regole invalicabili che valgono per **ogni sessione di un progetto** (linguaggio, framework, struttura cartelle, comandi build, anti-pattern da evitare). | **Alto**: caricato per intero ogni sessione. Tieni il file < 200 righe. | Hai regole stabili che il modello deve sempre conoscere prima di iniziare a lavorare. | Non si adatta a preferenze cross-progetto né ad apprendimenti dinamici (per quelli, Auto Memory). |
| **Auto Memory** | Apprendimenti che attraversano sessioni e progetti: preferenze utente, correzioni che il modello deve ricordare, decisioni architetturali stabili. | **Basso**: solo `MEMORY.md` (indice, max ~6.5K token) viene caricato; i topic file sono on-demand. | Vuoi che Claude *impari nel tempo* da come lavori, senza che tu debba ripetere le stesse istruzioni a ogni nuova sessione. | Non è un repository di documentazione: solo regole/preferenze concise. Se cresce oltre 200 righe va potato. |
| **Skill** | Playbook codificato e riusabile (procedura, framework di analisi, pattern di scrittura) invocabile da qualunque sessione che la abbia attiva. | **Medio**: ~1% finestra per descrizione (sempre presente), contenuto pieno solo se invocata. | Una procedura ricorrente che vorresti distribuire o standardizzare (`/security-review`, `/simplify`, una skill aziendale di code style). | La somma delle descrizioni di molte skill installate erode il contesto: 10 skill mirate > 50 "non si sa mai". |
| **Subagent** | Task read-heavy che gonfierebbe il main context: audit, esplorazione di codebase, ricerca pattern in molti file, analisi comparative. | **Quasi zero sul main**: il subagent gira in finestra separata, restituisce solo il sommario. Il vero risparmio strutturale di token. | Stai per leggere 20+ file per produrre un output sintetico, oppure vuoi parallelizzare 3 audit indipendenti. | Latenza maggiore (è un'altra chiamata), niente stato condiviso tra subagent e main, sommario può perdere dettagli. |
| **Hook** | Automazione deterministica su eventi del lifecycle (`PreToolUse`, `PostToolUse`, `UserPromptSubmit`, ecc.): formattazione, validazione, log, blocchi di sicurezza. | **Zero o negativo**: spesso un hook *riduce* il contesto filtrando l'output rumoroso prima che arrivi al modello. | Vuoi che qualcosa accada **sempre** in risposta a un evento, indipendentemente dalla decisione del modello (es. `prettier` dopo ogni `Edit`, blocco shell su pattern pericolosi). | È deterministico, non semantico: non "capisce", esegue. Non sostituisce un subagent o una skill quando serve giudizio del modello. |

**Come leggere la tabella decisionale.** Il punto non è scegliere "il migliore in assoluto" ma quello che sta nel posto giusto della catena. Tre principi pratici:

- **`CLAUDE.md` è la base**, non un'ambizione: se la regola non vale per ogni sessione del progetto, non ci va.
- **Skill e subagent** lavorano insieme: spesso una skill orchestra un subagent (es. `/security-review` delega a un subagent `Explore` per la lettura massiva, poi compone il report).
- **Hook è laterale**: non sostituisce nessuno degli altri quattro, li *integra* a costo zero quando serve azione automatica e prevedibile.

Quando ti accorgi di star ripetendo la stessa istruzione a tre sessioni di seguito, hai un candidato per `CLAUDE.md` o Auto Memory. Quando ti accorgi di star leggendo decine di file per produrre un sommario, hai un candidato per un subagent. Quando ti accorgi di voler garantire che qualcosa *succeda comunque*, hai un candidato per un hook.

---


---

> ← [7. Memoria persistente](07-memoria.md) | [Index](README.md) | [9. Sicurezza e permessi](09-sicurezza.md) →
