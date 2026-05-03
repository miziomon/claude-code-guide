# Guida Pratica a Claude Code CLI

> **Versione 4.23 — maggio 2026** — verificata su Claude Code v2.1.123
> Licenza [Creative Commons BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

> [Index](README.md) | [Premessa](00-premessa.md) →

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


---

> [Index](README.md) | [Premessa](00-premessa.md) →
