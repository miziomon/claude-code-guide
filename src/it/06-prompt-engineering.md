# Guida Pratica a Claude Code CLI

> **Versione 4.23 — maggio 2026** — verificata su Claude Code v2.1.123
> Licenza [Creative Commons BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

> ← [5. Plan Mode](05-plan-mode.md) | [Index](README.md) | [7. Memoria persistente](07-memoria.md) →

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


---

> ← [5. Plan Mode](05-plan-mode.md) | [Index](README.md) | [7. Memoria persistente](07-memoria.md) →
