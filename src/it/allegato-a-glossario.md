# Guida Pratica a Claude Code CLI

> **Versione 4.30 — maggio 2026** — verificata su Claude Code v2.1.123
> Licenza [Creative Commons BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

> ← [16. Conclusioni](16-conclusioni.md) | [Index](README.md) | [Allegato B — Fonti](allegato-b-fonti.md) →

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

**Guardrail** — Vincolo deterministico che vive *fuori* dal modello e limita le azioni di Claude indipendentemente da cosa il modello "decide". Non è un suggerimento nel system prompt (ottativo): è un cancello a valle della decisione. In Claude Code i guardrail si stratificano in quattro livelli: permessi dichiarativi (`settings.json`), hook programmatici (`PreToolUse`), modalità di esecuzione (Plan Mode, `--dangerously-skip-permissions`) e revisione umana. Il principio di taratura comune: il generatore non valida sé stesso. Vedi sezione 9 per la trattazione completa.

**Headless mode** — Esecuzione non-interattiva tramite flag `-p`. Claude riceve un prompt, produce output, esce. Usata per CI/CD e automazioni.

**Hook** — Script (bash, HTTP, prompt, agent o tool MCP) configurato in `settings.json` che intercetta eventi del lifecycle di Claude Code: `PreToolUse`, `PostToolUse`, `SessionStart`, `UserPromptSubmit`, e altri. Usato per validare, loggare, iniettare contesto o bloccare operazioni. Diverso da Subagent (esegue lavoro delegato) e da Skill (arricchisce il contesto del main agent): un Hook agisce **intorno** al main agent senza farne parte. Per la trattazione completa vedi sezione 13.

**Hope Coding** — Antipattern del prompt engineering: lanciare richieste generiche all'IA "sperando" che indovini cosa volevamo, senza specificare contesto, vincoli o formato di output. Produce risultati casuali e contrasta con il *Vibe coding consapevole* (vedi voce Vibe coding) basato su prompt strutturati.

**JSON-RPC** — Protocollo di comunicazione testuale (basato su JSON) per chiamate a procedure remote. È il livello-base su cui MCP impacchetta tutti i suoi messaggi tra client e server. Definisce richiesta, risposta e notifica con un formato standardizzato.

**MAX_THINKING_TOKENS** — Variabile d'ambiente che limita il budget di token riservato all'extended thinking (ragionamento interno) del modello. Di default è illimitato; impostandola (es. `MAX_THINKING_TOKENS=8000`) si riduce il costo dei token di output su sessioni non critiche. Citata nel §8.10 nel contesto dell'ottimizzazione del consumo.

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

**PostToolUse** — Evento del lifecycle hook che si attiva **dopo** che un tool ha completato la propria esecuzione. A differenza di `PreToolUse`, non può bloccare l'azione (già avvenuta), ma può loggare risultati, filtrare output rumorosi prima che arrivino al modello, o scatenare operazioni di follow-up (es. linting, audit log). Vedi esempi B ed F in §13.6.

**PreCompact** — Evento del lifecycle hook che si attiva immediatamente **prima** che la compaction `/compact` (automatica o manuale) comprima il transcript della sessione. Consente di salvare il transcript completo prima che il sommario lo sostituisca. Vedi Esempio E in §13.6.

**PreToolUse** — Evento del lifecycle hook che si attiva **prima** che un tool venga eseguito. Può bloccare l'operazione (exit 2 con messaggio in stderr) o modificare gli argomenti. È l'unico evento con potere di veto reale: usato per regole di sicurezza (es. blocco di `rm -rf` su path critici). Vedi Esempio A in §13.6.

**Prompt cache** — Meccanismo di Anthropic che conserva i prefissi stabili del prompt (tool MCP, system prompt, messaggi iniziali) tra turni successivi. Riduce il costo dei token di input fino al 90% per i blocchi già cachati. La cache ha un TTL di 5 minuti (default) o 1 ora (opt-in). La gerarchia di prefisso segue l'ordine: tools → system → messages. Monitorabile via `/cost` leggendo `cache_read_input_tokens` vs `cache_creation_input_tokens`. Vedi §8.10.

**Prompt engineering** — Disciplina di formulazione di richieste efficaci per un LLM. Si articola in quattro ingredienti fondamentali (contesto, task, vincoli, formato output) più uno opzionale (ruolo). Sui modelli di punta del 2026 il "role prompting" è ridimensionato a favore dei vincoli strutturali e dell'uso di delimitatori XML-like (`<contesto>`, `<task>`, `<vincoli>`, `<formato_output>`). Vedi sezione 6 per la trattazione completa.

**Prompt injection** — Attacco in cui istruzioni malevole vengono iniettate in file, commenti o risposte di servizi esterni per manipolare il comportamento dell'AI.

**REPL (Read-Eval-Print Loop)** — Ciclo interattivo leggi-esegui-stampa. La sessione interattiva di Claude Code è un REPL.

**Sessione** — Conversazione in corso con Claude Code, persistente tra i riavvii. Ogni sessione ha il proprio contesto e cronologia.

**SessionStart** — Evento del lifecycle hook che si attiva all'avvio di una sessione (matcher `startup`) o alla ripresa di una sessione esistente (matcher `resume`). Tipicamente usato per iniettare contesto iniziale, reminder dinamici o stati di sistema (branch corrente, variabili di progetto). Vedi Esempio D in §13.6.

**Skill** — Modulo specializzato (cartella con `SKILL.md`) che Claude attiva automaticamente quando la descrizione della skill matcha il contesto del task. Non si invocano con slash command.

**Slash command** — Comando che inizia con `/` dentro una sessione interattiva (es. `/init`, `/compact`, `/plan`). Diversi dai flag di lancio che iniziano con `--`.

**Subagent** — Istanza isolata di Claude creata dal tool `Task` per eseguire ricerche o task specializzati senza "sporcare" il contesto della sessione principale.

**Token** — Unità di misura del testo per un LLM (approssimativamente 4 caratteri in inglese, un po' meno in italiano). I costi API sono calcolati in token di input e output. Claude Code usa token ogni volta che legge un file, riceve un prompt o produce una risposta.

**Transcript** — Il log testuale completo di una sessione Claude Code: tutti i messaggi utente, le risposte del modello e gli output dei tool. Il transcript cresce a ogni turno e costituisce il principale responsabile della crescita del contesto. La compaction via `/compact` lo sostituisce con un sommario; gli hook `PreCompact` possono salvarlo prima che ciò avvenga. Vedi §13.6 Esempio E.

**UserPromptSubmit** — Evento del lifecycle hook che si attiva ogni volta che l'utente invia un messaggio. Può filtrare, arricchire o bloccare il prompt prima che raggiunga il modello. Vedi §13.4.

**Vibe coding** — Termine diventato popolare nel 2024-2025 per descrivere lo stile di sviluppo AI-assistito: invece di scrivere codice manualmente, si scrive un prompt strutturato che descrive cosa deve fare, e l'AI genera l'implementazione.

**WSL2 (Windows Subsystem for Linux)** — Ambiente Linux integrato in Windows 10/11. Consigliato per usare Claude Code su Windows evitando molti problemi di compatibilità.

:::

---


---

> ← [16. Conclusioni](16-conclusioni.md) | [Index](README.md) | [Allegato B — Fonti](allegato-b-fonti.md) →
