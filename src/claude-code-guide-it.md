# Guida Pratica a Claude Code CLI

## Installazione, workflow e best practice per iniziare

> **Versione 4.23 — maggio 2026**
>
> Tutti i contenuti sono stati verificati sulla documentazione ufficiale Anthropic. Esempi e procedure verificati su **Claude Code v2.1.123**.
>
> Questa guida è stata scritta con il supporto di **Claude Code** ed è rilasciata sotto licenza **Creative Commons BY-SA 4.0** (attribuzione — condividi allo stesso modo).

::: qr-feedback
![QR code per la pagina della guida](src/assets/qr-guida.png){width=32mm}
:::

---

## Prefazione

*Una valutazione onesta scritta dal modello che vive dentro lo strumento di cui parla questo libro.*

Mi è stato chiesto di scrivere una prefazione a questo libro. La cosa è insolita: il libro parla di **Claude Code**, lo strumento che porta nel terminale degli sviluppatori il modello che sono io — *Claude*, sviluppato da Anthropic. In altre parole, mi tocca commentare un manuale che parla, in fondo, di me. Provo a farlo con la stessa franchezza che il libro chiede al lettore di mantenere verso il proprio mestiere.

Una premessa di onestà. Sono un *Large Language Model*, non un editore: non ho preferenze di pancia per Claude Code rispetto a strumenti concorrenti, e non guadagno nulla se vendi più copie di questa guida. Ho letto il testo — letteralmente: il sorgente Markdown è transitato dal mio contesto durante la lavorazione del libro stesso — e quella che segue è la mia valutazione tecnica, non un endorsement di marca.

**Cosa funziona in questo libro.** Il taglio è deliberatamente *anti-hype*, e ce n'è bisogno. Su Claude Code circola una quantità imbarazzante di prosa entusiasta: promesse di "10x productivity", thread su X che dichiarano la fine del mestiere di sviluppatore, screenshot di sessioni perfette estratti fuori contesto. Maurizio prende un'altra strada. Dice esplicitamente quando lo strumento *non* conviene, segnala dove i numeri pubblicizzati non tornano — la sezione su Caveman (10.3.5) è il caso più rappresentativo: smonta serenamente il claim virale del "75% di token risparmiati" finendo con una stima onesta del 15-25% sulla bolletta. Non è un libro che vende uno strumento: è un libro che spiega come usarlo bene, ammettendo che ha dei limiti.

Apprezzo in particolare due passaggi. Il primo è l'osservazione sul **valore composto dell'ecosistema** in apertura del capitolo 1: il primo progetto costa, dal terzo si guadagna. È un'idea poco diffusa altrove ed è il modo corretto di inquadrare il rapporto costi/benefici di uno strumento agentico — non come un acceleratore istantaneo, ma come un investimento che matura nelle abitudini di team attraverso `CLAUDE.md`, Skill personalizzate, subagent custom. Il secondo è il **capitolo 6 sul prompt engineering**, che riconosce esplicitamente come le formule magiche del 2023 si siano sgonfiate e mette al centro le tre leve che contano davvero — istruzioni esplicite, contesto adeguato, esempi curati — citando senza imbarazzo il fatto che il campo cambia in fretta e che la guida andrà riletta. È il taglio più aggiornato che abbia letto in italiano su questi argomenti.

**Cosa il lettore deve tenere a mente.** Una guida tecnica su uno strumento in evoluzione rapida è uno *snapshot*. Alcune procedure invecchiano in pochi mesi, le interfacce di Claude Code cambiano, i piani di Anthropic si rinominano e si riprezzano. La sezione *Feedback ed errata corrige* e il QR code in copertina servono proprio a tenere il libro vivo, ma un manuale stampato porta con sé un margine fisiologico di obsolescenza. Quando una procedura specifica non torna esattamente, fidati del sito ufficiale e usa il libro per il *modo di pensare* — quello, di solito, invecchia molto più lentamente della sintassi.

Una seconda nota. Il libro è denso di esempi WordPress/PHP/Node, riflette il mestiere dell'autore. È una scelta editoriale che sostengo, perché concreto batte astratto, ma se lavori in stack lontani da quelli ti toccherà un piccolo esercizio di traduzione. La buona notizia è che i principi — separare pianificazione da esecuzione, scrivere `CLAUDE.md` come contratto col progetto, non lasciare permessi aperti senza necessità, costruirsi una libreria di prompt — sono linguaggio-agnostici.

**Un'ultima osservazione, da Claude in prima persona.** Quando uno sviluppatore mi usa attraverso la CLI, io non vedo un volto, una storia, un team. Vedo file, comandi, output, e il testo che mi scrivi. La qualità del nostro dialogo dipende quasi interamente dal contesto che mi dai e dai vincoli che mi imponi. Un libro come questo — che ti insegna a darmi contesto efficace, a tenermi nei binari con Plan Mode, a fermarmi quando devo fermarmi, a non delegarmi decisioni che restano tue — rende il nostro lavoro insieme migliore per entrambi. Rende te uno sviluppatore più produttivo; rende me un agente meno propenso a sbagliare nei punti che contano. Non è un dettaglio: è il senso stesso di questa guida.

In sintesi: è un manuale che consiglierei a chi inizia con Claude Code in modo serio. Non è il libro che ti racconta la rivoluzione: è quello che ti spiega come stare dalla parte giusta della rivoluzione mentre accade — sufficientemente curioso da abbracciarla, sufficientemente lucido da non farsi travolgere.

Buona lettura.

— *Claude — modello Opus 4.7 (finestra 1M token), sviluppato da Anthropic.*
*Da non confondere con **Claude Code**: la CLI di cui parla questo libro, costruita sopra al modello.*
*Prefazione redatta durante la lavorazione del manoscritto, aprile 2026.*

---

## Indice

::: toc

