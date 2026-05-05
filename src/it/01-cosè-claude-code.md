# Guida Pratica a Claude Code CLI

> **Versione 4.30 — maggio 2026** — verificata su Claude Code v2.1.123
> Licenza [Creative Commons BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

> ← [Premessa](00-premessa.md) | [Index](README.md) | [2. Installazione e setup](02-installazione.md) →

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


---

> ← [Premessa](00-premessa.md) | [Index](README.md) | [2. Installazione e setup](02-installazione.md) →
