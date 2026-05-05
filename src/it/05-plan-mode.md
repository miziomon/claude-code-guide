# Guida Pratica a Claude Code CLI

> **Versione 4.30 — maggio 2026** — verificata su Claude Code v2.1.123
> Licenza [Creative Commons BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

> ← [4. Comandi e scorciatoie](04-comandi.md) | [Index](README.md) | [6. Prompt engineering](06-prompt-engineering.md) →

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


---

> ← [4. Comandi e scorciatoie](04-comandi.md) | [Index](README.md) | [6. Prompt engineering](06-prompt-engineering.md) →