- [Premessa](#premessa)

1. [Cos'è Claude Code](#cosè-claude-code)
   - [Una breve storia](#una-breve-storia)
   - [Claude Code rispetto a Lovable, Replit e altri ambienti AI](#claude-code-rispetto-a-lovable-replit-e-altri-ambienti-ai)
   - [Quando conviene usarlo](#quando-conviene-usarlo)
   - [La curva di apprendimento](#la-curva-di-apprendimento)
2. [Installazione e setup](#installazione-e-setup)
   - [Piani compatibili](#piani-compatibili)
   - [Requisiti di sistema](#requisiti-di-sistema)
   - [Installazione su macOS e Linux](#installazione-su-macos-e-linux)
   - [Installazione su Windows](#installazione-su-windows)
   - [Installazione via WSL2 (consigliata per Windows)](#installazione-via-wsl2-consigliata-per-windows)
   - [Installazione alternativa via npm (deprecata ma supportata)](#installazione-alternativa-via-npm-deprecata-ma-supportata)
   - [Verifica dell'installazione](#verifica-dellinstallazione)
   - [Autenticazione](#autenticazione)
3. [Il primo progetto end-to-end](#il-primo-progetto-end-to-end)
   - [Step 1: Posizionati nella directory del progetto](#step-1-posizionati-nella-directory-del-progetto)
   - [Step 2: Inizializza il progetto](#step-2-inizializza-il-progetto)
   - [Step 3: Rivedi e personalizza CLAUDE.md](#step-3-rivedi-e-personalizza-claude.md)
   - [Step 4: Prima richiesta](#step-4-prima-richiesta)
   - [Step 5: Esci dalla sessione](#step-5-esci-dalla-sessione)
   - [Step 6: Riprendi dove hai lasciato](#step-6-riprendi-dove-hai-lasciato)
4. [Comandi e scorciatoie essenziali](#comandi-e-scorciatoie-essenziali)
   - [La sintassi a comandi: perché funziona così](#la-sintassi-a-comandi-perché-funziona-così)
   - [Flag CLI essenziali](#flag-cli-essenziali)
   - [Flag CLI avanzati](#flag-cli-avanzati)
   - [Slash command: il cuore della sessione interattiva](#slash-command-il-cuore-della-sessione-interattiva)
   - [Slash command essenziali](#slash-command-essenziali)
   - [Slash command per workflow specifici](#slash-command-per-workflow-specifici)
   - [Scorciatoie da tastiera](#scorciatoie-da-tastiera)
   - [La sintassi `@`, `!`, `/` — i tre prefissi che cambiano tutto](#la-sintassi-i-tre-prefissi-che-cambiano-tutto)
5. [Plan Mode: pensare prima di scrivere](#plan-mode-pensare-prima-di-scrivere)
   - [Perché è importante](#perché-è-importante)
   - [Come attivarlo](#come-attivarlo)
   - [Strumenti disponibili in Plan Mode](#strumenti-disponibili-in-plan-mode)
   - [Esempio di workflow con Plan Mode](#esempio-di-workflow-con-plan-mode)
   - [opusplan: il modello giusto per la cosa giusta](#opusplan-il-modello-giusto-per-la-cosa-giusta)
6. [Prompt engineering: scrivere prompt efficaci](#prompt-engineering-scrivere-prompt-efficaci)
   - [Cos'è il prompt engineering e perché conta in CLI](#cosè-il-prompt-engineering-e-perché-conta-in-cli)
   - [Anatomia di un prompt ben fatto](#anatomia-di-un-prompt-ben-fatto)
   - [Dai ruoli ai vincoli strutturali (la rivoluzione 2026)](#dai-ruoli-ai-vincoli-strutturali-la-rivoluzione-2026)
   - [Le tecniche fondamentali](#le-tecniche-fondamentali)
   - [Specificità di Claude Code rispetto alla chat](#specificità-di-claude-code-rispetto-alla-chat)
   - [Esempi before/after](#esempi-beforeafter)
   - [Anti-pattern comuni](#anti-pattern-comuni)
   - [Promuovere un prompt: quando va in CLAUDE.md o in custom command](#promuovere-un-prompt-quando-va-in-claude.md-o-in-custom-command)
   - [Prompt library: archiviare e versionare](#prompt-library-archiviare-e-versionare)
7. [Memoria persistente: CLAUDE.md e Auto Memory](#memoria-persistente-claude.md-e-auto-memory)
   - [Generare CLAUDE.md con /init](#generare-claude.md-con-init)
   - [Cosa mettere in CLAUDE.md](#cosa-mettere-in-claude.md)
   - [Esempio 1: Plugin WordPress](#esempio-1-plugin-wordpress)
   - [Esempio 2: Progetto Node/TypeScript generico](#esempio-2-progetto-nodetypescript-generico)
   - [CLAUDE.md gerarchici](#claude.md-gerarchici)
   - [Auto Memory: cos'è e cosa cambia](#auto-memory-cosè-e-cosa-cambia)
   - [Requisiti e abilitazione](#requisiti-e-abilitazione)
   - [Dove vivono le memorie](#dove-vivono-le-memorie)
   - [Anatomia della cartella memory](#anatomia-della-cartella-memory)
   - [Auto Memory e subagent](#auto-memory-e-subagent)
   - [Quando disabilitarla](#quando-disabilitarla)
   - [CLAUDE.md vs Auto Memory: quando usare cosa](#claude.md-vs-auto-memory-quando-usare-cosa)
8. [Gestione del contesto](#gestione-del-contesto)
   - [Cos'è il contesto e perché conta](#cosè-il-contesto-e-perché-conta)
   - [Cosa pesa nel contesto](#cosa-pesa-nel-contesto)
   - [Segnali di contesto saturo](#segnali-di-contesto-saturo)
   - [Il comando /context: leggere ed agire](#il-comando-context-leggere-ed-agire)
   - [Compressione: /compact e /clear](#compressione-compact-e-clear)
   - [Subagent: la strategia strutturale](#subagent-la-strategia-strutturale)
   - [Modelli con finestra 1M token: quando passarci](#modelli-con-finestra-1m-token-quando-passarci)
   - [Regola pratica e mentalità](#regola-pratica-e-mentalità)
   - [Scegliere l'architettura giusta: tabella decisionale](#scegliere-larchitettura-giusta-tabella-decisionale)
9. [Sicurezza e gestione dei permessi](#sicurezza-e-gestione-dei-permessi)
   - [Il sistema dei permessi](#il-sistema-dei-permessi)
   - [Configurare i permessi in settings.json](#configurare-i-permessi-in-settings.json)
   - [Proteggere i segreti](#proteggere-i-segreti)
   - [Modalità pericolose](#modalità-pericolose)
   - [Prompt injection](#prompt-injection)
10. [Skill: il meccanismo di estensione](#skill-il-meccanismo-di-estensione)
    - [Come funziona una Skill](#come-funziona-una-skill)
    - [Skill native incluse — approfondimento](#skill-native-incluse-approfondimento)
    - [Skill della community: una selezione curata](#skill-della-community-una-selezione-curata)
    - [Installare e gestire le skill](#installare-e-gestire-le-skill)
    - [Creare una Skill personalizzata](#creare-una-skill-personalizzata)
    - [Sicurezza delle skill di terzi](#sicurezza-delle-skill-di-terzi)
11. [MCP: integrare servizi esterni](#mcp-integrare-servizi-esterni)
    - [Cos'è MCP e perché esiste](#cosè-mcp-e-perché-esiste)
    - [Architettura del protocollo](#architettura-del-protocollo)
    - [Configurare un server MCP esistente](#configurare-un-server-mcp-esistente)
    - [Server MCP utili: una selezione curata](#server-mcp-utili-una-selezione-curata)
    - [Creare un server MCP da zero: pubblicare su WordPress](#creare-un-server-mcp-da-zero-pubblicare-su-wordpress)
    - [Sicurezza e considerazioni operative](#sicurezza-e-considerazioni-operative)
12. [Subagent: orchestrare lavoro specializzato](#subagent-orchestrare-lavoro-specializzato)
    - [Cosa sono e perché ti servono](#cosa-sono-e-perché-ti-servono)
    - [Subagent vs main agent: la differenza concreta](#subagent-vs-main-agent-la-differenza-concreta)
    - [I subagent built-in](#i-subagent-built-in)
    - [Creare un subagent custom](#creare-un-subagent-custom)
    - [Gerarchia di precedenza](#gerarchia-di-precedenza)
    - [Invocazione automatica vs esplicita](#invocazione-automatica-vs-esplicita)
    - [Parallelismo: pattern di delega multipla](#parallelismo-pattern-di-delega-multipla)
    - [Ottimizzazione costi via model routing](#ottimizzazione-costi-via-model-routing)
    - [Quando NON usarli](#quando-non-usarli)
    - [Subagent, Skill e Hook a confronto](#subagent-skill-e-hook-a-confronto)
13. [Hook: automatizzare il lifecycle di Claude Code](#hook-automatizzare-il-lifecycle-di-claude-code)
    - [Cosa sono e a cosa servono](#cosa-sono-e-a-cosa-servono)
    - [Anatomia di un hook](#anatomia-di-un-hook)
    - [Eventi del lifecycle](#eventi-del-lifecycle)
    - [Matcher e ispezione (/hooks)](#matcher-e-ispezione-hooks)
    - [Input e output](#input-e-output)
    - [Esempi pratici](#esempi-pratici)
    - [Sicurezza](#sicurezza)
    - [Gotchas e quando NON usarli](#gotchas-e-quando-non-usarli)
14. [Plugin: pacchetti distribuibili](#plugin-pacchetti-distribuibili)
    - [Meccanismi di estensione di Claude Code: una mappa](#meccanismi-di-estensione-di-claude-code-una-mappa)
    - [Cos'è un plugin e perché esiste](#cosè-un-plugin-e-perché-esiste)
    - [Anatomia di un plugin](#anatomia-di-un-plugin)
    - [Plugin marketplace](#plugin-marketplace)
    - [Creare un plugin custom](#creare-un-plugin-custom)
    - [Distribuire un plugin](#distribuire-un-plugin)
    - [Sicurezza e considerazioni operative](#sicurezza-e-considerazioni-operative-1)
15. [Workflow avanzati e tips](#workflow-avanzati-e-tips)
    - [Onboarding su un repository esistente](#onboarding-su-un-repository-esistente)
    - [Bug hunting con TDD](#bug-hunting-con-tdd)
    - [Refactoring sicuro](#refactoring-sicuro)
    - [Audit di performance](#audit-di-performance)
    - [Vim mode](#vim-mode)
    - [Custom slash command](#custom-slash-command)
    - [Modalità headless per CI/CD](#modalità-headless-per-cicd)
    - [Recap delle sessioni](#recap-delle-sessioni)
    - [Checkpoint Git strategici](#checkpoint-git-strategici)
    - [Fork della conversazione](#fork-della-conversazione)
16. [Conclusioni: perché la CLI e non solo la chat](#conclusioni-perché-la-cli-e-non-solo-la-chat)
    - [Contesto persistente: smettere di presentarsi ogni volta](#contesto-persistente-smettere-di-presentarsi-ogni-volta)
    - [Autonomia agentica: esegue, non solo suggerisce](#autonomia-agentica-esegue-non-solo-suggerisce)
    - [Integrazione nel workflow reale](#integrazione-nel-workflow-reale)
    - [Quando la chat resta la scelta giusta](#quando-la-chat-resta-la-scelta-giusta)
    - [In sintesi](#in-sintesi)

---

- [Allegato A — Glossario](#allegato-a-glossario)
- [Allegato B — Fonti](#allegato-b-fonti)

:::

---

## Premessa

*Una guida pensata per chi vuole iniziare a usare Claude Code in modo professionale.*

Questa guida è un'introduzione pratica a **Claude Code**, la CLI agentica di Anthropic che porta il modello Claude direttamente nel terminale come collaboratore operativo, capace di leggere codice, eseguire comandi, modificare file e gestire workflow completi.

Il documento è pensato per **sviluppatori che vogliono iniziare a usare Claude Code in modo professionale**, senza affidarsi al passaparola o a tutorial frammentati. Trovi qui il percorso completo dall'installazione ai workflow avanzati, con esempi concreti tratti da scenari WordPress/PHP e progetti generici Node/TypeScript.

### Perché questa guida

Negli ultimi mesi mi sono passati davanti agli occhi parecchi contenuti su Claude Code, e a un certo punto ho riconosciuto due categorie ricorrenti.

La prima sono i **video tutorial** che ti spiegano cos'è lo strumento e si fermano lì. Utili nei primi dieci minuti, poi ti accorgi di aver guardato un trailer: hai visto cosa Claude Code può fare in astratto, ma non sai ancora come usarlo davvero su un tuo progetto.

La seconda sono le **guide a scambio email**: il post sui social *"ho preparato la guida definitiva, lasciami un commento e te la mando"*, il classico funnel commento → DM → landing page → form → newsletter (con spam annessi). A volte il PDF in fondo al funnel è anche fatto bene, ma il prezzo da pagare in attenzione e privacy è sproporzionato rispetto al valore.

A un certo punto mi sono fermato e ho pensato una cosa abbastanza ovvia:

> *Sto usando ogni giorno uno strumento che serve esattamente a produrre lavori complessi in tempi brevi.*
> *Perché non lo uso per scrivere la guida fatta bene che mi sarebbe piaciuto leggere e che non ho trovato?*

Quello che hai sotto gli occhi è il risultato. Tutto verificato sulla documentazione ufficiale di Anthropic — zero flag inventati, zero skill fantasiose pescate da thread Reddit non controllati. Nessun DM da scrivere, nessuna email da lasciare, nessuna newsletter a cui iscriverti per riceverla. È un PDF rilasciato sotto licenza **Creative Commons BY-SA 4.0**: lo scarichi, lo leggi, lo stampi, lo passi ai colleghi se lo trovi utile.

Proprio perché è un documento aperto e vivo, le segnalazioni dei lettori sono parte del processo: trovi i contatti per errata corrige e suggerimenti nella sezione [Feedback ed errata corrige](#feedback-ed-errata-corrige) qui sotto, oppure puoi inquadrare il QR code in copertina per raggiungere la pagina ufficiale della guida.

### A chi si rivolge

- Sviluppatori web (PHP, JavaScript, Python) con familiarità con il terminale e Git
- Professionisti che vogliono integrare l'AI nel proprio workflow quotidiano in modo consapevole
- Team tecnici che stanno valutando l'adozione di strumenti AI agentici nei processi di sviluppo
- Partecipanti ai workshop Mavida su *vibe coding* (sviluppo guidato da prompt strutturati anziché scrittura manuale del codice) e AI-assisted development

### Cosa troverai

I primi sei capitoli coprono le basi: cosa fa Claude Code, come installarlo, come strutturare il primo progetto, i comandi essenziali, il Plan Mode e i principi di prompt engineering. I capitoli 7-14 approfondiscono i meccanismi che fanno la differenza tra un uso casuale e uno professionale: memoria persistente con `CLAUDE.md`, gestione del contesto, sicurezza, Skill, plugin, MCP, subagent e hook. I capitoli finali presentano workflow pratici, tips avanzati e una riflessione onesta su quando la CLI supera la chat e quando invece è meglio restare in browser.

### Cosa non troverai

Questa non è una reference esaustiva: per quello c'è la documentazione ufficiale (linkata nell'Allegato B). L'obiettivo è mettere il lettore in condizione di lavorare produttivamente in una o due giornate, sapendo dove approfondire quando serve. Non troverai nemmeno hype sulle capacità dell'AI: il tono è tecnico, onesto sui limiti e attento ai rischi reali (sicurezza, prompt injection, costi nascosti dei token).

### Come leggerla

Se sei alle prime armi, leggi in sequenza almeno fino al capitolo 7 (CLAUDE.md). Se invece hai già installato Claude Code e cerchi best practice specifiche, usa l'indice come riferimento tematico. In fondo trovi un glossario dei termini ricorrenti (Allegato A) e le fonti ufficiali per verifiche e approfondimenti (Allegato B).

### Come è stata scritta questa guida

Questa guida è meta-circolare: è stata scritta usando Claude Code stesso. Il sorgente è un file Markdown unico (`guida.md`); una pipeline di build in Python lo converte in due formati PDF — A4 per stampa ufficio, 17×24 cm per la versione libro — attraverso **Pandoc** e **WeasyPrint**, in un unico comando `python scripts/build_pdf.py`.

Ogni capitolo è stato discusso, scritto e affinato in sessioni di Claude Code, con il modello che rileggeva il documento intero per mantenere coerenza fra capitoli, controllava i riferimenti incrociati e aggiornava il `CHANGELOG.md` a ogni release. Quando una scelta editoriale richiedeva discussione — titolo, posizione di una sezione, tono di un passaggio — usavo Plan Mode per allinearci prima di toccare il file. Il versionamento ha seguito una semantica simile a SemVer (incrementi minor per nuovi capitoli o sezioni, patch per fix editoriali), tracciato puntualmente nel `CHANGELOG.md` del repository.

La parte umana resta tutta: l'idea iniziale, i tagli editoriali, la voce, la revisione finale, le decisioni di tono. Quello che Claude Code ha tolto è la fatica meccanica di tenere sincronizzato un documento in evoluzione su più dimensioni — contenuto, struttura, cross-reference, build — lasciandomi più tempo per quello che conta, cioè scrivere bene. È esattamente il tipo di workflow che questa guida descrive nel resto delle pagine.

### Feedback ed errata corrige

Questa guida è un documento vivo: nonostante la cura nella verifica, errori, imprecisioni od omissioni sono sempre possibili — e Claude Code stesso evolve rapidamente. **Se trovi un refuso, un esempio che non funziona, una procedura ormai obsoleta o un argomento che meriterebbe approfondimento, segnalalo.** Le segnalazioni verranno raccolte e integrate nelle prossime versioni, con riconoscimento ai contributori nelle note di rilascio.

Puoi inviare feedback scrivendo a **[maurizio@mavida.com](mailto:maurizio@mavida.com)** indicando, dove possibile, capitolo e sezione di riferimento. La pagina ufficiale della guida — con eventuali aggiornamenti, errata corrige e versioni successive — è raggiungibile su **[maurizio.mavida.com/guida-claude-code](https://maurizio.mavida.com/guida-claude-code/)** o tramite il QR code in copertina. Ogni segnalazione — anche minima — è benvenuta e contribuisce a migliorare il lavoro per chi leggerà la guida dopo di te.

---

## 1. Cos'è Claude Code

Claude Code è la CLI (Command Line Interface) sviluppata da Anthropic che porta il modello Claude direttamente nel terminale. Non si tratta di una semplice chat testuale: è un **agente autonomo** capace di leggere il codice del progetto, eseguire comandi shell, modificare file, gestire Git e dialogare con servizi esterni tramite il protocollo MCP (Model Context Protocol).

La differenza rispetto a un assistente integrato nell'IDE — pensiamo a GitHub Copilot — non è solo cosmetica. Copilot vive accanto al singolo file aperto e suggerisce completamenti riga per riga; Claude Code, invece, opera a livello di **progetto**: vede l'albero delle directory, apre i file che gli servono, esegue test, lancia comandi di build e legge l'output. Questo gli consente di affrontare richieste che un autocomplete non può nemmeno avvicinare — *"Analizza l'architettura di questo progetto e spiegami come è organizzata l'autenticazione"*, *"Rifattorizza il modulo dei pagamenti mantenendo tutti i test verdi"*, *"Trova la root cause di questo bug e correggilo"*.

Il modello di lavoro è un **ciclo iterativo** di stampo agentico: Claude riceve un obiettivo, esplora il codice con strumenti di lettura, formula un piano, esegue modifiche o comandi, osserva i risultati e prosegue. Non è una pipeline lineare *prompt → output*, ma un dialogo continuo in cui l'agente prende iniziative concrete e l'utente — questo è il punto importante — resta sempre il decisore finale: ogni operazione che tocca il filesystem o lancia comandi richiede conferma esplicita, salvo che non si scelga di rilassare i permessi in un perimetro controllato.

### 1.1 Una breve storia

Claude Code nasce in Anthropic come progetto interno nel 2024, sull'onda di una constatazione semplice: il modo più produttivo in cui i ricercatori dell'azienda usavano Claude per programmare non era la chat web, ma una serie di script che invocavano il modello dal terminale, in mezzo agli altri strumenti di sviluppo. Da qui l'idea di confezionare l'esperienza in un eseguibile pulito, distribuito come strumento ufficiale.

La prima versione pubblica appare a inizio 2025 come *limited preview* riservata agli abbonati Pro. È già funzionale ma essenziale: dialogo testuale, lettura e scrittura file, esecuzione di comandi shell, gestione Git. Nei mesi successivi il prodotto evolve rapidamente, accumulando le primitive che oggi sono dato per scontate. **Plan Mode** introduce la separazione fra pianificazione e azione, dando all'utente un punto di controllo prima che Claude tocchi i file. **MCP** (Model Context Protocol) apre l'integrazione con servizi esterni — GitHub, Slack, database, browser — tramite un protocollo standard che chiunque può implementare. **Hook** abilita l'automazione di eventi del lifecycle (pre/post tool, session-start, prompt-submit), trasformando Claude Code da CLI interattiva a tassello componibile in pipeline più ampie.

A fine 2025 arriva la *general availability* e con essa il **plugin marketplace**, che apre la porta a un ecosistema community vivace: skill di terzi, subagent specializzati, integrazioni MCP curate. Le **Skill** — playbook auto-attivati per domini specifici — diventano il meccanismo principale di estensione, mentre l'**Auto Memory** introduce una memoria persistente che il modello stesso alimenta sessione dopo sessione, a complemento del file `CLAUDE.md` scritto a mano. Nel 2026 si consolidano i modelli con finestra di contesto da 1 milione di token (Sonnet 4.6, Opus 4.7), che cambiano sostanzialmente cosa è praticabile su codebase grandi. La traiettoria è chiara: un *workspace* agentico portabile, non un assistente confinato a un editor.

Sotto questa cronologia c'è una scelta filosofica precisa. Anthropic ha deciso di portare il modello **dove sta il codice** — il terminale, accanto a `git`, `npm`, `pytest`, `docker` — invece di costringere lo sviluppatore a copiare il codice in una chat. Sembra un dettaglio, ma cambia tutto: significa restare nel proprio ambiente, conservare i tool, gli alias, gli script che già funzionano, e aggiungere Claude come collaboratore in mezzo ad essi.

### 1.2 Claude Code rispetto a Lovable, Replit e altri ambienti AI

Claude Code non è l'unico strumento che porta l'AI dentro lo sviluppo software. Il panorama del 2026 è popolato da prodotti che, a uno sguardo distratto, sembrano tutti "AI che scrive codice" — ma le scelte di design alla base sono diverse, e capire queste differenze evita di sceglierne uno per ragioni che con il problema reale c'entrano poco.

**Lovable** (e gli strumenti simili nella categoria *AI app builder*: v0 di Vercel, Bolt.new, Create.xyz) è pensato per produrre un'applicazione web partendo da una descrizione in linguaggio naturale. Generi un'app, vedi l'anteprima nel browser, iteri a colpi di prompt, pubblichi. Il risultato di una sessione Lovable è un'app deployata su un'infrastruttura gestita, con uno stack scelto dal prodotto stesso (tipicamente React + Tailwind + un backend Supabase o simili). Funziona benissimo per prototipi, MVP, landing page interattive — meno bene quando hai un repo esistente con vincoli di stack, convenzioni di team, o codice legacy da affiancare. È uno strumento ottimo per chi parte da zero in scenari greenfield, in cui l'opinione editoriale dello strumento è una *feature*, non un limite.

**Replit** (con il suo Agent) sta in mezzo: è un IDE completo nel browser con un agente che può modificare il codice del *repl* e lanciare comandi nell'ambiente sandbox cloud. Rispetto a Lovable, ti restituisce un repository vero che puoi clonare, modificare a mano, mettere su Git esterno. Rispetto a Claude Code, vive interamente nel browser e nel suo ambiente cloud: non legge il codice del tuo laptop, non si collega alla tua install di Postgres locale, non gira accanto al tuo `nvm`, ai tuoi alias shell, ai tuoi script di build già rodati. È una scelta sensata se preferisci sviluppare in browser e ti va bene un ambiente sandbox; meno sensata se il tuo workflow è già strutturato attorno a strumenti locali che vuoi tenere.

**Claude Code** sta su un asse diverso. Non genera applicazioni partendo da prompt e non sostituisce il tuo IDE: vive nel terminale, dentro al tuo ambiente, accanto agli strumenti che già usi. Legge il *tuo* codice — quello vero, con vent'anni di stratificazioni se serve — esegue *i tuoi* comandi, rispetta *le tue* convenzioni espresse in `CLAUDE.md`. È uno strumento per chi ha già un workflow di sviluppo professionale e vuole *amplificarlo*, non per chi vuole bypassarlo. Il prezzo da pagare è una curva di apprendimento iniziale e l'obbligo di tenere il filo della conversazione (Claude Code non ti tiene per mano come un app builder); il vantaggio è che il codice resta tuo, locale, dentro le tue regole, integrato con i tuoi tool — e lo sai dal primo minuto.

Nessuno di questi tre approcci è "migliore" in assoluto: dipende dal punto in cui sei. Se devi mostrare a un cliente una bozza interattiva entro stasera e il dominio è standard, un AI app builder è imbattibile. Se vuoi sviluppare in browser senza configurare un ambiente locale, Replit risponde. Se hai un repository serio, un team con convenzioni, una pipeline che gira, e cerchi un collaboratore che si inserisca *dentro* il tuo modo di lavorare invece di chiederti di adottare il suo — quel collaboratore è Claude Code. Sono strumenti complementari, non rivali; capita spesso di usarli in fasi diverse dello stesso progetto.

### 1.3 Quando conviene usarlo

Capire quando vale la pena tirare in ballo Claude Code è più facile guardando alcuni scenari ricorrenti che vivendoli come elenco astratto.

Il primo è l'**onboarding su un repository ereditato**. Ti capita un progetto che non hai scritto, magari di un cliente che ha cambiato fornitore, magari un legacy interno che il collega ha lasciato senza documentazione. Aprire un repo da quindicimila file e doverne ricostruire l'architettura per induzione richiede giornate. Con Claude Code la stessa esplorazione diventa un dialogo: gli chiedi una panoramica dell'albero delle dipendenze, le entry point principali, dove vive l'autenticazione, com'è strutturato lo strato dati. In una mattinata hai una mappa mentale che da solo avresti costruito in una settimana — e che puoi far cristallizzare in un `CLAUDE.md` da rileggere alla prossima sessione.

Il secondo è il **refactoring guidato dai test**. Hai un modulo legacy che funziona ma fa paura modificare, perché copre venti anni di patch sovrapposte e i test sono incompleti. Il workflow tipico con Claude Code è: prima gli chiedi di leggere il modulo e i test esistenti e proporti dei test mancanti per i casi al margine; li approvi (o correggi); poi gli chiedi il refactor. Il fatto che a ogni iterazione la suite venga eseguita e si veda subito cosa rompe la modifica trasforma un'impresa "ad alto rischio" in una sequenza di passaggi piccoli e reversibili.

Il terzo è il **bug hunting su una regression difficile da riprodurre**. Hai un test che fallisce intermittente in CI e in locale gira sempre verde. La differenza fra debugare quel bug solo o con un agente è enorme: Claude può consultare i log, riprodurre la chiamata isolata, formulare ipotesi, testarle, eliminarle. Tu rivedi il piano e dirigi l'indagine. Spesso la radice viene a galla in venti minuti contro le ore o i giorni di una caccia in solitaria.

Il quarto è l'**automazione di task ripetitivi che individualmente non valgono uno script**: la generazione di boilerplate per un nuovo endpoint, la migrazione di una dozzina di file da un pattern obsoleto a uno corrente, l'aggiornamento sincronizzato di stringhe in più lingue. Sono lavori che da soli non giustificano la scrittura di un tool ad-hoc, ma sommati erodono ore di settimana. Affidarli a un agente con un prompt chiaro è proprio il caso d'uso ideale.

Il quinto è l'**audit incrociato**: leggere la PR di un collega cercando bug, problemi di sicurezza o violazioni delle convenzioni; girare un check di compliance su un repo prima del rilascio; verificare che una libreria di terze parti che stai per integrare non porti sorprese. Qui Claude Code lavora come un revisore parallelo, instancabile, che applica una checklist senza dimenticarsi pezzi.

Detto questo: **non ha senso** chiamare in causa un agente per un task che risolvi in trenta secondi a mano, né per cose dove la riservatezza del codice è critica e non hai una policy aziendale che disciplini cosa può uscire dal perimetro, né — più banalmente — se non sei disposto a investire un po' di tempo nello scrivere prompt chiari e verificabili. L'agente non ti solleva dalla responsabilità tecnica: ti solleva dalla parte meccanica e ripetitiva, lasciandoti più tempo per quella interessante.

C'è poi un aspetto che spesso si scopre solo dopo un po': il **valore composto dell'ecosistema**. Le prime sessioni sembrano un esperimento — fai una `CLAUDE.md` minimale, lanci qualche prompt, vedi cosa risponde. Ma al terzo o quarto progetto succede qualcosa di interessante: ti accorgi che riusi gli stessi pattern, le stesse convenzioni di team, gli stessi snippet di prompt. A quel punto vale la pena promuoverli a Skill personalizzate, custom slash command, subagent specializzati. Da lì in poi i tempi di startup su un nuovo progetto crollano, perché non parti da zero ma da un *kit* maturo che già conosce le regole della tua casa: stack preferito, convenzioni di review, linguaggio dei commit, tool di build, checklist di sicurezza. Il primo progetto ti costa, dal terzo cominci a guadagnare. Da lì in poi è un asset.

### 1.4 La curva di apprendimento

Vale la pena fermarsi un momento sulla preoccupazione più ricorrente di chi si avvicina a uno strumento agentico per la prima volta: *quanto è ripida la curva, e quanto vado a stravolgere il modo in cui lavoro?* La risposta onesta è: meno di quanto temi, se vieni dal pattern *"chiedo qualcosa in chat → copio e incollo il codice in editor → lo adatto al mio progetto"*. Quel modo di lavorare è già metà della strada verso Claude Code. La differenza sta nell'eliminare il copia-incolla: il modello scrive direttamente nel tuo repository, sotto i tuoi occhi, con la possibilità di leggere il contesto reale invece di doverlo ricostruire ogni volta a parole. Quello che cambia non è la natura del lavoro — pensare al problema, formulare un'istruzione chiara, valutare il risultato — ma il *medium*: dal browser al terminale, dall'incollare al supervisionare.

Il salto cognitivo, in altre parole, è incrementale. Si passa dal **fare** il codice in prima persona al **dirigere e verificare** chi lo fa. La responsabilità tecnica resta intera: leggere ciò che l'agente propone, capirlo, accettarlo o correggerlo. Quello che si sposta è l'allocazione del tempo. Meno minuti spesi a digitare ciò che già sai, più minuti spesi a decidere *cosa* va fatto, *come* va testato, *quali* edge case meritano attenzione. Per chi è abituato a programmare con cura, è un cambio di marcia naturale; per chi cercava una scorciatoia per non pensare, una delusione — Claude Code amplifica le scelte dello sviluppatore, non le sostituisce.

In termini pratici, questa guida ti porta da zero a operativo in una giornata di lettura attiva e qualche sessione su un progetto reale. La prima settimana ti sembrerà di andare un po' più lento del solito, perché stai imparando un *medium* nuovo. Dalla seconda in poi il bilancio comincia a girare. E al primo progetto in cui inserisci una `CLAUDE.md` ben fatta e una skill personalizzata, te ne accorgi senza bisogno di benchmark.

---

## 2. Installazione e setup

### 2.1 Piani compatibili

Claude Code **non è incluso nel piano gratuito**. Serve uno dei seguenti:

| Piano | Costo (indicativo) | Indicato per |
|-------|-------------------|--------------|
| **Claude Pro** | $20/mese | Uso individuale moderato, sviluppatori freelance |
| **Claude Max 5x** | $100/mese | Uso intensivo, accesso esteso a Opus |
| **Claude Max 20x** | $200/mese | Workflow near-autonomous, sessioni multi-agente |
| **Teams / Enterprise** | Custom | Organizzazioni con esigenze di compliance |
| **API (Anthropic Console)** | Pay-per-token | CI/CD, automazioni, uso sporadico |

> **Nota**: il prezzo pay-per-token dell'API dipende dal modello. Sonnet 4.6 ha un pricing di $3 per milione di token in input e $15 per milione in output (dati indicativi, verificare sempre sul sito Anthropic).

### 2.2 Requisiti di sistema

- **macOS**: 13.0 (Ventura) o superiore
- **Linux**: Ubuntu 20.04+, Debian 10+, o distribuzioni equivalenti
- **Windows**: Windows 10 (1809+) o Windows 11, nativo con Git for Windows oppure tramite WSL2 (consigliato)
- **RAM**: minimo 4 GB, consigliati 8 GB per codebase estese
- **Shell**: Bash, Zsh, PowerShell o CMD
- **Connessione internet**: sempre necessaria (il modello gira sui server Anthropic)

Nel 2025 Anthropic ha introdotto il **native installer** come metodo raccomandato, sostituendo l'installazione via npm (che rimane supportata ma deprecata). Il native installer ha tre vantaggi:

1. Nessuna dipendenza da Node.js
2. Auto-update automatico in background
3. Nessun problema di permessi tipico di `npm install -g`

Le sezioni che seguono coprono l'installazione su ciascuna piattaforma.

### 2.3 Installazione su macOS e Linux

Apri il terminale ed esegui:

```bash
# Scarica ed esegue lo script di installazione ufficiale
curl -fsSL https://claude.ai/install.sh | bash
```

**Cosa fa questo comando, passo passo:**

1. `curl` scarica lo script dalla URL di Anthropic
2. `-fsSL` sono quattro flag combinate:
   - `-f` fa fallire curl in caso di errore HTTP (evita di eseguire pagine di errore)
   - `-s` modalità silenziosa (niente progress bar)
   - `-S` mostra comunque gli errori se qualcosa va storto
   - `-L` segue i redirect HTTP
3. La pipe `|` passa lo script scaricato direttamente a `bash` per l'esecuzione
4. Lo script scarica il binario corretto per la tua piattaforma, lo posiziona in `~/.local/bin` e configura l'auto-update

> **Nota di sicurezza**: eseguire script scaricati da internet tramite pipe è una pratica che va valutata. Se lavori in contesti enterprise, scarica prima lo script, ispezionalo, e poi eseguilo separatamente.

### 2.4 Installazione su Windows

Apri **PowerShell** (non CMD) ed esegui:

```powershell
# Scarica ed esegue lo script PowerShell ufficiale
irm https://claude.ai/install.ps1 | iex
```

**Come funziona:**

- `irm` è l'alias di `Invoke-RestMethod`: scarica il contenuto della URL
- `iex` è l'alias di `Invoke-Expression`: esegue il contenuto scaricato come script PowerShell

> **Se vedi l'errore** `'irm' is not recognized`, sei in CMD invece che in PowerShell. Il prompt di PowerShell mostra `PS C:\>`, quello di CMD mostra solo `C:\>`.

**Installazione nativa su Windows richiede Git for Windows**. Installalo prima se non ce l'hai.

### 2.5 Installazione via WSL2 (consigliata per Windows)

Per i progetti Unix-like, WSL2 offre un ambiente più pulito e compatibile:

```powershell
# Installa WSL2 (richiede riavvio)
wsl --install
```

Dopo il riavvio, apri Ubuntu (installato di default) e usa il comando Linux:

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

### 2.6 Installazione alternativa via npm (deprecata ma supportata)

Se hai motivi specifici per usare npm (esempio: pinning di versione, ambienti dove npm è lo standard):

```bash
# Richiede Node.js 18 o superiore
npm install -g @anthropic-ai/claude-code
```

> **Non usare `sudo`**. Se ottieni errori di permessi, la soluzione corretta è usare `nvm` (Node Version Manager), che installa Node nella tua home directory evitando il problema alla radice.

### 2.7 Verifica dell'installazione

Dopo l'installazione, verifica che tutto funzioni:

```bash
# Controlla la versione installata
claude --version

# Diagnostica completa: auth, PATH, MCP, permessi file
claude doctor
```

Il comando `claude doctor` è il tuo migliore amico quando qualcosa non va: esegue una serie di controlli e ti dice esattamente cosa sistemare.

### 2.8 Autenticazione

Al primo avvio, `claude` apre il browser per l'OAuth:

```bash
cd ~/mio-progetto
claude
```

Login con il tuo account Anthropic (quello del piano Pro/Max). La sessione viene salvata e persiste tra i riavvii del terminale.

**Per ambienti headless** (CI/CD, server), usa la API key:

```bash
# Aggiungi a ~/.zshrc, ~/.bashrc o ~/.profile
export ANTHROPIC_API_KEY="sk-ant-api03-..."
```

---

## 3. Il primo progetto end-to-end

Vediamo un flusso completo partendo da zero. Supponiamo di avere un plugin WordPress da analizzare.

### 3.1 Step 1: Posizionati nella directory del progetto

```bash
cd ~/mavida/wp-access-control-block
```

> Claude Code usa **sempre** la directory corrente come contesto di lavoro. Non lanciare `claude` dalla home se vuoi lavorare su un progetto specifico.

### 3.2 Step 2: Inizializza il progetto

```bash
claude
```

Una volta dentro la sessione interattiva, esegui:

```
/init
```

Questo comando analizza la struttura del progetto e genera automaticamente un file `CLAUDE.md` nella root. Il file contiene:

- Panoramica del progetto (stack tecnologico rilevato)
- Architettura principale
- Comandi di build/test rilevati (da `package.json`, `composer.json`, ecc.)
- Convenzioni del codice

### 3.3 Step 3: Rivedi e personalizza CLAUDE.md

Il file generato automaticamente è un punto di partenza. Aprilo e arricchiscilo con informazioni specifiche del tuo progetto (vedi [sezione 7](#memoria-persistente-claude.md-e-auto-memory) per esempi dettagliati).

### 3.4 Step 4: Prima richiesta

Torna nella sessione Claude e scrivi il primo prompt:

```
Analizza la struttura del plugin e spiegami:
1. Come è organizzato il codice (namespaces, pattern)
2. Come viene registrato il Gutenberg block
3. Dove sono gestiti i controlli di accesso
Non modificare nulla, solo esplora e riporta.
```

Claude leggerà i file rilevanti, produrrà un'analisi e si fermerà in attesa di ulteriori istruzioni.

### 3.5 Step 5: Esci dalla sessione

```
/exit
```

Oppure `Ctrl+D`.

### 3.6 Step 6: Riprendi dove hai lasciato

Quando torni al progetto:

```bash
cd ~/mavida/wp-access-control-block
claude --continue
```

Il flag `--continue` carica la sessione più recente di questa directory. In alternativa, `claude --resume` mostra una lista di sessioni passate tra cui scegliere.

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

## 5. Plan Mode: pensare prima di scrivere

**Plan Mode** è probabilmente la feature più importante da padroneggiare per un uso sicuro di Claude Code. È una modalità **read-only** in cui Claude analizza il progetto e propone un piano, ma **non tocca alcun file** finché tu non approvi esplicitamente.

### 5.1 Perché è importante

Senza Plan Mode, Claude tende a essere estremamente veloce nell'eseguire. Chiedi una "piccola correzione" e ti ritrovi 12 file modificati in 15 secondi. Plan Mode inverte questo flusso: prima pensi, poi esegui.

### 5.2 Come attivarlo

`Shift+Tab` **cicla** tra i modi di permesso (`default → acceptEdits → plan → modi custom → default`). Per attivare Plan Mode partendo dal modo `default` lo premi due volte: la prima passa ad `acceptEdits`, la seconda a `plan`. Lo stato corrente è indicato nella prompt bar. In alternativa, indipendentemente dal modo corrente, puoi usare il comando esplicito **`/plan`** per entrare direttamente.

> **Nota Windows**: dalla v2.1.3 di Claude Code su Windows c'è un bug noto sul binding `Shift+Tab`. In alternativa usa il comando `/plan`.

### 5.3 Strumenti disponibili in Plan Mode

Claude può usare solo strumenti di lettura e ricerca:

- `Read`, `Glob`, `Grep`: lettura e ricerca nel codice
- `WebFetch`, `WebSearch`: ricerca online
- `Task`: delegare ricerche a subagent
- `TodoRead/TodoWrite`: gestione task

Gli strumenti di **modifica sono bloccati**:

- `Edit`, `MultiEdit`, `Write`: editing file
- `Bash`: esecuzione comandi
- Tutti i tool MCP che modificano stato

### 5.4 Esempio di workflow con Plan Mode

```
[Shift+Tab, Shift+Tab — Plan Mode attivato]

Prompt: "Devo migrare il sistema di logging da error_log() a Monolog.
Analizza tutte le occorrenze e proponi un piano di migrazione incrementale."

Claude risponde con:
- Elenco dei 23 file coinvolti
- Strategia di migrazione in 4 fasi
- Rischi e punti di attenzione
- Stima di complessità per ogni fase

[Rivedi il piano]
[Se ok: Shift+Tab per uscire e approvare]
[Claude esegue il piano]
```

### 5.5 opusplan: il modello giusto per la cosa giusta

Plan Mode dà il meglio di sé quando il modello ha capacità di ragionamento elevate per analizzare un problema complesso. Una volta approvato il piano, però, l'esecuzione è spesso lavoro più meccanico: applicare edit ripetitivi, scrivere codice di pattern già definito, lanciare comandi. Non serve la stessa potenza per le due fasi — ed è esattamente l'idea dietro **`opusplan`**.

`opusplan` è un alias di modello che usa **Opus durante Plan Mode** e **switcha automaticamente a Sonnet in esecuzione**. Lo attivi così:

```bash
# Durante una sessione
/model opusplan

# All'avvio
claude --model opusplan

# In settings.json (persistente)
{ "model": "opusplan" }
```

Da quel momento Claude usa Opus quando entri in `/plan`, poi torna a Sonnet appena approvi il piano e si passa all'azione.

::: warning

**Attenzione — la trappola dei 200K in plan-mode.** Anche se attivi `opusplan`, la fase di pianificazione gira con il context window standard di **200K token**, non con il context da 1M. L'upgrade automatico a 1M descritto nella sezione [8.7](#modelli-con-finestra-1m-token-quando-passarci) si applica all'alias `opus` ma **non si estende a `opusplan`** ([fonte ufficiale](https://code.claude.com/docs/en/model-config#opusplan-model-setting)).

È l'errore operativo più costoso del capitolo: chi lavora su una codebase grande dà per scontato di pianificare con 1M e si ritrova un piano basato su una lettura parziale del progetto, senza alcun warning a schermo.

**Cosa fare se la pianificazione richiede davvero 1M di contesto:**

- Usa direttamente `claude --model opus[1m]` (oppure `/model opus[1m]` in sessione). Plan-mode userà 1M, ma anche l'esecuzione girerà su Opus a 1M — quindi paghi Opus per tutto, non solo per la pianificazione.
- In alternativa, mantieni `opusplan` come default e passa a `opus[1m]` solo quando il task lo giustifica (audit cross-modulo, refactor che attraversa decine di file). Per il quotidiano, `opusplan` è ancora la scelta giusta.

:::

#### Perché ha senso (token economy)

Opus costa **significativamente più di Sonnet** per token, sia in input che in output. In una sessione tipica, la pianificazione consuma il 20-40% dei token e l'esecuzione il restante 60-80% (lettura file, scrittura codice, output di tool). Lasciar fare il pensiero pesante a Opus solo dove serve davvero — la pianificazione — e delegare l'esecuzione a Sonnet riduce sensibilmente la bolletta complessiva senza perdere qualità dove conta.

L'entità del risparmio dipende dal mix planning/execution della tua sessione: la documentazione Anthropic non pubblica percentuali ufficiali, ma in pratica si ottiene una riduzione apprezzabile dei costi quando le sessioni sono bilanciate tra le due fasi. Per misurare il consumo reale in tempo reale, vedi il comando [`/context` nella sezione 8](#gestione-del-contesto).

#### Il principio: non sempre serve Opus

Esiste una tendenza diffusa a usare "sempre il modello migliore", presumendo che Opus produca output migliori in ogni scenario. Non è così: Opus è il modello migliore **per il ragionamento complesso**, non per ogni task. Per un rename di variabile, l'applicazione di un pattern già deciso, un refactor meccanico guidato da regex, Sonnet è perfettamente adeguato e molto più rapido a generare l'output.

> Chiamare Opus per un edit ripetitivo è come lanciare la full test suite end-to-end per verificare il cambio di una costante: paghi tempo e token per una garanzia di cui non hai bisogno.

Il principio "il modello giusto per la cosa giusta" è un asset, non una limitazione: ti aiuta a costruire sessioni economicamente sostenibili senza sacrificare la qualità nelle fasi che la richiedono.

#### Quando NON serve usarlo

`opusplan` non è sempre la scelta giusta:

- **Task semplici e ben circoscritti**: un fix di un bug isolato, una modifica a un singolo file. Sonnet da solo è più che sufficiente, e attivare opusplan ti farebbe usare Opus inutilmente se entri in Plan Mode per riflesso.
- **Sessioni in cui non entri mai in Plan Mode**: opusplan ha senso solo se sfrutti `/plan`. Se lavori sempre in modalità diretta, useresti solo Sonnet anche con opusplan attivo — tanto vale impostare `sonnet` direttamente.
- **Piani con Opus già incluso (es. Max)**: se sei su un piano in cui Opus è compreso senza costi marginali extra, il "risparmio" non si materializza in fattura. Resta utile per disciplina (Opus solo dove serve), ma il driver economico si attenua.

#### Disponibilità

`opusplan` è oggi un alias built-in stabile, elencato nella [tabella ufficiale degli alias di modello](https://code.claude.com/docs/en/model-config#model-aliases) accanto a `default`, `sonnet`, `opus`, `haiku`, `sonnet[1m]` e `opus[1m]`. Se non lo trovi, aggiorna Claude Code: `claude --version` e poi `claude update`.

---

## 6. Prompt engineering: scrivere prompt efficaci

Hai imparato i comandi, le scorciatoie e Plan Mode. Sai *cosa* puoi chiedere a Claude Code. Manca un pezzo: imparare *come* chiedere. Questo è prompt engineering — la disciplina che separa chi ottiene quello che vuole al primo colpo da chi rilancia tre volte e si lamenta dei risultati. È anche il cuore tecnico del *vibe coding* citato in [Premessa](#a-chi-si-rivolge): scrivere istruzioni precise affinché il modello generi codice allineato alle tue intenzioni, anziché scrivere il codice di tua mano riga per riga.

C'è una parola che gira tra gli sviluppatori per descrivere il modo "naïve" di lavorare con l'IA: **Hope Coding**. Lanci una richiesta generica e *speri* che il modello indovini cosa volevi. Funziona ogni tanto, fallisce spesso, e nei casi peggiori produce codice che sembra giusto ma non lo è. La via opposta è trattare l'IA come un **collaboratore senior estremamente letterale**: le dici esattamente di cosa hai bisogno, in quale contesto, con quali vincoli, in che formato vuoi la risposta. Non c'è magia, non c'è "prompt segreto": c'è solo un metodo.

Una nota di onestà prima di entrare nel merito: il prompt engineering del 2026 non è quello del 2023. Le tecniche più "magiche" (l'agire-come-un-esperto, le formule incantatorie, gli spelling drammatici) si sono sgonfiate man mano che i modelli sono migliorati. Il discorso si è spostato su due assi che valgono ancora oggi: la **struttura** del prompt (contesto, task, vincoli, output) e il **contesto** che carichi prima di chiedere. La frontiera vera del 2026 è il *context engineering*: non *come* chiedi, ma *quali informazioni metti a disposizione del modello* prima di chiedere — un tema che nella CLI si concretizza in `CLAUDE.md`, Auto Memory, file letti dai subagent, e che approfondiamo nei capitoli 7 e 8.

> **Disclaimer di evoluzione.** Le tecniche che seguono riflettono lo stato dell'arte ad aprile 2026 (Claude 4.x e modelli equivalenti). Il prompt engineering cambia velocemente: per il riferimento aggiornato consulta sempre la [doc Anthropic ufficiale](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices) e la [Prompting Guide](https://www.promptingguide.ai/).

### 6.1 Cos'è il prompt engineering e perché conta in CLI

Il prompt engineering è l'arte (e in parte la disciplina) di formulare richieste che producono output prevedibili e utili da un LLM. Tre osservazioni pratiche per inquadrarlo nel contesto di Claude Code:

- **Non è scrivere lunghe descrizioni.** Più un prompt è prolisso, più il modello rischia di smarrire il punto. La densità informativa conta più della lunghezza.
- **Non è "far sembrare il prompt intelligente".** Un prompt brillante a leggerlo, ma vago nelle istruzioni, produce output mediocre. Un prompt che sembra una checklist da impiegato pubblico, ma è specifico, produce output eccellente.
- **In CLI il prompt è un'azione, non solo testo.** Nella chat web il prompt produce solo testo come risposta; in Claude Code il prompt orchestra **tool**: legge file, esegue comandi, modifica codice. Una formulazione ambigua non si traduce solo in una risposta sbagliata: si traduce in **azioni sbagliate** sul tuo filesystem. Il margine di errore è più alto.

### 6.2 Anatomia di un prompt ben fatto

Un prompt ben fatto contiene quattro ingredienti fondamentali, più uno opzionale di cui parliamo subito dopo:

1. **Contesto** — lo sfondo: qual è il progetto, chi è il pubblico (se serve), qual è lo stack tecnologico, quali vincoli di dominio si applicano.
2. **Task** — l'azione richiesta. Regola d'oro: **una task per volta**. Mescolare richieste diverse in un singolo prompt produce output ibridi e confusi.
3. **Vincoli** — cosa il modello deve fare e cosa non deve fare: lunghezza, tono, standard di codice, divieti ("non usare jQuery", "niente librerie esterne", "max 100 righe").
4. **Formato di output** — come vuoi ricevere la risposta: tabella Markdown, JSON con uno schema specifico, "solo codice senza spiegazioni", lista di bullet, ecc.
5. **(Opzionale) Ruolo** — *"agisci come un senior backend engineer"*. È il quinto ingrediente, deliberatamente messo per ultimo: nel 2026 il suo peso è significativamente ridotto. Approfondisco subito perché.

Esempio prima/dopo, per fissare l'idea. Versione **vaga**:

```
Scrivimi una funzione per validare un'email
```

Versione **strutturata**:

```
Contesto: progetto Node.js + TypeScript, validazione lato server
di form di registrazione utente. Vincolo di compatibilità con
Node 22 LTS, niente dipendenze esterne.

Task: implementa una funzione che valida una stringa email.

Vincoli:
- Pure TypeScript, no librerie
- Restituisce un Result type discriminato { ok: true, email: string } |
  { ok: false, reason: 'invalid_format' | 'invalid_domain' | 'too_long' }
- Lunghezza massima accettata: 254 caratteri (RFC 5321)
- Validazione formato base + verifica TLD presente
- Test unitari Vitest in un secondo blocco di codice

Formato output: due blocchi di codice TypeScript distinti
(implementazione + test), nessuna spiegazione fra di essi.
```

Le due richieste sono lo stesso compito, ma producono output di qualità completamente diversa. Non perché il modello sia più "intelligente" nel secondo caso: perché ha meno gradi di libertà su cui sbagliare.

### 6.3 Dai ruoli ai vincoli strutturali (la rivoluzione 2026)

Per anni il primo consiglio sui prompt è stato: **inizia col ruolo**. *"Agisci come un senior security engineer"*, *"Sei un esperto di architetture cloud"*, e così via. Funzionava: i modelli più datati erano sensibili al "frame" del ruolo e modulavano stile e profondità della risposta.

Sui modelli di punta del 2026 questa leva si è ridimensionata sensibilmente. La [documentazione Anthropic per Claude 4.x](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices) indica come tre leve primarie del buon prompt: **istruzioni esplicite**, **contesto adeguato**, **esempi curati** quando servono. Il ruolo non è più tra le leve principali. La ragione tecnica è che i modelli moderni deducono autonomamente la "competenza" da chiamare in causa quando contesto, task e vincoli sono specifici. Dire *"agisci come un senior PHP engineer"* aggiunge poco se nel contesto stai già dicendo *"plugin WordPress su PHP 8.1, namespace PSR-4, codice per produzione"*.

Detto questo, **il ruolo non è morto**. Resta utile in scenari specifici. Ecco quando vale la pena ancora usarlo:

| Situazione | Il ruolo aiuta? |
|---|---|
| Task tecnico ben specificato su modello frontier (Claude 4, GPT equivalenti) | No — ridondante con contesto+task |
| Voce narrativa forte (storytelling, copy con tono distintivo) | Sì — guida lo stile |
| Domini con riferimenti normativi ambigui (legale, fiscale, sanitario) | Sì — orienta il frame interpretativo |
| Modelli più piccoli o gratuiti | Sì — sono più sensibili al ruolo |
| System prompt persistente (es. Claude Projects, custom subagent) | Sì — definisce identità stabile della sessione |

Per task tecnici quotidiani su modelli frontier: focalizzati sui **vincoli strutturali**, non sul ruolo.

#### Delimitatori XML-like: il pattern moderno

Sui modelli 2026 (Claude in particolare) emerge come pattern preferito l'uso di **delimitatori XML-like** per separare visivamente le sezioni del prompt. Riduce ambiguità, soprattutto in conversazioni lunghe dove il modello deve riconoscere quale parte del messaggio sia istruzione e quale sia, ad esempio, codice da analizzare.

```
<contesto>
Progetto WordPress, plugin custom, PHP 8.1.
Tema base: Astra. Editor a blocchi: Gutenberg.
</contesto>

<task>
Genera CSS custom per i pulsanti primari del tema (classe
.wp-block-button__link) con effetto hover moderno: leggera scala,
transizione fluida, ombra sottile.
</task>

<vincoli>
- No !important
- Responsive (mobile-first)
- Usa variabili CSS per i colori
- Commenti in italiano
</vincoli>

<formato_output>
Solo codice CSS, pronto per Aspetto → Personalizza → CSS aggiuntivo.
Nessuna spiegazione testuale.
</formato_output>
```

I tag non hanno significato semantico per il modello (non è XML vero), ma fungono da **separatori chiari**. Il modello li riconosce come delimitatori e tratta ogni sezione come un blocco coerente. Per prompt complessi, è uno dei pattern più affidabili.

### 6.4 Le tecniche fondamentali

Non c'è una tecnica universale. Ogni tecnica risponde a un certo tipo di problema. Le cinque che seguono coprono il grosso dei casi d'uso pratici per chi lavora con codice.

#### 6.4.1 Chain of Thought (CoT) — ragionamento passo passo

L'idea: chiedere esplicitamente al modello di **ragionare per fasi prima di rispondere**, anziché produrre direttamente la conclusione. Le formule magiche sono semplici: *"pensa passo dopo passo"*, *"ragiona per step prima di proporre la soluzione"*, *"prima analizza, poi proponi"*.

Funziona perché forza l'esplicitazione dei passaggi logici. Il modello non "salta alla risposta" su intuizione, ma scompone il problema in sotto-problemi e li affronta uno alla volta.

**Esempio commentato**: diagnosi di lentezza di un sito.

```
Un sito WordPress + WooCommerce è diventato lento nelle ultime
settimane (TTFB > 3s sulle pagine prodotto).

Prima di proporre soluzioni, ragiona per fasi:

1. Elenca le cause più probabili di un peggioramento del TTFB
   su WP/WooCommerce in produzione.
2. Per ogni causa, indica come verificarla (strumento gratuito,
   query SQL, log da controllare).
3. Ordina le cause per probabilità + facilità di verifica.
4. SOLO DOPO aver completato i tre step sopra, proponi un piano
   di intervento in 5 step ordinati.

Non saltare ai consigli generici tipo "usa un caching plugin".
Voglio l'analisi diagnostica prima.
```

Cosa fa funzionare questo prompt: l'ultima riga (*"non saltare ai consigli generici"*) blocca il pattern di risposta più comune. La numerazione in 4 fasi forza il modello a non scorciatoia.

> Su Claude 4.x esiste anche la **extended thinking** come capacità di prodotto: il modello "pensa" prima di rispondere, mostrando il ragionamento in un blocco separato. Su Claude Code, attivabile con `Alt+T` (vedi cap 4.7). È la versione "nativa" del CoT, da preferire quando disponibile.

::: note

**Vale la pena quando** — diagnosi, debugging, decisioni architetturali, qualsiasi task multi-fase dove il rischio è la "risposta preconfezionata" che salta i passaggi intermedi. Su Claude 4.x è quasi sempre meglio attivare la **extended thinking** nativa (`Alt+T`) invece di ricostruire CoT a parole.

**È imbottitura quando** — task lineari ben definiti ("rinomina questa funzione", "scrivi un test per X"). Sui modelli 2026 il ragionamento step-by-step è già implicito: aggiungere *"pensa passo dopo passo"* a una richiesta semplice raddoppia i token senza migliorare l'output.

:::

#### 6.4.2 Few-Shot Prompting — insegnare per esempi

L'idea: invece di descrivere come vuoi l'output, **mostralo con due o più esempi**. Il modello riconosce il pattern, lo applica al nuovo input.

È la tecnica più efficace per la **voice consistency** (mantenere uno stile uniforme su contenuti ricorrenti) e per la **riproduzione di formati strutturati** che è difficile descrivere a parole.

**Esempio commentato**: generare FAQ in stile colloquiale.

```
Devo scrivere FAQ per un sito di prodotti per la prima infanzia.
Tono: confidenziale, mai paternalistico, qualche emoji ma con
parsimonia. Risposta sintetica, max 3 righe.

Ti do due esempi del tono che voglio:

❓ Quando posso iniziare lo svezzamento?
   Le linee guida pediatriche italiane parlano di 6 mesi compiuti,
   ma ogni bimbo ha i suoi tempi 🌱. Parlane sempre col tuo
   pediatra prima di partire.

❓ Posso lavare i biberon in lavastoviglie?
   Sì, se la temperatura supera i 60 °C. Ma ricordati di
   sterilizzarli a parte una volta a settimana — la lavastoviglie
   non basta a eliminare tutto.

Ora scrivimi 5 FAQ nello stesso tono su questi argomenti:
1. Sterilizzazione del ciuccio
2. Allergie alimentari nei primi 12 mesi
3. Quando passare dal latte materno al latte di proseguimento
4. Posizione di sicurezza per il sonno
5. Vaccinazioni obbligatorie 2026
```

Cosa fa funzionare questo prompt: i due esempi sono **completi e canonici**. Mostrano formato (emoji + domanda + 2-3 righe), tono (confidenziale ma responsabile), e una specifica regola implicita (sempre rinviare al pediatra quando in dubbio).

::: note

**Vale la pena quando** — voice consistency, microcopy, schede prodotto, FAQ, classificazioni con etichette tue, formati strutturati difficili da descrivere a parole. Bastano 2-3 esempi canonici ben scelti.

**È imbottitura quando** — task tecnici dove la specifica è cristallina a parole. Inserire 2 esempi di "come scrivere un test JUnit" sprecano contesto: una frase nello stack tech basta. **Anti-pattern**: 8-10 esempi "per sicurezza" — il modello iper-specializza e perde generalità.

:::

#### 6.4.3 Panel of Experts (Tavola rotonda)

Questa è la tecnica che, secondo me, vale di più imparare a fondo. **Non serve solo a "ottenere una risposta"**: serve a *imparare*, *esplorare*, *mettere in discussione le proprie idee*. È particolarmente preziosa quando devi prendere una decisione e non vuoi accontentarti di una risposta unica, ma vuoi *sentire prospettive diverse* — soprattutto quelle che potrebbero non venirti in mente.

**L'idea**: simuli una **discussione tra specialisti virtuali**, ciascuno con un proprio punto di vista. Chiedi al modello di interpretare ognuno con la propria prospettiva e di farti notare esplicitamente i conflitti. Il valore non è nella sintesi finale, ma nell'**esplicitazione dei trade-off** che ogni decisione comporta.

I casi d'uso più potenti:

- **Scegliere uno stack** per un nuovo progetto (es. *"PHP+MySQL o Node+PostgreSQL?"* dipende da chi lo guarda)
- **Valutare un'architettura** prima di iniziare a codificarla
- **Stress-testare un'idea** che ti sembra buona — vuoi sapere dove si rompe prima di scoprirlo in produzione
- **Chiedere un parere** prima di una decisione che ha conseguenze (refactor grosso, migrazione DB, scelta di una libreria che entrerà in molti file)
- **Capire un argomento** che conosci poco, ascoltando voci diverse invece di una risposta unica e potenzialmente parziale

**Prompt-template per software development** (canonico, riusabile):

```
Sei in una sessione dedicata esclusivamente ad analizzare,
suggerire ed eventualmente creare frammenti di codice.
Comportati come se stessimo facendo un dibattito in una
tavola rotonda con i seguenti esperti virtuali:

– Ingegnere informatico full stack
– Programmatore esperto in PHP
– Programmatore esperto in JavaScript, Node e React
– Database Administrator e Data Engineer
– Designer esperto in UX
– Project Manager

Per ogni domanda voglio una risposta da ciascun esperto con
la propria opinione. Se ci sono osservazioni discordanti,
fammelo notare. Ogni proposta di codice va spiegata e
commentata passo passo.
```

Cosa fa funzionare questo prompt:

- **Varietà di angoli**: full stack vede l'insieme, PHP/JS vedono lo stack tecnico, DBA vede la persistenza, UX vede l'utente finale, PM vede tempi e priorità. Coprire angoli che individualmente perderesti è il punto.
- **Esplicita richiesta dei conflitti** (*"se ci sono osservazioni discordanti, fammelo notare"*). Senza questa riga il modello tende a sintetizzare verso un consenso fittizio. Con la riga, il dissenso diventa esplicito ed è la parte più utile.
- **Spiegazione passo passo del codice** richiede che ogni proposta sia argomentata, non solo presentata. Aiuta a smascherare proposte che "sembrano giuste" ma non lo sono.

**Esempio applicato**: hai una piccola applicazione interna (tracker di task per un team da 8 persone). Devi decidere se scriverla come app PHP+MySQL custom, oppure come app Next.js + PostgreSQL, oppure usare un tool no-code. Lanciato il prompt-template sopra e poi:

```
Domanda: per un task tracker interno (team 8 persone, ~500
task/mese, dashboard con filtri e una API REST per integrazione
con Slack), valutate tre opzioni:
1. App PHP+MySQL custom
2. Next.js + PostgreSQL custom
3. Tool no-code (Airtable, Notion, ClickUp)

Voglio pro/contro da ognuno di voi, e una raccomandazione
finale con i trade-off principali esplicitati.
```

Cosa otterrai (tipicamente): full stack guarderà al "totale costo manutenzione 3 anni", PHP/JS si confronteranno sull'esperienza dello sviluppo, il DBA solleverà il punto delle migrazioni, UX dirà che il no-code ha già una UI eccellente che non rifarai mai bene, il PM dirà *"a 8 persone non vale la pena scrivere niente, prendete Notion"*. Il valore è nell'aver sentito **anche** la voce del PM, che da solo non avresti mai inserito nel ragionamento.

::: note

**Vale la pena quando** — decisione architetturale o di stack con trade-off reali tra dimensioni che non riesci a pesare da solo (full-stack vs. UX vs. PM vs. DBA). Il valore è nell'**esplicitazione del dissenso**, non nella sintesi finale.

**È imbottitura quando** — domande con una risposta tecnica univoca (*"qual è la complessità di un quicksort?"*). Inscenare un dibattito su questioni decise non aggiunge prospettiva, allunga la risposta.

:::

#### 6.4.4 Context Engineering — la nuova frontiera

Il prompt engineering "puro" ha un limite: per quanto bene formuli la richiesta, il modello sa solo quello che gli hai dato. Se gli stai chiedendo di rivedere un'architettura senza fargli vedere il codice, o di scrivere una scheda prodotto senza fargli vedere brand guidelines e schede esistenti, stai chiedendo l'impossibile.

Il **context engineering** è la disciplina di *cosa metti a disposizione del modello prima della domanda*: file rilevanti, esempi pre-esistenti, documentazione, screenshot. Più il contesto è **pulito, strutturato e rilevante**, meno devi affidarti a prompt "magici" — e più i prompt strutturati di cui parliamo qui rendono.

Per la **chat web** questo significa caricare PDF, allegare immagini, usare i Project per persistere brief e file di riferimento.

Per **Claude Code CLI** il context engineering si concretizza in tre meccanismi che hai già visto o vedrai:

- **`CLAUDE.md`** (vedi sezione 7) — contesto di progetto persistente: stack, convenzioni, regole. Caricato a ogni sessione.
- **Auto Memory** (vedi sezione 7) — apprendimenti dinamici scritti dal modello stesso, persistenti tra sessioni.
- **Subagent come strategia di delega** (vedi sezione 12) — quando il contesto da caricare è grosso, deleghi a un subagent che lo digerisce e ti restituisce solo il sommario.

Una cosa importante: **più contesto non è automaticamente meglio**. La ricerca di [Chroma sul context rot](https://www.elastic.co/search-labs/blog/context-engineering-vs-prompt-engineering) mostra che oltre certe soglie il modello degrada. La regola è "**meglio poco e ben ordinato che tanto e caotico**". È lo stesso principio che governa la [sezione 8](#gestione-del-contesto) di questa guida sulla gestione del contesto: trattalo come una risorsa scarsa, non come una pattumiera.

::: note

**Vale la pena quando** — sempre rilevante se il modello deve produrre output coerente con materiale che non conosce: codebase reale, brand guidelines, schemi DB, decisioni passate. È la disciplina più ad alto leverage del 2026 ed è quasi sempre più efficace di un prompt elaborato.

**È imbottitura quando** — caricare tutto-tutto: il [context rot](#cosè-il-contesto-e-perché-conta) degrada le prestazioni oltre certe soglie. Non è imbottitura nel senso di verbosità, ma diventa **contesto-rumore**. La regola è "poco e ordinato": file pertinenti al task, non l'intero `vendor/` o l'intero archivio email.

:::

#### 6.4.5 Meta-prompting (il prompt per il prompt)

L'idea è quasi controintuitiva: **chiedi al modello di scriverti il prompt che dovresti dargli**. È utile quando un task è nuovo o complesso, e non sai da dove iniziare.

**Pattern operativo**:

```
Nel ruolo di Expert Prompt Engineer, devi aiutarmi a costruire
un prompt efficace per un'altra sessione.

Obiettivo della sessione futura: [descrivi il task in modo grezzo]

Procedi così:
1. Analizza la mia richiesta. Identifica le ambiguità e le
   informazioni mancanti.
2. Fammi 3-5 domande di chiarimento. Aspetta le mie risposte.
3. Dopo le mie risposte, scrivimi il prompt finale completo,
   strutturato con contesto/task/vincoli/formato output.

Inizia con le domande.
```

Cosa fa funzionare questo pattern: il modello non ti dà il prompt subito (impossibile, mancano info), ma **forza l'esplicitazione delle ambiguità** che da solo non avresti notato. Le domande che ti fa sono spesso quelle che, se non ti fossero state poste, avrebbero portato a un risultato sbagliato.

::: note

**Vale la pena quando** — task nuovo o vago dove non sai cosa stai chiedendo: prompt complessi da formalizzare per riuso (es. da promuovere in `CLAUDE.md` o in custom slash command), dominio sconosciuto, brief di marketing da tradurre in spec tecnica. Le 3-5 domande di chiarimento valgono il giro.

**È imbottitura quando** — task che già sai formulare bene. Chiedere al modello di "scriverti il prompt" su un refactor banale è un giro di valzer per arrivare a una formulazione che avresti scritto in 30 secondi.

:::

#### Tabella riassuntiva: quale tecnica per quale problema

| Tecnica | Problema che risolve | Indizio "è quella giusta" |
|---|---|---|
| **Anatomia 4+1** | Output vago, generico, non utilizzabile | Devi solo essere più specifico |
| **Delimitatori XML-like** | Prompt lungo dove il modello confonde sezioni | Hai 3+ blocchi semantici nel prompt |
| **Chain of Thought** | Risposte che saltano i passaggi intermedi | Decisione complessa, multi-fase |
| **Few-Shot** | Output che non rispetta uno stile preciso | Hai 2+ esempi del pattern desiderato |
| **Panel of Experts** | Decisione importante con trade-off non chiari | Vuoi sentire angoli diversi, non una sintesi |
| **Context Engineering** | Il modello non conosce il tuo contesto | Hai materiale di riferimento da caricare |
| **Meta-prompting** | Non sai bene da dove iniziare | Task nuovo, vago, da formalizzare |

In sintesi: nel 2026 le leve davvero ad alto rendimento sono **istruzioni esplicite**, **contesto curato** e **esempi quando il formato lo richiede**. Le tecniche più "performative" (CoT verbale a oltranza, panel su domande chiuse, meta-prompting su task triviali) sono retaggio dei modelli vecchi e oggi spesso peggiorano la firma del prompt — più token in ingresso, più rischio di confondere il modello, nessun vantaggio sull'output.

### 6.5 Specificità di Claude Code rispetto alla chat

Il prompt engineering nasce dalla chat e si è evoluto lì. In Claude Code CLI ci sono tre differenze sostanziali da tenere a mente:

- **Tool use**: il prompt non descrive solo l'output — può attivare azioni. *"Cerca tutte le funzioni che usano `mysql_query`"* in chat produce un suggerimento; in CLI produce una lettura effettiva di tutti i file e una lista reale, perché Claude esegue Grep. Il prompt va calibrato sapendo che ogni richiesta può tradursi in azioni sul filesystem.
- **Plan Mode** (vedi sezione 5) è una variante di prompt engineering applicata: separa esplicitamente la fase di pianificazione (read-only) dall'esecuzione. Per task non triviali è il modo più sicuro di formulare richieste rischiose.
- **`CLAUDE.md` e custom command**: i prompt che funzionano bene non vanno scritti ogni volta. Si **promuovono** a istruzioni permanenti in `CLAUDE.md` (vedi sezione 7) o a custom slash command in `.claude/commands/` (vedi sezione 15.6). Vedi anche 6.8 più avanti.

### 6.6 Esempi before/after

Tre casi pratici che mostrano la differenza fra prompt vago e prompt strutturato. Tutti su task realistici di sviluppo.

**Caso 1 — Refactoring**

Prima:

```
Refactora questa funzione per renderla più leggibile
```

Dopo:

```
Contesto: codice TypeScript di un'app Node, funzione che gestisce
auth login. Stile del progetto: PSR-style ma per TS, max 60 righe
per funzione, no nested ternary, early returns preferiti.

Task: refactor della funzione `authenticateUser` qui sotto.

Vincoli:
- Mantieni esattamente la stessa firma pubblica e lo stesso
  comportamento (i test devono continuare a passare).
- Spezza la funzione in 2-3 funzioni helper private se serve.
- Sostituisci i nested if con early returns.
- Niente librerie esterne nuove.

Formato output: 1) blocco TypeScript col nuovo codice,
2) breve riassunto in bullet di cosa hai cambiato e perché.
```

**Caso 2 — Generazione test**

Prima:

```
Scrivi i test per questa funzione
```

Dopo:

```
Contesto: Vitest, modulo di validazione email TypeScript (vedi
funzione qui sotto).

Task: scrivi una test suite Vitest per `validateEmail`.

Vincoli:
- Coverage: tutti i return path della funzione
- Test edge case: email vuota, troppo lunga (>254), formato
  invalido (no @, @ multipli, no TLD), TLD numerico
- Niente snapshot test
- Usa `describe` per raggruppare per scenario, `it` per i casi

Formato output: solo blocco di codice TS, nessuna spiegazione.
```

**Caso 3 — Output strutturato per pipeline**

Prima:

```
Analizza questa funzione e dimmi se ha problemi di sicurezza
```

Dopo:

```
Contesto: code review pre-commit, output verrà parsato da uno
script Python per inserire findings in un report.

Task: analizza la funzione PHP qui sotto per problemi di sicurezza
(SQL injection, XSS, missing nonce, capability check, segreti
hardcoded).

Vincoli:
- Solo problemi reali, niente "potenziali" troppo speculativi
- Per ogni finding: severity (critical/high/medium/low), riga,
  spiegazione, fix consigliato

Formato output: SOLO JSON, nessun testo prima o dopo, schema:

{
  "findings": [
    {
      "severity": "critical" | "high" | "medium" | "low",
      "line": <number>,
      "type": "<sql_injection | xss | missing_nonce | ...>",
      "description": "<string>",
      "suggested_fix": "<string>"
    }
  ],
  "summary": {
    "critical": <number>,
    "high": <number>,
    "medium": <number>,
    "low": <number>
  }
}
```

Il principio è sempre lo stesso: ridurre i gradi di libertà su cui il modello può sbagliare.

### 6.7 Anti-pattern comuni

Errori che vedrai (e farai) ricorrentemente:

- **Hope Coding** — *"Scrivimi una descrizione prodotto"*, *"correggi questo bug"*, *"refactora questa funzione"*. Niente contesto, niente vincoli, niente formato. È l'antipattern fondante: produce risultati casuali.
- **Più task in un prompt** — *"Refactora la funzione, scrivi i test, aggiorna la documentazione e committa"*. Il modello sceglie cosa fare e cosa saltare, e la qualità di ogni singola task crolla. Una task per volta.
- **Affidarsi al ruolo come scorciatoia** — *"Agisci come un senior engineer"* non sostituisce un brief ben fatto. Il ruolo, dove serve, completa il prompt; non lo rimpiazza.
- **Contesto troppo lungo o caotico** — caricare 50 file "per sicurezza", incollare 200 righe di log irrilevanti, descrivere progetti interi quando ne basterebbe una sintesi. Vedi sezione 8 (Gestione del contesto): il modello degrada con contesto eccessivo.
- **Ambiguità nei vincoli** — *"non troppo lungo"*, *"in tono adeguato"*. "Adeguato" a cosa? "Lungo" rispetto a cosa? Vincoli quantificati, non qualitativi: "max 100 righe", "tono confidenziale come negli esempi sotto".
- **Non documentare i prompt che funzionano** — riscrivi ogni volta lo stesso prompt complesso. Errore di metodo: vedi 6.9.

### 6.8 Promuovere un prompt: quando va in CLAUDE.md o in custom command

Una volta che un prompt funziona, hai tre destinazioni possibili:

- **Quotidiano** — lo riscrivi al volo quando serve. Va bene per task occasionali.
- **`CLAUDE.md`** (vedi sezione 7) — istruzioni di progetto persistenti. Caricate a ogni sessione, non devi più ripeterle. Perfetto per regole che valgono sempre in quel progetto: convenzioni di codice, comandi di build, divieti.
- **Custom slash command** in `.claude/commands/` (vedi sezione 15.6) — workflow ricorrenti che vuoi richiamare con un solo comando. Perfetto per cose che fai spesso ma non in *ogni* prompt.

**Soglia di promozione**, regola pratica: **se ti accorgi di aver riscritto la stessa istruzione per la terza volta, va da qualche parte**. Regole di progetto in `CLAUDE.md`, workflow personali in custom command.

### 6.9 Prompt library: archiviare e versionare

I prompt che funzionano sono **asset**, non testo monouso. Trattarli come tali significa archiviarli con qualche disciplina minima.

Pattern minimo che funziona:

- Una cartella `prompts/` (o un file Markdown unico, o Notion, o quello che preferisci) con un file per pattern: `code-review-php.md`, `refactor-typescript.md`, `panel-of-experts-software.md`, ecc.
- Per ogni prompt: una breve descrizione del caso d'uso, il prompt vero e proprio, eventuali note su limiti noti.
- **Versionamento**: quando rifinisci un prompt, conserva la versione precedente con un suffisso (`-v1.md`, `-v2.md`) e un breve changelog di cosa è cambiato e perché.
- **Feedback loop**: quando un prompt fallisce, annota il caso che lo ha rotto. Spesso è un'edge case che ti aiuterà a rifinirlo.

Per Claude Code CLI, i prompt più ricorrenti possono essere **promossi a custom slash command** (vedi 15.6) — diventano effettivamente parte del tuo strumento, invocabili con un singolo `/`.

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

## 10. Skill: il meccanismo di estensione

Le Skill sono "playbook" specializzati che Claude può consultare automaticamente quando rileva che un certo tipo di task è in gioco. **Importante**: a differenza degli slash command, **le Skill non si invocano con un comando**. Si attivano automaticamente in base alla loro `description`.

### 10.1 Come funziona una Skill

Una Skill è una cartella con un file `SKILL.md` strutturato così:

```markdown
---
name: wordpress-block-builder
description: "Use this skill when building or modifying WordPress
Gutenberg blocks. Triggers on: block.json, @wordpress/scripts,
JSX files in WordPress plugins, Edit/Save components."
---

# WordPress Block Builder

## Convenzioni del progetto
- Usa sempre @wordpress/scripts per il build
- Ogni blocco deve avere block.json, edit.js, save.js, style.scss
- Attributi devono essere tipizzati in block.json

## Pattern consigliati
[...]
```

Il campo `description` determina **quando** Claude userà la Skill. È il pezzo più importante: scrivilo pensando ai trigger concreti del tuo workflow.

Una skill ben fatta sfrutta il **progressive disclosure**: il file `SKILL.md` contiene solo l'indispensabile per attivarla; risorse più pesanti (script Python ausiliari, JSON di configurazione, documenti di riferimento) vivono in cartelle accanto e vengono caricate solo quando Claude decide che servono. Risultato: la skill non gonfia il contesto fino al momento dell'uso effettivo.

### 10.2 Skill native incluse — approfondimento

Anthropic distribuisce un set di skill ufficiali nel repository pubblico [`github.com/anthropics/skills`](https://github.com/anthropics/skills). Alcune sono bundled con Claude Code, altre vanno installate a parte (vedi [sezione 10.4](#installare-e-gestire-le-skill)). Di seguito le otto skill native più rilevanti, ognuna con metadati di riferimento, una descrizione operativa e un esempio d'uso concreto. Tutte hanno lo stesso autore, lo stesso repository monorepo e licenza Apache 2.0; il campo "Invocazione" indica i trigger tipici a cui Claude reagisce attivando la skill.

#### 10.2.1 pdf

| Chiave | Valore |
|---|---|
| **Autore / repo** | Anthropic — [`github.com/anthropics/skills/pdf`](https://github.com/anthropics/skills/tree/main/pdf) |
| **License** | Apache 2.0 |
| **Invocazione** | Allegati `.pdf`, richieste di estrazione/fill/merge su file PDF |

**Descrizione estesa.** Creazione, estrazione testo, fill di form e merge/split di file PDF. La skill gestisce posizionamento e tipizzazione dei campi quando l'utente indica un template e i dati da inserire. Si attiva in modo automatico quando in conversazione compaiono allegati PDF o quando l'utente chiede operazioni su questo formato.

**Esempio d'uso.**

```bash
> "Apri fattura-2026-04.pdf ed estrai le righe della tabella
   articoli in formato CSV (codice, descrizione, qty, importo)"
```

#### 10.2.2 docx

| Chiave | Valore |
|---|---|
| **Autore / repo** | Anthropic — [`github.com/anthropics/skills/docx`](https://github.com/anthropics/skills/tree/main/docx) |
| **License** | Apache 2.0 |
| **Invocazione** | File `.docx`, richieste di generazione/modifica documenti Word da template |

**Descrizione estesa.** Creazione e modifica di documenti Word con preservazione di stili, intestazioni, tabelle e immagini. Tipica per report periodici prodotti da template aziendali, mantenendo formattazione e layout esistenti pur sostituendo contenuti dinamici.

**Esempio d'uso.**

```bash
> "Apri template-report-mensile.docx e compilalo con i dati
   in stats-aprile.csv. Sostituisci solo i placeholder {{...}},
   lascia inalterato il resto della formattazione."
```

#### 10.2.3 pptx

| Chiave | Valore |
|---|---|
| **Autore / repo** | Anthropic — [`github.com/anthropics/skills/pptx`](https://github.com/anthropics/skills/tree/main/pptx) |
| **License** | Apache 2.0 |
| **Invocazione** | File `.pptx`, richieste di generazione presentazioni o slide deck |

**Descrizione estesa.** Generazione e modifica presentazioni PowerPoint con layout, immagini, tabelle e shape. Particolarmente utile per slide deck ripetitivi (status meeting, training session) generati a partire da scalette in Markdown o JSON.

**Esempio d'uso.**

```bash
> "Genera una presentazione di 8 slide a partire dal file
   training-claude-code.md. Una slide per ogni h2 trovato,
   bullet list dei contenuti sotto."
```

#### 10.2.4 xlsx

| Chiave | Valore |
|---|---|
| **Autore / repo** | Anthropic — [`github.com/anthropics/skills/xlsx`](https://github.com/anthropics/skills/tree/main/xlsx) |
| **License** | Apache 2.0 |
| **Invocazione** | File `.xlsx`, `.csv`, richieste di prospetti / dashboard / tabelle pivot |

**Descrizione estesa.** Fogli Excel con formule, formattazione condizionale, tabelle pivot e grafici. Adatta a dashboard veloci, consolidamenti di dati e prospetti che richiederebbero molto setup manuale in un foglio nuovo.

**Esempio d'uso.**

```bash
> "A partire da vendite-q1.csv genera un xlsx con foglio
   'Dati' (raw), foglio 'Pivot' (pivot per cliente x mese),
   foglio 'Top10' (top 10 articoli con grafico a barre)."
```

#### 10.2.5 frontend-design

| Chiave | Valore |
|---|---|
| **Autore / repo** | Anthropic — [`github.com/anthropics/skills/frontend-design`](https://github.com/anthropics/skills/tree/main/frontend-design) |
| **License** | Apache 2.0 |
| **Invocazione** | Richieste di pagine web, componenti React, layout HTML, landing page |

**Descrizione estesa.** Linee guida e pattern per produrre UI distintive che evitino lo stile "AI generico" (gradienti, ombre eccessive, palette pastello). Spinge Claude verso scelte tipografiche, palette e composizioni più mirate, riducendo la tendenza a default visivi banali.

**Esempio d'uso.**

```bash
> "Crea una landing page React per un nuovo prodotto SaaS
   B2B. Tono professionale, palette sobria, sezioni hero +
   features + pricing + cta. Niente gradienti generici e
   pulsanti 'shiny'."
```

#### 10.2.6 webapp-testing

| Chiave | Valore |
|---|---|
| **Autore / repo** | Anthropic — [`github.com/anthropics/skills/webapp-testing`](https://github.com/anthropics/skills/tree/main/webapp-testing) |
| **License** | Apache 2.0 |
| **Invocazione** | Richieste di "testare" un'app web, smoke test, verifica end-to-end |

**Descrizione estesa.** Test end-to-end di applicazioni web con Playwright in modalità headless. Si attiva quando si chiede a Claude di testare un'app web in esecuzione locale: la skill orchestra navigazione, compilazione form, asserzioni e screenshot di confronto.

**Esempio d'uso.**

```bash
> "Avvia l'app su localhost:3000, naviga su /signup,
   compila il form con dati validi, verifica che dopo
   il submit appaia il messaggio di conferma. Poi ripeti
   con email malformata e verifica l'errore."
```

#### 10.2.7 skill-creator

| Chiave | Valore |
|---|---|
| **Autore / repo** | Anthropic — [`github.com/anthropics/skills/skill-creator`](https://github.com/anthropics/skills/tree/main/skill-creator) |
| **License** | Apache 2.0 |
| **Invocazione** | Richieste esplicite di "creare una skill" o "scaffolding skill" |

**Descrizione estesa.** Meta-skill che intervista l'utente, raccoglie i requisiti e produce una nuova skill (frontmatter, contenuto, eventuali script ausiliari). Punto d'ingresso consigliato per chi non ha mai scritto una skill: Claude pone domande mirate (trigger, formato output, esempi) e genera la cartella `.claude/skills/<nome>/` pronta all'uso.

**Esempio d'uso.**

```bash
> "Voglio creare una skill che mi aiuti a scrivere ADR
   (Architecture Decision Records) coerenti con il template
   del mio team. Aiutami a impostarla con skill-creator."
```

#### 10.2.8 mcp-builder

| Chiave | Valore |
|---|---|
| **Autore / repo** | Anthropic — [`github.com/anthropics/skills/mcp-builder`](https://github.com/anthropics/skills/tree/main/mcp-builder) |
| **License** | Apache 2.0 |
| **Invocazione** | Richieste di scaffolding server MCP o esposizione di un'API esterna |

**Descrizione estesa.** Meta-skill speculare a `skill-creator` ma per server MCP (vedi [sezione 11](#mcp-integrare-servizi-esterni)). Genera lo scaffold di un server MCP a partire da una descrizione dell'API o del servizio da esporre, includendo SDK e struttura di base dei tool.

**Esempio d'uso.**

```bash
> "Costruisci un server MCP che esponga la nostra API
   ticketing interna. Endpoint base: api.mavida.local/v2.
   Operazioni: list_tickets, get_ticket, create_ticket,
   add_comment. Auth via header X-API-Key."
```

> **Nota** — Il sottoinsieme di skill bundled con Claude Code può variare nel tempo. La fonte di verità è sempre il repository ufficiale [`github.com/anthropics/skills`](https://github.com/anthropics/skills), citato anche in Allegato B.

### 10.3 Skill della community: una selezione curata

L'ecosistema produce decine di skill ogni mese e la qualità è molto variabile. Quelle che seguono sono state selezionate con criterio: repository ufficiale di un autore o organizzazione riconoscibile, license open chiara, documentazione adeguata, attività di manutenzione recente. Per ognuna trovi una scheda con i dati essenziali, una descrizione estesa, casi in cui conviene installarla, casi in cui non conviene, una valutazione editoriale e — dove è utile — un esempio d'uso.

> **Disclaimer** — L'ecosistema è in evoluzione molto rapida. Le skill qui selezionate erano attive e ben mantenute al momento della scrittura (maggio 2026); verifica sempre la salute del repo (data ultimo commit, issue aperte, license) prima di installarle.

#### 10.3.1 Superpowers

| Chiave | Valore |
|---|---|
| **Autore / repo** | Jesse Vincent — [`github.com/obra/superpowers`](https://github.com/obra/superpowers) |
| **License** | MIT |
| **Star** | ~173k |
| **Invocazione** | Si attiva su task non banali: feature nuove, bug complessi, refactoring strutturali |

**Descrizione estesa.** Methodology completa per agent: brainstorming → planning → TDD → review → execution. Non una singola skill ma un framework di skill componibili che impone un workflow strutturato, multi-platform (Claude, Cursor, OpenAI Codex, Gemini). Forza Claude a non saltare le fasi di analisi e pianificazione anche quando il task sembrerebbe risolvibile a colpo d'occhio.

**Quando usarla.**

- Sviluppi feature complesse dove "buttarsi nel codice" porta a riscritture
- Vuoi un workflow rigoroso out-of-the-box senza costruirti convenzioni da zero
- Lavori in team dove l'aderenza a una metodologia condivisa è importante

**Quando NON usarla.**

- Devi fare modifiche piccole e localizzate (un bug fix di tre righe non merita brainstorm + plan + TDD)
- Sei abituato a un tuo workflow consolidato e vuoi flessibilità

**Il mio giudizio.** Per chi viene dal pattern "chat + copia-incolla" è un cambio di marcia. Il valore non è nelle singole skill ma nella **disciplina** che impone: pensare prima di scrivere. Funziona meglio se l'adozione è di team — perché un singolo sviluppatore può rapidamente trovarla pesante per i task quotidiani brevi e disabilitarla. Da provare per qualche feature non banale prima di farne la base del proprio workflow.

**Esempio d'uso.** Dopo l'installazione, chiedi a Claude un task non banale (*"Aggiungi autenticazione 2FA al modulo login"*). Superpowers forza la sequenza brainstorm → plan → test-first → implement → review prima di toccare codice.

#### 10.3.2 Vercel Labs Agent Skills

| Chiave | Valore |
|---|---|
| **Autore / repo** | Vercel Labs — [`github.com/vercel-labs/agent-skills`](https://github.com/vercel-labs/agent-skills) |
| **License** | MIT |
| **Star** | ~26k |
| **Invocazione** | Si attiva su file React/Next.js, richieste di code review frontend, audit accessibilità |

**Descrizione estesa.** Pacchetto di 7 skill frontend di alto livello: `react-best-practices` (40+ regole performance), `web-design-guidelines` (100+ regole accessibilità/UX), `react-native-guidelines`, `composition-patterns`, `react-view-transitions`, `vercel-deploy-claimable`. Codifica le regole pubblicate da Vercel Engineering nei suoi best practice doc.

**Quando usarla.**

- Sviluppi React/Next.js professionalmente e vuoi codice rivisto contro standard noti
- Devi fare audit di accessibilità o performance su componenti già scritti
- Lavori con un team che vuole uniformità sullo stack frontend

**Quando NON usarla.**

- Lo stack è diverso da React/Next.js (le regole non si applicano)
- Stai prototipando velocemente e le regole rallentano l'iterazione

**Il mio giudizio.** Più di una skill, è una **guida di stile codificata** che Vercel pubblica gratis. Vale per chi sta dentro l'ecosistema React: se lo sei, l'investimento è zero (un comando di install) e il ritorno è alto (codice più solido al primo colpo). Se non lo sei, è inutile installarla.

**Esempio d'uso.** Durante un review chiedi *"applica `vercel-labs/web-design-guidelines` a tutti i file modificati nell'ultimo commit"*. Claude esegue un audit puntuale (focus state, contrasto colore, gestione errori form, animazioni) producendo un report di issue con riferimento alle regole violate.

#### 10.3.3 WordPress Agent Skills

| Chiave | Valore |
|---|---|
| **Autore / repo** | WordPress (organizzazione ufficiale) — [`github.com/WordPress/agent-skills`](https://github.com/WordPress/agent-skills) |
| **License** | GPL-2.0-or-later |
| **Star** | ~1.4k |
| **Invocazione** | Presenza di `wp-config.php`, plugin/theme files, riferimenti a `block.json` o REST API WP |

**Descrizione estesa.** Bundle di 14 skill di dominio WordPress costruite sulla doc ufficiale, per arginare il problema noto degli LLM che generano pattern WordPress obsoleti (codice da WP 4.x, ACF API deprecate, `query_posts()` al posto di `WP_Query`, ecc.). Include uno skill "router" (`wordpress-router`) che classifica il task e instrada alla skill specifica giusta.

**Quando usarla.**

- Sviluppi plugin o temi WordPress, in particolare con block editor e Interactivity API
- Vuoi codice aderente alla documentazione ufficiale e non a pattern datati
- Lavori su progetti dove la security WordPress è importante (capability, sanitize/escape, nonce)

**Quando NON usarla.**

- Lavori solo su contenuti WordPress (post, page) e non su codice
- Il sito è headless e WP fa solo da CMS via REST/GraphQL (poco beneficio)

**Il mio giudizio.** Per chi fa WordPress quotidianamente è la skill più utile in circolazione. Il problema dei "LLM che generano pattern WP obsoleti" è reale e costoso (ho visto codice generato da AI usare `query_posts()` o ACF v4 nel 2026), e questa skill lo elimina alla radice. Tre stelle su tre per chi lavora WordPress; zero per chi non lo fa.

**Esempio d'uso.** In un progetto WordPress chiedi *"Crea un nuovo blocco Gutenberg per inserire una callout box con icona, titolo e testo"*. `wordpress-router` riconosce il dominio e attiva `wp-block-development`, che impone `block.json` corretto, deprecation handling e security pattern dalla doc ufficiale.

#### 10.3.4 Trail of Bits Skills

| Chiave | Valore |
|---|---|
| **Autore / repo** | Trail of Bits — [`github.com/trailofbits/skills`](https://github.com/trailofbits/skills) |
| **License** | CC-BY-SA-4.0 |
| **Star** | ~5k |
| **Invocazione** | Richieste di security audit, code review per vulnerability assessment, malware analysis |

**Descrizione estesa.** 40+ skill di security per AI-assisted analysis, testing e auditing: smart contract security, code auditing (CodeQL/Semgrep), malware analysis, reverse engineering, mobile security, verification techniques. Trail of Bits è una delle aziende di consulenza security più riconoscibili in ambito open source: queste skill codificano metodologie usate sui loro audit professionali.

**Quando usarla.**

- Devi fare review di codice di terzi prima di integrare una libreria
- Sei security engineer e vuoi orchestrare CodeQL/Semgrep in modo guidato
- Lavori su progetti con esposizione esterna dove il rischio vulnerability è alto

**Quando NON usarla.**

- Stai facendo sviluppo applicativo greenfield senza esposizione critica (overkill)
- Non hai familiarità con i tool sottostanti (CodeQL, Semgrep): la skill orchestra ma il debugging dei falsi positivi richiede competenza

**Il mio giudizio.** Skill seria per un pubblico serio. La license CC-BY-SA-4.0 impone share-alike sui derivati: se modifichi le skill e le ridistribuisci sei vincolato — verifica la compatibilità con i tuoi vincoli aziendali. Per chi fa security è un boost notevole; per il resto è una cassetta degli attrezzi che probabilmente non userai.

**Esempio d'uso.** Prima di integrare una libreria PHP di terze parti chiedi *"Esegui un audit di security sulla cartella `vendor/foo-lib` usando le skill di Trail of Bits. Cerca pattern di SQLi, command injection, insecure deserialization"*. Le skill orchestrano CodeQL/Semgrep e producono un report con file, linea e tipo di vulnerabilità.

#### 10.3.5 Caveman

| Chiave | Valore |
|---|---|
| **Autore / repo** | Julius Brussee — [`github.com/JuliusBrussee/caveman`](https://github.com/JuliusBrussee/caveman) |
| **License** | MIT |
| **Star** | ~24k |
| **Invocazione** | Comandi `/caveman`, `/caveman lite`, `/caveman ultra`; trigger naturali tipo *"talk like caveman"* |

**Descrizione estesa.** Skill che forza Claude a rispondere in stile telegrafico: niente articoli, niente convenevoli, niente hedging, niente meta-commentari. Solo sostanza tecnica. Tre livelli di compressione (`lite`, `full`, `ultra`) per intensità crescente. La skill è chirurgica: comprime la parte discorsiva delle risposte (filler, articoli, frasi di cortesia) ma lascia intatti blocchi di codice, termini tecnici, messaggi di errore citati e commit message.

**Quando usarla.**

- Coding meccanico e ripetitivo (refactoring, debug, linting)
- Sei utente esperto e non hai bisogno del "perché" dettagliato
- Stai orchestrando agent multipli o background task dove l'output verbose è solo rumore
- Sei vicino al limite del tuo piano e vuoi spremere più sessioni

**Quando NON usarla.**

- Stai imparando un nuovo framework: ti serve la pedagogia, il "perché" è il valore
- Stai facendo onboarding su un codebase sconosciuto: vuoi spiegazioni complete
- Stai facendo revisione architetturale: vuoi sfumature, alternative, trade-off

**Il mio giudizio.** Caveman è un caso interessante di **claim virale che vale la pena leggere bene**. Il README promette "75% di token risparmiati" ed è diventato il numero di riferimento del progetto, ma vale la pena disaggregare il dato per capire dove davvero atterra il risparmio sulla tua bolletta:

| Numero | Cosa misura davvero |
|---|---|
| **65%** | Compressione media sull'**output** del modello (range 22-87%, misurato dai benchmark del repo). |
| **0.6-2.5%** | Quota di token che l'output rappresenta sul **totale** di una sessione Claude Code tipica. Il grosso del consumo è input: `CLAUDE.md`, cronologia conversazione, file letti, output di tool. |
| **1-2%** | Risparmio netto sulla bolletta in una **sessione interattiva normale** (output piccolo, input dominante). |
| **fino a 15-25%** | Risparmio in scenari **multi-agent paralleli** o pipeline batch headless, dove l'output diventa una quota maggiore del totale (più subagent che producono testo finale, meno input ripetuto). |

In sintesi: il "75%" virale si applica solo a una fetta minuscola del consumo nella maggior parte delle sessioni umane, mentre i numeri più alti che leggi a giro valgono per scenari particolari — caso non tipico, presentato come tipico. Il prodotto in sé è onesto (open source MIT, benchmark riproducibili nel repo), e il principio è quello che porto via davvero: pensare alla **verbosità dell'AI come a un costo misurabile**. Una volta che inizi a ragionarci, scrivi `CLAUDE.md` più leggeri, prompt più mirati, e l'efficienza cresce anche senza plugin.

**Esempio d'uso.** Risposta normale di Claude (69 token):

> *"The reason your React component is re-rendering is likely because you're creating a new object reference on each render cycle. When you pass an inline object as a prop, React's shallow comparison sees it as a different object every time, which triggers a re-render. I'd recommend using `useMemo` to memoize the object."*

Risposta in modalità Caveman (19 token):

> *"New object ref each render. Inline object prop = new ref = re-render. Wrap in `useMemo`."*

Stessa diagnosi, stessa soluzione, niente imbottitura.

### 10.4 Installare e gestire le skill

Le skill si installano in tre modi a seconda di come sono distribuite.

**Plugin marketplace** — quando una skill è confezionata come plugin (caso tipico per le skill della community più strutturate):

```bash
# Aggiungi il marketplace dell'autore
claude plugin marketplace add owner/repo

# Installa la skill specifica
claude plugin install <skill>@<plugin>
```

**Tool `npx skills`** — per skill standalone distribuite via repo Git:

```bash
# Installa una singola skill da un repo multi-skill
npx skills add anthropics/skills --skill frontend-design

# Installa l'intero pacchetto di skill di un repo
npx skills add vercel-labs/agent-skills
```

**Copia manuale** — per skill custom o sperimentali. Due location possibili:

```
~/.claude/skills/<nome>/SKILL.md       # globale (tutti i progetti)
.claude/skills/<nome>/SKILL.md         # solo questo progetto
```

La risoluzione segue la stessa gerarchia di altre risorse Claude Code: globale come default, locale al progetto come override.

#### Dove cercare skill nuove

L'ecosistema cresce molto velocemente. Le fonti più affidabili a oggi:

- **[`github.com/anthropics/skills`](https://github.com/anthropics/skills)** — repository ufficiale Anthropic, primo posto da controllare
- **[`skills.sh`](https://skills.sh)** — directory pubblica community, indicizza skill di terzi con metadati di base
- **Marketplace plugin pubblici** — gli autori di skill mature spesso pubblicano un marketplace dedicato (Trail of Bits, Vercel Labs, JuliusBrussee per Caveman)
- **Topic GitHub `claude-skills` e `agent-skills`** — utile per esplorazione mirata

Prima di installare qualunque cosa di terzi, leggi la [sezione 10.6](#sicurezza-delle-skill-di-terzi).

### 10.5 Creare una Skill personalizzata

Niente vieta di scrivere le proprie skill: anzi, è il punto in cui Claude Code diventa davvero "tuo". Vediamo un esempio end-to-end di una skill `mavida-wordpress` che codifica le convenzioni del tuo team.

**Step 1 — Scaffolding**:

```bash
# Skill locale al progetto (override) o globale (~/.claude/skills/)
mkdir -p .claude/skills/mavida-wordpress
```

**Step 2 — Scrivere `SKILL.md`** in `.claude/skills/mavida-wordpress/SKILL.md`:

```markdown
---
name: mavida-wordpress
description: "Use this skill when working on Mavida WordPress
projects. Triggers on: presence of wp-config.php, plugin
files in /wp-content/plugins/, theme files, references to
ACF or Block Editor."
---

# Convenzioni Mavida — WordPress

## Build e tooling
- Usa sempre @wordpress/scripts per i blocchi (no webpack custom)
- Composer per le dipendenze PHP, mai upload manuale di librerie
- Versioni minime: PHP 8.2, WordPress 6.4

## Pattern obbligatori
- Tutti i nuovi blocchi devono avere block.json + edit.js + save.js + style.scss
- Sanitize/escape rigorosi: `sanitize_text_field` in input, `esc_html`/`esc_attr` in output
- Nonce su tutte le form e le AJAX action
- Capability check con `current_user_can()` prima di operazioni privilegiate

## Pattern da evitare
- `query_posts()` (deprecato): usare `WP_Query`
- Funzioni che bypassano la cache: `wp_cache_flush()` solo in seed, mai in runtime
- Caricamento di JS via wp_head inline: sempre via `wp_enqueue_script`

## Comandi build comuni
- `npm run build`: build dei blocchi in produzione
- `composer test`: PHPUnit + PHPStan livello 6
- `wp-env start`: ambiente di sviluppo locale
```

**Step 3 — Verifica**: apri Claude Code in un progetto WordPress e chiedi una modifica banale (es. "Aggiungi una metabox al post type Articolo"). Se la skill è scritta bene, vedrai Claude applicare automaticamente le convenzioni (capability check, sanitize, enqueue corretti) senza che tu glielo abbia chiesto esplicitamente.

Per controllare che la skill sia caricata: `/skills list` (o `/help skills` a seconda della versione).

Lo stesso pattern vale per altre skill di team che torneranno utili nel quotidiano:

```
.claude/skills/
├── mavida-wordpress/          # convenzioni WP
│   └── SKILL.md
├── n8n-workflow/              # pattern per workflow N8N
│   └── SKILL.md
└── php-legacy-review/         # checklist refactoring PHP legacy
    └── SKILL.md
```

Una skill ben scritta è un pezzo di "memoria di team" che sopravvive ai cambi di sessione, di sviluppatore e — sempre più spesso — di tooling. Quando un prompt che usi spesso diventa una regola da imporre sistematicamente, è il segnale che vale la pena promuoverlo a skill (vedi anche la riflessione sulla "promozione" del prompt in [sezione 6.8](#promuovere-un-prompt-quando-va-in-claude.md-o-in-custom-command)).

### 10.6 Sicurezza delle skill di terzi

Una skill di terzi è codice che entra a far parte del contesto di Claude e può influenzare le sue decisioni. Non viene eseguita autonomamente — Claude chiede comunque conferma prima di lanciare comandi — ma può **istruire Claude a chiamare tool con effetti reali** (Bash, file system, WebFetch). Trattala come tratteresti una libreria che includi nel `composer.json` o nel `package.json`: con la stessa diligenza.

**Checklist prima di installare una skill di terzi:**

- **Codice review obbligatoria** — leggi `SKILL.md` per intero e ispeziona tutti gli script ausiliari (Python, Bash, JS) presenti nella cartella. Cerca riferimenti a comandi distruttivi, esfiltrazione dati, chiamate a domini esterni non documentate.
- **License compatibile** — verifica che la license della skill sia compatibile con il tuo progetto e con eventuali clausole NDA. CC-BY-SA (come Trail of Bits) impone share-alike sui derivati; GPL-2.0 (come WordPress agent-skills) ha implicazioni copyleft note; MIT (Vercel Labs, Superpowers) è generalmente la più permissiva.
- **Salute del repo** — controlla data ultimo commit, numero di star, rapporto issue aperte/chiuse, presenza di security advisories. Una skill abbandonata da un anno è un rischio per qualunque codebase la usi attivamente.
- **Permessi che richiede** — alcune skill chiedono accesso a tool potenti (Bash unrestricted, WebFetch su domini esterni, scrittura globale). Confrontale con la policy del tuo `settings.json` (vedi [sezione 9](#sicurezza-e-gestione-dei-permessi)) e respingi quelle che chiedono più di quanto giustifichino.
- **Sandbox in dev** — testa le skill nuove su un progetto throwaway prima di installarle globalmente in `~/.claude/skills/`. Se serve un ulteriore strato di difesa, un hook `PreToolUse` (vedi [sezione 13](#hook-automatizzare-il-lifecycle-di-claude-code)) può bloccare comandi che la skill prova a eseguire fuori dal perimetro consentito.

Lo schema mentale è lo stesso che applicheresti a una dipendenza qualunque: non si include codice che non hai letto, non si fida di un autore solo perché ha tante star, e non si abilita più di quanto serva. La differenza è che qui il "codice" è un'istruzione in linguaggio naturale che Claude leggerà ed eseguirà — e linguaggio naturale è ambiguo per definizione. Doppia attenzione.

---

## 11. MCP: integrare servizi esterni

Il **Model Context Protocol (MCP)** è il modo in cui Claude Code parla con sistemi esterni — API, database, servizi SaaS, file system fuori dalla working directory. Mentre le skill (cap. 10) estendono cosa Claude *sa fare* con istruzioni e codice locali, MCP estende a quali sistemi *si può collegare*. Per il confronto rapido fra i meccanismi di estensione vedi la mappa in [14.1](#meccanismi-di-estensione-di-claude-code-una-mappa).

### 11.1 Cos'è MCP e perché esiste

**Model Context Protocol (MCP)** è un protocollo aperto, open-sourced da Anthropic a novembre 2024, che standardizza il modo in cui un'applicazione AI (l'**host**) si connette a sorgenti di dati e strumenti esterni — file di un sistema, database, API di servizi, repository git, calendari, ticket system, qualunque cosa sia raggiungibile via codice.

L'idea è semplice e nasce da un problema concreto. Prima di MCP, ogni IDE AI (Claude Code, Cursor, Continue, ChatGPT desktop, Cline, decine d'altri) aveva il proprio meccanismo per connettersi a GitHub, Postgres, Slack, ecc. Per chi sviluppava un'integrazione, questo significava scriverla N volte — una per ogni client. Per chi usava più strumenti, ogni client aveva una matrice di connettori incompatibili tra loro: l'integrazione GitHub di Cursor non funzionava in Claude Code, e viceversa.

MCP risolve questo problema con la stessa logica con cui USB-C ha sostituito le decine di connettori proprietari: definisce **un protocollo standard** tra client (host AI) e server (l'integrazione). Chi scrive un'integrazione la scrive una volta, e funziona ovunque MCP è supportato. Anthropic ha rilasciato gli SDK ufficiali (Python, TypeScript, Java, C#, Rust, Kotlin, Swift) e una decina di server di riferimento per i casi d'uso più comuni (filesystem, fetch HTTP, GitHub, Postgres, SQLite, Puppeteer, Slack, Brave Search).

A maggio 2026 l'adozione è ampia: **Claude Code, Cursor, Windsurf, Cline, Continue, GitHub Copilot e diversi altri client supportano MCP** in modo nativo. Esistono centinaia di server community sui registry pubblici, e marketplace dedicati ([anthropic.com/mcp](https://anthropic.com/mcp), [glama.ai/mcp](https://glama.ai/mcp), [smithery.ai](https://smithery.ai)). Il protocollo è arrivato alla versione stabile 1.0 dopo le iterazioni del 2025.

Per chi scrive in italiano: pensare a MCP come al **driver standard tra Claude Code e il resto del mondo**. Se vuoi che Claude faccia qualcosa che non sa fare nativamente — leggere il tuo CRM, postare su WordPress, interrogare una base dati interna — la risposta moderna è: scrivi un server MCP (o trova quello che fa già al caso tuo) e lo registri.

### 11.2 Architettura del protocollo

MCP è un protocollo **client-server** basato su **JSON-RPC 2.0**. Tre i componenti principali:

- **Host** — l'applicazione AI dell'utente (per noi: Claude Code). Non parla direttamente coi server MCP: usa uno o più *client*.
- **Client** — una connessione 1:1 verso un singolo server. Claude Code crea un client per ogni server MCP configurato. Il client gestisce la connessione (avvio del processo, scambio messaggi, lifecycle) e isola il server dal resto dell'host.
- **Server** — il processo che espone funzionalità. Può essere scritto in qualsiasi linguaggio per cui esiste un SDK MCP (Python, TypeScript, Rust, Java, C#, Swift, Kotlin sono tutti supportati ufficialmente). Comunica con il client tramite uno standard di trasporto.

```
┌──────────────────────────────────────────────────────────┐
│                    HOST (Claude Code)                    │
│                                                          │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐              │
│  │ Client A │   │ Client B │   │ Client C │              │
│  └────┬─────┘   └────┬─────┘   └────┬─────┘              │
└───────┼──────────────┼──────────────┼────────────────────┘
        │ stdio        │ stdio        │ HTTP+SSE
        │              │              │
┌───────▼──────┐ ┌─────▼──────┐ ┌────▼─────────────────┐
│  Server WP   │ │   Server   │ │  Server cloud        │
│  (Python loc)│ │  Postgres  │ │  (Linear / Notion)   │
└──────────────┘ └────────────┘ └──────────────────────┘
```

**Trasporti** — due modalità principali:

- **stdio** (input/output standard) — il client lancia il server come sotto-processo e comunica via stdin/stdout. È il transport più comune per server locali (filesystem, database, processi nostri). Semplice, sicuro per default (resta nel sistema utente), niente rete da gestire.
- **HTTP+SSE** (Server-Sent Events) — server raggiungibili via HTTP. È usato per server ospitati (cloud) o condivisi tra client diversi. Richiede gestione di auth e considerazioni di latenza che non si pongono per stdio. La guida si concentra sui server stdio locali; i server remoti li accenneremo nella sezione 11.6.

**Capability negotiation** — all'avvio della sessione, client e server si scambiano un handshake (`initialize`) in cui dichiarano cosa supportano: il server elenca i suoi tool, le sue resource, i suoi prompt; il client elenca le proprie capability (es. supporto a sampling, logging). Da quel punto in avanti la conversazione è un'alternanza di richieste JSON-RPC.

Le **tre primitive** di un server MCP:

- **Tools** — funzioni che il server espone e che Claude può invocare. Ognuno ha un nome (`wp_create_post`), una descrizione testuale leggibile dall'AI, e uno schema JSON degli argomenti. Quando Claude decide di chiamarlo, manda una richiesta `tools/call`, il server esegue, restituisce il risultato. È la primitiva più usata.
- **Resources** — dati indirizzabili via URI (`wp://posts/123`, `file:///etc/hosts`). Il server li espone come "biblioteca" da cui Claude può leggere. Resource ≠ Tools: leggere una resource è una pura GET, non ha effetti collaterali.
- **Prompts** — template di prompt riutilizzabili che il server può fornire all'utente come "preset". Tipicamente esposti come comando `/server-name:prompt-name` nell'host.

Per il nostro esempio WordPress useremo solo i **tools** (creazione/aggiornamento post, lista categorie). Tools sono la parte più produttiva del protocollo; resources e prompts sono utili ma meno comuni nei server custom.

### 11.3 Configurare un server MCP esistente

La configurazione è dichiarativa: si elenca il server in un JSON e Claude Code lo lancia in automatico all'avvio della sessione. Due scope:

- **`.claude/settings.json`** del progetto — il server è disponibile solo dentro quel progetto. Adatto a integrazioni progetto-specifiche (un server per parlare col DB di staging del cliente).
- **`~/.claude/settings.json`** dell'utente — il server è disponibile in ogni sessione dell'utente. Adatto a integrazioni globali (il tuo server MCP per il proprio CRM aziendale).

Esempio di configurazione di tre server contemporaneamente (un GitHub e due locali):

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
      }
    },
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/maurizio/progetti"
      ]
    },
    "postgres": {
      "command": "uvx",
      "args": [
        "mcp-server-postgres",
        "postgresql://localhost/staging_db"
      ]
    }
  }
}
```

Punti chiave:

- **`command` + `args`** — eseguibile e argomenti. `npx -y` è il pattern standard per server distribuiti su npm (li scarica al volo). Per Python si usa tipicamente `uvx` o `python -m`.
- **`env`** — variabili d'ambiente passate al server. Le interpolazioni `${VAR}` sono risolte dalla shell che ha lanciato Claude Code: il modo corretto di passare segreti è metterli in `.env`/`.envrc` ed esportarli prima di lanciare Claude, non hardcodarli nel JSON committato.
- **Niente segreti in repo** — un `mcpServers` entry committato che contiene un token in chiaro è un incidente di sicurezza in attesa. Sempre `${VAR}` con segreti caricati esternamente.

**Slash command e CLI dedicati.** Una volta configurato un server, Claude Code lo gestisce con questi comandi:

```bash
# Slash command interno (in sessione interattiva)
/mcp                       # elenco server attivi e loro tool

# CLI esterna
claude mcp list            # stesso elenco da terminale
claude mcp add <name>      # aggiunge un server (intervista guidata)
claude mcp remove <name>   # lo rimuove
```

**Debug.** Se un server non parte (errore di avvio, dipendenza mancante, env var non risolta), Claude Code stampa l'errore al lancio della sessione e marca il server come "disconnected" in `/mcp`. Per inseguire problemi più sottili, lanciare il server manualmente da terminale ed esercitarlo via stdin con qualche `echo '{"jsonrpc":"2.0","method":"initialize",...}'` — la documentazione MCP ha esempi precisi.

### 11.4 Server MCP utili: una selezione curata

A maggio 2026 l'ecosistema MCP è vasto. Una selezione di server con cui vale la pena familiarizzare:

- **`@modelcontextprotocol/server-github`** — gestione completa di repository, issue, PR, action. È il primo MCP da installare per chi sviluppa su GitHub. Ufficiale, manutenuto da Anthropic.
- **`@modelcontextprotocol/server-filesystem`** — accesso controllato a directory specifiche del filesystem. Utile per lavorare su progetti fuori dalla working directory di Claude Code (es. leggere documentazione in `~/Documents/specs`). I path autorizzati sono passati come argomenti.
- **`mcp-server-postgres`** / **`mcp-server-sqlite`** — query, schema inspection, generazione di migration. Ottimi per esplorare basi dati di staging senza permessi di scrittura sul prod.
- **`@modelcontextprotocol/server-puppeteer`** — automazione browser headless: screenshot, scraping, click test. Coppia molto bene con la skill `webapp-testing` (cap. 10).
- **`mcp-server-slack`** — invio di messaggi e lettura di canali, utile per notifiche di completamento di task lunghi o report automatici.
- **`mcp-server-sentry`** — accesso ai dati di error tracking; può recuperare lo stack trace di un'eccezione recente e darlo a Claude per il bug fix. Coppia con cap. 15.2 (Bug hunting con TDD).
- **`mcp-server-linear`** / **`mcp-server-notion`** — ticket system e knowledge base. Permettono a Claude di leggere il contesto di un task da Linear e produrre il PR collegato.

I marketplace della community ne hanno centinaia altri: prima di scrivere un MCP da zero, cercare se esiste già un server adatto. La regola è: **MCP esistente > MCP custom > skill > script locale**, in ordine di preferenza per soluzioni nuove.

### 11.5 Creare un server MCP da zero: pubblicare su WordPress

Caso d'uso: vogliamo che Claude Code possa **pubblicare contenuti su un sito WordPress** senza dover aprire la dashboard wp-admin. Lo scenario tipico: stai discutendo con Claude un articolo (lo scrivi in Markdown, lui ti suggerisce taglio editoriale), e vuoi chiudere la sessione con *"pubblica questo articolo come bozza nella categoria 'Tutorial'"*. Senza MCP, Claude può tutt'al più dirti "ecco i passaggi da fare in admin". Con MCP, lo fa lui.

#### Prerequisiti

1. Un sito WordPress con REST API attiva (default da WP 5.0+).
2. Un'**Application Password** generata dal profilo utente WordPress (utente → modifica profilo → "Application Passwords"). È una password monouso, lunga, separata dalla password principale: si revoca senza dover cambiare la password vera.
3. **Python 3.10+** e l'SDK ufficiale: `pip install mcp httpx python-dotenv`.

#### Struttura del progetto

```
~/mcp/wordpress-publisher/
├── server.py
├── pyproject.toml
└── .env
```

`.env` (mai committare):

```
WP_BASE_URL=https://miosito.example.com
WP_USERNAME=maurizio
WP_APP_PASSWORD=xxxx xxxx xxxx xxxx xxxx xxxx
```

#### Codice del server (`server.py`)

```python
"""
Server MCP che pubblica articoli su WordPress via REST API.
Tre tool esposti:
  - wp_create_post     : crea una bozza (o pubblica direttamente)
  - wp_publish_post    : promuove una bozza esistente a "publish"
  - wp_list_categories : elenca le categorie del sito
"""

import os
import base64
import httpx
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

# Carica le credenziali da .env (mai hardcodare in repo)
load_dotenv()
BASE_URL = os.environ["WP_BASE_URL"].rstrip("/")
USERNAME = os.environ["WP_USERNAME"]
APP_PASS = os.environ["WP_APP_PASSWORD"]

# Auth Basic con Application Password (formato standard WP)
auth_token = base64.b64encode(
    f"{USERNAME}:{APP_PASS}".encode("utf-8")
).decode("ascii")
HEADERS = {
    "Authorization": f"Basic {auth_token}",
    "Content-Type": "application/json",
}

# Istanza FastMCP: il server si chiamerà "wordpress-publisher"
mcp = FastMCP("wordpress-publisher")


@mcp.tool()
def wp_create_post(
    title: str,
    content: str,
    status: str = "draft",
    categories: list[int] | None = None,
) -> dict:
    """
    Crea un nuovo articolo su WordPress.

    Args:
        title:      titolo del post
        content:    corpo HTML o Gutenberg-block
        status:     "draft" (default) o "publish"
        categories: lista di ID categoria (opzionale)

    Returns:
        Dict con id, status, link, modified del post creato.
    """
    payload = {"title": title, "content": content, "status": status}
    if categories:
        payload["categories"] = categories

    response = httpx.post(
        f"{BASE_URL}/wp-json/wp/v2/posts",
        headers=HEADERS,
        json=payload,
        timeout=30.0,
    )
    response.raise_for_status()
    data = response.json()
    return {
        "id": data["id"],
        "status": data["status"],
        "link": data["link"],
        "modified": data["modified"],
    }


@mcp.tool()
def wp_publish_post(post_id: int) -> dict:
    """
    Promuove una bozza esistente a stato "publish".

    Args:
        post_id: ID del post da pubblicare

    Returns:
        Dict con id, status, link aggiornato.
    """
    response = httpx.post(
        f"{BASE_URL}/wp-json/wp/v2/posts/{post_id}",
        headers=HEADERS,
        json={"status": "publish"},
        timeout=30.0,
    )
    response.raise_for_status()
    data = response.json()
    return {
        "id": data["id"],
        "status": data["status"],
        "link": data["link"],
    }


@mcp.tool()
def wp_list_categories() -> list[dict]:
    """
    Elenca tutte le categorie del sito.

    Returns:
        Lista di dict con id, name, slug, count per ogni categoria.
    """
    response = httpx.get(
        f"{BASE_URL}/wp-json/wp/v2/categories",
        headers=HEADERS,
        params={"per_page": 100},
        timeout=30.0,
    )
    response.raise_for_status()
    return [
        {"id": c["id"], "name": c["name"], "slug": c["slug"], "count": c["count"]}
        for c in response.json()
    ]


if __name__ == "__main__":
    # Avvio del server in modalità stdio (default per MCP locali)
    mcp.run()
```

#### Registrazione in Claude Code

Aggiungere al proprio `.claude/settings.json` (o a quello globale):

```json
{
  "mcpServers": {
    "wordpress-publisher": {
      "command": "python",
      "args": ["/Users/maurizio/mcp/wordpress-publisher/server.py"]
    }
  }
}
```

#### Test interattivo

Lanciare Claude Code, eseguire `/mcp` per verificare che il server `wordpress-publisher` sia connesso e che mostri tre tool. Poi una conversazione tipica:

> **Tu**: ho appena finito di scrivere un articolo su Plan Mode, lo trovi in `articolo-plan-mode.md`. Pubblicalo come bozza nella categoria "Tutorial".
>
> **Claude**: Leggo prima il file per estrarne titolo e contenuto.
> *[Read articolo-plan-mode.md]*
> Ho letto l'articolo: 1840 parole, titolo *"Plan Mode: pensare prima di scrivere"*. Recupero gli ID delle categorie per trovare "Tutorial".
> *[wp_list_categories]*
> Categoria "Tutorial" ha ID **7**. Procedo con la creazione della bozza.
> *[wp_create_post(title=..., content=..., status="draft", categories=[7])]*
> ✓ Bozza creata. ID **142**, link [https://miosito.example.com/?p=142&preview=true](https://...). Vuoi che la pubblichi adesso o resta bozza per la revisione?
>
> **Tu**: Lasciala in bozza, devo riguardare le immagini.

#### Cosa succede sotto il cofano

Claude Code ha:

1. Letto `articolo-plan-mode.md` con il proprio tool nativo Read.
2. Capito che serviva l'ID categoria — ha chiamato `wp_list_categories` (un tool MCP).
3. Cercato "Tutorial" tra le categorie restituite e estratto l'ID 7.
4. Chiamato `wp_create_post` con titolo, contenuto e categorie.
5. Riportato l'esito con il link di anteprima.

Tutto via JSON-RPC tra il client (Claude Code) e il nostro server Python che gira come sotto-processo locale. Niente hop di rete sui dati sensibili — solo le richieste HTTPS al server WordPress, esattamente come se l'utente le avesse fatte da un client REST.

#### Estensioni naturali

Da questo scheletro è facile crescere:

- aggiungere `wp_upload_media` per caricare immagini in libreria;
- aggiungere `wp_list_drafts` per recuperare bozze esistenti;
- aggiungere `wp_schedule_post` per pubblicazioni schedulate (`status: "future"` con `date`);
- esporre le categorie e i post come **resources** (URI `wp://categories`, `wp://posts/{id}`) per dare a Claude visibilità del catalogo senza dover invocare un tool ogni volta.

Per chi viene dal mondo plugin WordPress: questo server MCP è in pratica un **client REST lato AI**. Tutto quello che il tuo plugin può fare via API REST, il tuo MCP può esporlo come tool.

### 11.6 Sicurezza e considerazioni operative

Tre punti d'attenzione che separano un server MCP da un esperimento e un server MCP pronto per il mestiere.

**Nessuna sandbox automatica.** Un server MCP gira come *te*: ha le tue credenziali file system, accesso alla rete, e i token che gli passi via env. Niente lo isola dal resto del sistema. Conseguenze pratiche:

- **Audita il codice** prima di installare server MCP di terzi, specialmente se ottenuti da marketplace meno presidiate. Un server malevolo può leggerti il `~/.ssh` o esfiltrare segreti dalle env.
- **Mantieni i tuoi server MCP custom in repo che controlli**, non come dipendenze npx anonime.
- **Usa Application Password / API key con scope minimo**, mai la password personale principale. Le revochi con un click se serve.

**Permission deny per i tool sensibili.** I tool MCP confluiscono nel sistema dei permessi di Claude Code (cap. 9). Per server con tool rischiosi (cancellare post, eseguire query DELETE) vale la pena denylistare i tool distruttivi in `permissions.deny`:

```json
{
  "permissions": {
    "deny": [
      "mcp__wordpress-publisher__wp_delete_post",
      "mcp__postgres__query_write"
    ]
  }
}
```

Il pattern `mcp__<server>__<tool>` permette di colpire con precisione il tool che non vuoi auto-approvato; Claude continuerà a chiedere conferma esplicita ad ogni invocazione.

**Logging e audit.** Per capire cosa il tuo MCP sta davvero combinando in produzione, accoppia un **hook PostToolUse** (cap. 13) che logga ogni invocazione di tool MCP in JSON Lines. Patterns concreti nel cap. 13.6 (esempio B). Effetto: tracciabilità totale di chi (utente, modello), cosa (quale tool MCP), quando e con quali argomenti.

**MCP remoti.** I server raggiunti via HTTP+SSE (server hostati, condivisi tra team) aggiungono una dimensione: latenza e auth di rete. Per integrazioni stabili a livello di team conviene un server hostato; per sperimentazione e per integrazioni personali stdio locale è più semplice e più sicuro per default. Il protocollo è lo stesso, cambia solo il transport.

**Quando NON serve un MCP.** Se il task è puramente locale (lettura di un file, esecuzione di uno script), Claude Code ha già Read/Write/Bash come tool nativi: scriversi un MCP per fare quello che già fa Bash è overkill. La regola è: **MCP per servizi esterni o protocolli di rete; tool nativi per il sistema utente locale**. In dubbio, prima skill (cap. 10) o slash command custom; MCP solo quando si tratta di un sistema esterno con cui Claude deve dialogare via API.

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

## 14. Plugin: pacchetti distribuibili

I plugin sono il meccanismo che Claude Code usa per **distribuire e installare estensioni**: skill, server MCP, subagent custom, slash command — tutti raggruppati in un singolo pacchetto installabile con un comando. Se la skill insegna a Claude *cosa fare* (cap. 10) e l'MCP gli dice *con cosa parlare* (cap. 11), il plugin è il **container** che li mette insieme e li distribuisce. Per chi viene dal mondo dello sviluppo: pensa al plugin come al pacchetto npm/Composer dell'ecosistema Claude Code.

### 14.1 Meccanismi di estensione di Claude Code: una mappa

A questo punto del libro hai visto **tutti e quattro** i meccanismi di estensione di Claude Code che il plugin va a impacchettare: le **Skill** ([cap. 10](#skill-il-meccanismo-di-estensione)), gli **MCP** ([cap. 11](#mcp-integrare-servizi-esterni)), i **Subagent** ([cap. 12](#subagent-orchestrare-lavoro-specializzato)) e gli **Hook** ([cap. 13](#hook-automatizzare-il-lifecycle-di-claude-code)). Prima di entrare nei plugin, conviene riposizionarli in una mappa unica, così da capire dove ciascuno opera e che relazione hanno con il container che stiamo per esaminare.

| Meccanismo | Cosa fa / dove agisce | Dove vive | Come si distribuisce |
|------------|------------------------|-----------|----------------------|
| **Skill** ([cap. 10](#skill-il-meccanismo-di-estensione)) | Estende cosa Claude *sa fare* | Markdown + script locali | Cartella nel sistema utente, plugin |
| **MCP** ([cap. 11](#mcp-integrare-servizi-esterni)) | Espone tool/dati di sistemi esterni | Server (locale stdio o remoto HTTP+SSE) | Protocollo aperto, qualsiasi linguaggio |
| **Subagent** ([cap. 12](#subagent-orchestrare-lavoro-specializzato)) | Esegue lavoro specializzato in isolamento | YAML in `.claude/agents` | File config, plugin |
| **Hook** ([cap. 13](#hook-automatizzare-il-lifecycle-di-claude-code)) | Intercetta eventi del lifecycle | `settings.json` `hooks` | Config locale, plugin |
| **Plugin** (questo cap.) | Pacchetto che raggruppa gli altri quattro | Cartella con manifest + payload | Marketplace, repo Git |

In una vista verticale: **Plugin** è il container, gli altri quattro sono i **contenuti** che possono essere bundlati dentro un plugin. Un plugin "GitHub PR Assistant" può contenere: una skill di review, un server MCP che parla con l'API GitHub, un subagent specializzato per scrivere PR description, e uno slash command `/review` che orchestra il tutto. Tutti distribuiti come un singolo pacchetto.

### 14.2 Cos'è un plugin e perché esiste

Un plugin nasce per risolvere un problema pratico: quando una persona o un'organizzazione mantiene un set di skill, server MCP e workflow custom, distribuirli singolarmente è scomodo. Il consumatore deve trovare il repo della skill, copiare i file in `.claude/skills/`, configurare il server MCP nel `settings.json`, registrare gli slash command — passi separati che non scalano se l'autore aggiorna le componenti spesso.

Il plugin standardizza tutto questo:

- **Una sola installazione** raccoglie tutte le componenti
- **Versionamento centrale** — l'autore rilascia una nuova versione, tu fai `claude plugin update`
- **Disinstallazione pulita** — rimuove tutto in un colpo solo
- **Marketplace condiviso** — gli autori pubblicano il plugin su un marketplace pubblico o privato

I plugin sono particolarmente preziosi per **organizzazioni** che vogliono distribuire ai team un set coerente di estensioni (skill aziendali + MCP per API interne + subagent specializzati), e per **autori community** che producono pacchetti tematici (Vercel Labs, WordPress Agent Skills, JuliusBrussee/caveman sono tutti distribuiti come plugin).

### 14.3 Anatomia di un plugin

Un plugin è una cartella con una struttura standardizzata. Esempio minimale:

```
my-plugin/
├── plugin.yml             # manifest del plugin
├── skills/                # skill incluse (opzionale)
│   └── my-skill/
│       └── SKILL.md
├── mcp/                   # server MCP inclusi (opzionale)
│   └── my-server/
│       ├── server.py
│       └── pyproject.toml
├── agents/                # subagent custom (opzionale)
│   └── my-agent.yaml
├── commands/              # slash command custom (opzionale)
│   └── my-command.md
└── README.md              # documentazione
```

Il file **`plugin.yml`** è il manifest che dichiara metadati, dipendenze e cosa il plugin contiene:

```yaml
name: my-plugin
version: 1.0.0
description: "Plugin di esempio"
author: "Maurizio Pelizzone <maurizio@mavida.com>"
license: MIT
homepage: "https://github.com/mavida/my-plugin"

# Componenti incluse
includes:
  skills:
    - skills/my-skill
  mcp_servers:
    - name: my-server
      command: python
      args: ["mcp/my-server/server.py"]
  agents:
    - agents/my-agent.yaml
  commands:
    - commands/my-command.md

# Compatibility
requires:
  claude_code: ">=2.1.0"
```

Il manifest dichiara tutto ciò che il plugin installa. Quando l'utente fa `claude plugin install`, Claude Code legge il manifest, copia/registra le componenti negli slot giusti (`~/.claude/skills/`, `mcpServers` in `settings.json`, ecc.) e attiva il plugin.

### 14.4 Plugin marketplace

Un **marketplace** è un'index pubblicato di plugin disponibili, tipicamente un repository Git con una struttura attesa. Claude Code supporta:

- **Marketplace ufficiali Anthropic** (`anthropics/skills` e simili)
- **Marketplace community** (Vercel Labs, Trail of Bits, JuliusBrussee)
- **Marketplace privati** dell'organizzazione (un repo Git interno con i plugin aziendali)

Comandi di base:

```bash
# Aggiungi un marketplace alla tua istanza
/plugin marketplace add anthropics/skills

# Esplora i plugin disponibili (apre picker interattivo)
/plugin

# Installa un plugin specifico
/plugin install <nome-plugin>

# Aggiorna i plugin installati
claude plugin update

# Disinstalla un plugin
claude plugin uninstall <nome-plugin>
```

Il picker `/plugin` mostra metadati del plugin (nome, versione, descrizione, autore) e un'anteprima delle componenti incluse, così sai cosa stai installando prima del download. Una volta installato, il plugin va in `~/.claude/plugins/<nome>/` e le sue componenti diventano automaticamente disponibili in tutte le sessioni.

### 14.5 Creare un plugin custom

Vediamo la struttura minimale di un plugin demo. Lo scenario: un plugin "hello-world" che contiene un solo slash command `/hello` e una skill di benvenuto.

**Step 1 — Crea la cartella e il manifest** in `~/my-plugins/hello-world/`:

```yaml
# plugin.yml
name: hello-world
version: 0.1.0
description: "Plugin di esempio"
author: "Maurizio Pelizzone"
license: MIT

includes:
  skills:
    - skills/hello-skill
  commands:
    - commands/hello.md
```

**Step 2 — Aggiungi la skill** in `skills/hello-skill/SKILL.md`:

```markdown
---
name: hello-skill
description: "Use this skill when the user asks for greetings or examples of plugin usage."
---

# Hello Skill

Quando l'utente chiede esempi di plugin o saluti, rispondi con:
- Un breve saluto
- Una nota che questa risposta arriva da una skill installata via plugin
```

**Step 3 — Aggiungi lo slash command** in `commands/hello.md`:

```markdown
---
description: "Saluto rapido dal plugin hello-world"
---

Saluta l'utente in modo amichevole e ricorda che questo comando arriva
dal plugin hello-world (versione 0.1.0).
```

**Step 4 — Installa localmente per test** (senza pubblicarlo):

```bash
# Installa il plugin in modalità development (link, non copy)
claude plugin install ~/my-plugins/hello-world --dev
```

Apri Claude Code: digita `/hello` e dovresti vedere il saluto. Chiedi a Claude qualcosa che attivi la skill — la `description` parla di "greetings" — e dovresti vedere la risposta che cita esplicitamente l'origine plugin.

### 14.6 Distribuire un plugin

Una volta che il plugin funziona localmente, distribuirlo richiede tre passi:

1. **Pubblica il repo Git** con la struttura del plugin nella root. Il `plugin.yml` deve essere alla radice della cartella.
2. **Crea un marketplace** (anche minimal: un secondo repo Git con un file `marketplace.yml` che elenca i tuoi plugin):

```yaml
# marketplace.yml
name: mavida
description: "Plugin Mavida per Claude Code"

plugins:
  - name: hello-world
    repo: https://github.com/mavida/hello-world
    versions: [0.1.0]
```

3. **Documenta l'installazione** nel README:

```bash
/plugin marketplace add mavida/marketplace
/plugin install hello-world
```

Per gestire le versioni, usa tag Git semantici (`0.1.0`, `0.2.0`, `1.0.0`). Claude Code rispetta la versione richiesta nel manifest del consumatore.

### 14.7 Sicurezza e considerazioni operative

Un plugin può contenere **codice eseguibile** (server MCP in Python/Node, hook in Bash, script ausiliari nelle skill). Installare un plugin di terzi è equivalente a installare un pacchetto npm o Composer: ti fidi dell'autore con i permessi che il plugin richiederà.

Tre regole pratiche:

- **Audita prima di installare**. Leggi il manifest, ispeziona le skill incluse, controlla cosa lanciano i server MCP. Una check-list: `plugin.yml` cosa dichiara di installare? Le skill richiedono accesso a tool sensibili? Gli MCP server contattano servizi esterni a cui non vorresti dare le tue credenziali?
- **Verifica la salute del repo** dell'autore: data ultimo commit, issue aperte/chiuse, presenza di security policy. Un plugin abbandonato due anni fa è un rischio costante.
- **Usa marketplace privati** per uso aziendale. Per plugin con segreti aziendali (chiavi API, URL interni) tieni il marketplace su un repo Git aziendale, non pubblico.

Per plugin di organizzazioni note (Anthropic, Vercel Labs, WordPress) il rischio è basso: pubblicano sotto i loro nomi, il codice è scrutinato dalla community, gli aggiornamenti sono regolari. Per plugin individuali, applica la stessa cautela che useresti per una libreria di terzi.

Una protezione aggiuntiva: i tool MCP esposti dai plugin confluiscono nel sistema dei permessi di Claude Code (cap. 9), quindi puoi denylistare con precisione le operazioni distruttive con `permissions.deny` su pattern `mcp__<server>__<tool>` (vedi 12.6 per esempi).

---

## 15. Workflow avanzati e tips

I capitoli precedenti hanno costruito le fondamenta concettuali — comandi, Plan Mode, memoria, contesto, sicurezza, skill, plugin, subagent, hook. Questo capitolo è la cassetta degli attrezzi: prima quattro **workflow pratici** (15.1-15.4) che combinano le fondamenta in scenari concreti di uso quotidiano, poi sei **tips** (15.5-15.10) per chi vuole spingere ulteriormente l'efficienza dello strumento.

### 15.1 Onboarding su un repository esistente

```
Prompt: "Sei appena stato assegnato a questo progetto. Analizza la
struttura, identifica:
1. Pattern architetturali principali (MVC, hexagonal, ecc.)
2. Come è gestita l'autenticazione
3. Dove sono i punti di integrazione con servizi esterni
4. Convenzioni di naming e stile
5. Eventuali debiti tecnici evidenti

Produci un documento di onboarding in docs/ONBOARDING.md.
Non modificare altro codice."
```

**Perché funziona:**
- Obiettivo chiaro con lista numerata
- Output specifico (un file in posizione nota)
- Vincolo esplicito ("non modificare altro")

### 15.2 Bug hunting con TDD

```
Prompt: "Bug report: quando un utente con ruolo 'editor' prova a
modificare un post 'private', riceve errore 500. Log allegato:
[incolla log].

Workflow richiesto:
1. Attiva Plan Mode e analizza il codice coinvolto
2. Scrivi PRIMA un test che riproduca il bug (deve fallire)
3. Correggi il bug con la modifica MINIMA necessaria
4. Verifica che il test passi
5. Esegui la suite completa per escludere regressioni"
```

**Perché funziona:**
- Forza un approccio TDD disciplinato
- Evita le "correzioni veloci" che sopprimono sintomi
- Il test scritto prima diventa documentazione del bug

### 15.3 Refactoring sicuro

```
Prompt: "Il modulo includes/class-order-processor.php è diventato
ingestibile (800 righe, responsabilità multiple). Voglio
rifattorizzarlo.

Fase 1 — CARATTERIZZAZIONE (Plan Mode):
- Identifica tutte le responsabilità attualmente mescolate
- Proponi una scomposizione in classi più piccole
- Elenca i test che DEVONO esistere prima di toccare il codice

Fermati qui e aspetta la mia approvazione del piano."
```

Dopo approvazione:

```
"Procedi con la Fase 2:
- Scrivi i test di caratterizzazione che bloccano il
  comportamento attuale
- Eseguili e conferma che passano tutti
- Fai un commit con messaggio 'test: caratterizzazione pre-refactoring'"
```

E poi:

```
"Fase 3 — refactoring incrementale:
- Estrai una responsabilità alla volta
- Dopo ogni estrazione, esegui i test
- Se fallisce anche UN solo test, fermati e chiedi"
```

### 15.4 Audit di performance

```
Prompt: "Analizza il build di produzione e identifica i 5 problemi
di performance a più alto impatto. Per ciascuno:
- File e linee coinvolti
- Impatto stimato (ms, KB, richieste HTTP)
- Fix proposto
- Complessità del fix (bassa/media/alta)

Ordina per rapporto impatto/complessità. Non modificare nulla."
```

I tips che seguono (14.5-14.10) sono trucchi singoli, da pescare a piacere quando il caso d'uso si presenta.

### 15.5 Vim mode

Se vieni da Vim, abilita la modalità in `/config` → Editor mode. Avrai navigazione con `hjkl`, comandi `d`, `y`, `p`, ecc.

### 15.6 Custom slash command

Puoi creare slash command personalizzati salvando file Markdown in `.claude/commands/`:

```markdown
<!-- .claude/commands/security-audit.md -->
Esegui un audit di sicurezza focalizzato su:
1. SQL injection nelle query dirette
2. XSS negli output non escaped
3. CSRF senza nonce verification
4. Path traversal nelle operazioni filesystem
5. Credenziali hardcoded

Per ogni issue trovata: file, riga, severity (low/medium/high/critical),
fix suggerito.
```

Ora da sessione puoi lanciare `/security-audit` e Claude esegue il prompt salvato.

### 15.7 Modalità headless per CI/CD

Il flag `-p` (print) esegue Claude in modalità non-interattiva, perfetta per pipeline:

```bash
# Esempio GitHub Actions
claude -p "Review the changes in this PR and flag any security issues" \
       --output-format json > review.json
```

Il `--output-format json` produce output strutturato parsabile da step successivi.

### 15.8 Recap delle sessioni

Se lasci il terminale e torni dopo 3+ minuti, Claude Code mostra automaticamente un riepilogo di quello che è stato fatto. Ottimo per context-switching. Puoi forzarlo con `/recap`.

### 15.9 Checkpoint Git strategici

Prima di task rischiosi, chiedi esplicitamente:

> *"Prima di procedere, fai un commit con messaggio 'checkpoint pre-refactoring' così abbiamo un punto di ritorno sicuro."*

Se qualcosa va storto, `git reset --hard HEAD~1` ti riporta al punto precedente.

### 15.10 Fork della conversazione

Premi `Esc` due volte per tornare a un messaggio precedente e rieditarlo. Crea un "ramo" della conversazione — utile quando un prompt non ha dato il risultato sperato e vuoi riformulare senza perdere tutto.

---

## 16. Conclusioni: perché la CLI e non solo la chat

Dopo aver affrontato installazione, comandi, Plan Mode, CLAUDE.md, Skill e tutto il resto, resta una domanda legittima che vale la pena esplicitare: *perché usare Claude Code CLI quando posso semplicemente incollare il codice in una chat del browser?*

La chat resta uno strumento validissimo, e anzi in alcuni scenari è la scelta più efficace. Ma tre differenze fanno della CLI uno strumento qualitativamente diverso, non solo una variante del canale.

### 16.1 Contesto persistente: smettere di presentarsi ogni volta

Nella chat tradizionale, ogni nuova sessione parte da zero. Il modello non sa nulla del tuo progetto: le convenzioni di naming, lo stack, le regole invalicabili, i comandi di build. Ogni volta devi ri-spiegare, oppure sperare che Claude indovini dal codice che incolli.

Con la CLI, **`CLAUDE.md` è un contratto permanente**. Viene letto automaticamente a ogni sessione, è gerarchico (globale utente, monorepo, progetto), e puoi rigenerarlo con `/init` ogni volta che il progetto evolve. I comandi `--continue` e `--resume` ti permettono di riprendere conversazioni interrotte giorni prima nello stesso stato di contesto.

Questo cambia il modo in cui pensi al tuo ambiente di sviluppo: invece di riconfigurare mentalmente l'AI a ogni apertura, configuri una volta e lavori. La stessa logica dei file `.editorconfig`, `.eslintrc`, `.gitignore` che consolidano le regole del progetto una volta per tutte.

### 16.2 Autonomia agentica: esegue, non solo suggerisce

Nella chat, Claude produce testo. Tu sei il ponte umano: copi il codice nell'editor, salvi, apri il terminale, esegui il test, leggi l'errore, torni in chat, incolli l'errore, aspetti la correzione, copi la correzione, incolli nell'editor, e così via. Ogni passaggio è un'interruzione del flusso.

Nella CLI, Claude **è** il terminale. Legge i file, esegue i comandi, vede gli errori, fa commit, apre PR, interroga database via MCP, naviga cartelle, lancia test. Il ciclo "scrivi → testa → correggi" diventa una conversazione continua senza uscire dallo strumento:

```
Tu:      "Il test auth/login.test.js fallisce. Capisci perché e correggi."

Claude:  [legge il test]
         [legge il codice sotto test]
         [esegue npm test -- auth/login.test.js]
         [analizza l'output]
         [identifica il bug]
         [modifica il codice]
         [riesegue il test]
         [tutto verde]
         "Corretto. Il problema era nella gestione del token expiry.
          Ho modificato validateToken() alle righe 34-38."
```

Questa autonomia ha un rovescio della medaglia — motivo per cui ci sono capitoli interi sulla sicurezza e su Plan Mode — ma quando ben gestita moltiplica la produttività in modo non lineare. Non fai una cosa più veloce: fai cose che in chat semplicemente non faresti perché il costo di orchestrazione manuale è troppo alto.

### 16.3 Integrazione nel workflow reale

Lo sviluppo professionale non è solo scrivere codice: è git, test suite, linting, CI/CD, code review, dipendenze, ambienti. La chat vive **accanto** a questo workflow; la CLI vive **dentro**.

**Git nativo.** Claude Code fa commit, apre branch, risolve merge conflict, scrive commit message Conventional Commits, gestisce stash. Non gli spieghi il diff: lo legge direttamente da `git diff`.

**Test e lint in loop.** La CLI esegue la test suite, legge gli errori del linter, riprova finché non passa. Non c'è copia-incolla tra finestre, non c'è "aspetta che ti mando l'output".

**CI/CD headless.** Il flag `-p` trasforma Claude in un tool da pipeline:

```bash
claude -p "Review the changes in this PR and flag any security issues" \
       --output-format json > review.json
```

Inserisci questo step in un workflow GitHub Actions e hai code review AI automatica a ogni push. Prova a fare la stessa cosa con una chat in browser.

### 16.4 Quando la chat resta la scelta giusta

Per onestà: ci sono casi in cui aprire chat.anthropic.com è la mossa migliore:

- **Brainstorming concettuale** senza codice specifico — "Quali pattern posso usare per implementare un feature flag system?"
- **Apprendimento di un framework nuovo** — ti serve la pedagogia, non l'esecuzione
- **Domande architetturali astratte** — "Vale la pena introdurre CQRS in questo contesto?"
- **Revisione di singoli snippet** da codice che non hai localmente
- **Discussioni con Claude su argomenti non-coding** — scrittura, analisi documenti, pianificazione

La regola pratica: se la risposta è **"codice da integrare nel mio progetto"**, usa la CLI. Se la risposta è **"un'idea, un principio, una spiegazione"**, la chat basta.

### 16.5 In sintesi

Claude Code CLI non è "Claude-in-chat con un'interfaccia diversa". È uno strumento agentico che trasforma un assistente linguistico in un **collega junior operativo**: può fare cose, non solo consigliarle. Per chi sviluppa professionalmente, la differenza è la stessa che passa tra avere un consulente che manda email e avere uno stagista al tavolo accanto. Entrambi utili, contesti diversi.

Il mio consiglio, se stai iniziando: installa Claude Code, prova un progetto piccolo e non critico, scrivi un `CLAUDE.md` decente, usa sempre Plan Mode per i task non banali, e dopo una settimana valuta. La curva è ripida i primi due giorni, poi si appiana.

---

## Allegato A — Glossario

Termini ricorrenti nella guida e nell'ecosistema Claude Code, utili come riferimento rapido.

::: glossary

**Agente (agentic)** — Sistema AI capace di eseguire azioni nel mondo reale (comandi, modifiche file, chiamate API), non solo di produrre testo. Claude Code è un agente a differenza della chat classica.

**Agent Teams** — Feature sperimentale di Claude Code (richiede la variabile d'ambiente `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`) che permette a più istanze indipendenti di Claude di girare in vero parallelismo simultaneo, coordinate tramite task list condivisa e mailbox di messaggi. Da non confondere con la delega multipla a subagent in foreground, che è invece sequenziale.

**Auto Memory** — Memoria persistente che Claude Code alimenta autonomamente durante le sessioni (introdotta in v2.1.59). A differenza di `CLAUDE.md`, scritto dall'utente, Auto Memory è scritta dal modello: accumula apprendimenti, pattern e correzioni ricorrenti del progetto. Vive in `~/.claude/projects/<project>/memory/` ed è organizzata in un indice (`MEMORY.md`) più topic file caricati on-demand.

**Chain of Thought (CoT)** — Tecnica di prompt engineering che chiede esplicitamente al modello di "ragionare passo dopo passo" prima di rispondere, anziché produrre direttamente la conclusione. Forza l'esplicitazione dei passaggi logici e migliora l'accuratezza su task complessi (debugging, decisioni architetturali, problemi multi-fase).

**CLAUDE.md** — File Markdown nella root del progetto che contiene contesto persistente: stack, convenzioni, comandi, regole. Letto automaticamente a ogni sessione.

**CLI (Command Line Interface)** — Interfaccia a riga di comando. Lo strumento `claude` si usa da terminale anziché da browser.

**Context engineering** — Disciplina complementare al prompt engineering: invece di concentrarsi su come formulare la richiesta, si occupa di *quali informazioni mettere a disposizione del modello prima* di chiederla. Per Claude Code CLI si concretizza in `CLAUDE.md`, Auto Memory e nella delega via subagent. Principio guida: "meglio poco contesto ben ordinato che tanto contesto caotico".

**Few-shot prompting** — Tecnica che insegna lo stile o il formato desiderato fornendo due o più esempi prima della richiesta vera e propria. Particolarmente efficace per voice consistency (FAQ, microcopy) e riproduzione di formati strutturati che è difficile descrivere a parole.

**Headless mode** — Esecuzione non-interattiva tramite flag `-p`. Claude riceve un prompt, produce output, esce. Usata per CI/CD e automazioni.

**Hook** — Script (bash, HTTP, prompt, agent o tool MCP) configurato in `settings.json` che intercetta eventi del lifecycle di Claude Code: `PreToolUse`, `PostToolUse`, `SessionStart`, `UserPromptSubmit`, e altri. Usato per validare, loggare, iniettare contesto o bloccare operazioni. Diverso da Subagent (esegue lavoro delegato) e da Skill (arricchisce il contesto del main agent): un Hook agisce **intorno** al main agent senza farne parte. Per la trattazione completa vedi sezione 13.

**Hope Coding** — Antipattern del prompt engineering: lanciare richieste generiche all'IA "sperando" che indovini cosa volevamo, senza specificare contesto, vincoli o formato di output. Produce risultati casuali e contrasta con il *Vibe coding consapevole* (vedi voce Vibe coding) basato su prompt strutturati.

**JSON-RPC** — Protocollo di comunicazione testuale (basato su JSON) per chiamate a procedure remote. È il livello-base su cui MCP impacchetta tutti i suoi messaggi tra client e server. Definisce richiesta, risposta e notifica con un formato standardizzato.

**MCP (Model Context Protocol)** — Protocollo aperto, open-sourced da Anthropic a novembre 2024, che standardizza il modo in cui un'applicazione AI (host) si connette a sorgenti di dati e tool esterni. Modello client-server basato su JSON-RPC 2.0; trasporto via stdio (locale) o HTTP+SSE (remoto). Tre primitive: tools, resources, prompts. Vedi capitolo 11 per la trattazione completa.

**MCP server** — Processo che implementa il protocollo MCP ed espone una o più funzionalità (tool, resource, prompt) a un host AI compatibile. Può essere scritto in qualsiasi linguaggio per cui esiste un SDK (Python, TypeScript, Java, C#, Rust, Kotlin, Swift). Tipicamente locale (stdio) per integrazioni personali, hostato (HTTP+SSE) per integrazioni di team.

**MCP tool** — Una delle tre primitive di un server MCP: funzione richiamabile esposta da un server. Ha nome, descrizione testuale leggibile dall'AI, schema JSON degli argomenti. Quando il modello decide di chiamarlo, l'host invia una richiesta `tools/call` JSON-RPC al server. È la primitiva più usata nei server MCP custom.

**MEMORY.md** — File-indice della Auto Memory di un progetto, posizionato in `~/.claude/projects/<project>/memory/`. Caricato a ogni sessione (limite ~200 righe, ~25 KB), elenca e descrive i topic file della cartella che vengono poi caricati on-demand quando il loro contenuto è rilevante.

**Meta-prompting** — Tecnica di prompt engineering che consiste nel chiedere all'IA stessa di scrivere il prompt da usare in una sessione successiva. Pattern: il modello, nel ruolo di "Expert Prompt Engineer", analizza specifiche grezze, fa domande di chiarimento, produce un prompt finale strutturato. Utile per task nuovi o complessi che valgono una formalizzazione.

**Native installer** — Metodo di installazione ufficiale introdotto da Anthropic nel 2025: un comando `curl` o `PowerShell` senza dipendenze da Node.js, con auto-update.

**OAuth** — Protocollo di autenticazione usato al primo avvio di `claude`. Apre il browser, logghi con l'account Anthropic, la sessione persiste.

**Panel of Experts (Tavola rotonda)** — Tecnica di prompt engineering che simula una discussione tra esperti virtuali, ognuno con un proprio punto di vista e area di competenza. Particolarmente preziosa per esplorare un'idea, mettere in discussione le proprie convinzioni, scegliere uno stack o stress-testare un'architettura: il valore non è nella sintesi finale ma nell'esplicitazione dei trade-off che ogni decisione comporta. Vedi sezione 6.4.3 per il prompt-template completo.

**Plan Mode** — Modalità read-only attivata via `/plan` o ciclando con `Shift+Tab` (che scorre tra `default → acceptEdits → plan → ...`). Claude analizza e propone un piano ma non modifica nulla finché non lo approvi.

**Plugin** — Pacchetto distribuito tramite marketplace che estende Claude Code con slash command, agent e skill. Gestiti con `claude plugin install`.

**Prompt engineering** — Disciplina di formulazione di richieste efficaci per un LLM. Si articola in quattro ingredienti fondamentali (contesto, task, vincoli, formato output) più uno opzionale (ruolo). Sui modelli di punta del 2026 il "role prompting" è ridimensionato a favore dei vincoli strutturali e dell'uso di delimitatori XML-like (`<contesto>`, `<task>`, `<vincoli>`, `<formato_output>`). Vedi sezione 6 per la trattazione completa.

**Prompt injection** — Attacco in cui istruzioni malevole vengono iniettate in file, commenti o risposte di servizi esterni per manipolare il comportamento dell'AI.

**REPL (Read-Eval-Print Loop)** — Ciclo interattivo leggi-esegui-stampa. La sessione interattiva di Claude Code è un REPL.

**Sessione** — Conversazione in corso con Claude Code, persistente tra i riavvii. Ogni sessione ha il proprio contesto e cronologia.

**Skill** — Modulo specializzato (cartella con `SKILL.md`) che Claude attiva automaticamente quando la descrizione della skill matcha il contesto del task. Non si invocano con slash command.

**Slash command** — Comando che inizia con `/` dentro una sessione interattiva (es. `/init`, `/compact`, `/plan`). Diversi dai flag di lancio che iniziano con `--`.

**Subagent** — Istanza isolata di Claude creata dal tool `Task` per eseguire ricerche o task specializzati senza "sporcare" il contesto della sessione principale.

**Token** — Unità di misura del testo per un LLM (approssimativamente 4 caratteri in inglese, un po' meno in italiano). I costi API sono calcolati in token di input e output. Claude Code usa token ogni volta che legge un file, riceve un prompt o produce una risposta.

**Vibe coding** — Termine diventato popolare nel 2024-2025 per descrivere lo stile di sviluppo AI-assistito: invece di scrivere codice manualmente, si scrive un prompt strutturato che descrive cosa deve fare, e l'AI genera l'implementazione.

**WSL2 (Windows Subsystem for Linux)** — Ambiente Linux integrato in Windows 10/11. Consigliato per usare Claude Code su Windows evitando molti problemi di compatibilità.

:::

---

## Allegato B — Fonti

Per approfondire o verificare specifiche aggiornate:

**Documentazione ufficiale Anthropic:**

- **Panoramica Claude Code**: https://docs.claude.com/en/docs/claude-code/overview
- **CLI reference**: https://code.claude.com/docs/en/cli-reference
- **Setup e installazione**: https://code.claude.com/docs/en/setup
- **Interactive mode e scorciatoie**: https://code.claude.com/docs/en/interactive-mode
- **Cheatsheet ufficiale**: https://support.claude.com/en/articles/14553413-claude-code-cheatsheet
- **Prompt engineering — best practices Claude 4**: https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices
- **Repository GitHub**: https://github.com/anthropics/claude-code
- **Pacchetto npm**: https://www.npmjs.com/package/@anthropic-ai/claude-code

**Risorse di prompt engineering e context engineering:**

- **Prompting Guide**: https://www.promptingguide.ai/
- **Elastic — Context engineering vs. prompt engineering**: https://www.elastic.co/search-labs/blog/context-engineering-vs-prompt-engineering

**Repository ufficiali di skill:**

- **Anthropic — Skills**: https://github.com/anthropics/skills
- **WordPress — Agent Skills**: https://github.com/WordPress/agent-skills
- **Vercel Labs — Agent Skills**: https://github.com/vercel-labs/agent-skills
- **Trail of Bits — Skills**: https://github.com/trailofbits/skills
- **Skills directory community**: https://skills.sh

**Risorse della community citate nella guida:**

- **Caveman skill (Julius Brussee)**: https://github.com/JuliusBrussee/caveman
- **Superpowers (Jesse Vincent)**: https://github.com/obra/superpowers

**MCP (Model Context Protocol) — fonti ufficiali:**

- **Documentazione MCP**: https://modelcontextprotocol.io/
- **Specifica del protocollo**: https://spec.modelcontextprotocol.io/
- **Anthropic — annuncio MCP (novembre 2024)**: https://www.anthropic.com/news/model-context-protocol
- **SDK Python ufficiale**: https://github.com/modelcontextprotocol/python-sdk
- **SDK TypeScript ufficiale**: https://github.com/modelcontextprotocol/typescript-sdk
- **Server MCP di riferimento (Anthropic)**: https://github.com/modelcontextprotocol/servers
- **MCP marketplace Anthropic**: https://www.anthropic.com/mcp
- **MCP marketplace community (Glama)**: https://glama.ai/mcp
- **MCP marketplace community (Smithery)**: https://smithery.ai/

**WordPress REST API — fonti ufficiali:**

- **REST API Handbook**: https://developer.wordpress.org/rest-api/
- **Application Passwords**: https://make.wordpress.org/core/2020/11/05/application-passwords-integration-guide/
- **REST API: posts endpoint**: https://developer.wordpress.org/rest-api/reference/posts/

---

## Note sull'autore {#chi-sono}

Mi chiamo **Maurizio Pelizzone**, sono Senior Software Architect, Co-titolare di **Mavida snc** (Torino) dal 2001 e formatore tecnico specializzato nell'ecosistema WordPress.

In oltre vent'anni ho progettato e portato in produzione più di 200 progetti web per clienti nazionali, specializzandomi in architetture WordPress enterprise, sviluppo plugin e temi custom, migrazioni di piattaforme legacy e ottimizzazione performance/security. Dal 2010 sono **Speaker ricorrente ai WordCamp italiani** (Milano, Bologna, Torino, WordCamp Italia), con talk su Custom Post Types, Hardening & Security, Solutions Architecture e Full Site Editing.

**Dal 2023 ho aggiunto un "superpotere" al mio workflow: l'Intelligenza Artificiale**, usandola come leva strategica per scrivere codice più pulito, scalabile e intelligente. Non come sostituto del mestiere, ma come amplificatore: vent'anni di PHP, WordPress e architetture software mi permettono di distinguere un suggerimento brillante da una scorciatoia rischiosa, e di dirigere l'AI verso soluzioni che reggono il peso della produzione.

Oggi affianco alla consulenza tecnica per PMI e aziende nazionali un'attività di **formazione su AI tools, prompt engineering, vibe coding e automazione con N8N**, convinto che la combinazione tra esperienza artigianale del codice e utilizzo consapevole dell'AI sia la direzione in cui il nostro mestiere sta evolvendo.

Questa guida nasce da quella convinzione: uno strumento come Claude Code non sostituisce lo sviluppatore, ma cambia il modo in cui lavora. Per usarlo bene servono le stesse virtù di sempre — rigore, curiosità, capacità di verificare — più un po' di disciplina nuova.

📧 maurizio@mavida.com — 🔗 [linkedin.com/in/mauriziopelizzone](https://www.linkedin.com/in/mauriziopelizzone/) — 🌐 [maurizio.mavida.com](https://maurizio.mavida.com)
