# Guida Pratica a Claude Code CLI

> **Versione 4.30 — maggio 2026** — verificata su Claude Code v2.1.123
> Licenza [Creative Commons BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

> ← [14. Plugin](14-plugin.md) | [Index](README.md) | [16. Conclusioni](16-conclusioni.md) →

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

Puoi creare slash command personalizzati salvando file Markdown in `.claude/commands/`. Il file diventa il prompt che Claude esegue quando invochi il comando.

#### Struttura di un file comando

```markdown
---
description: Breve descrizione che appare nel picker (max ~80 char)
allowed-tools: Read, Bash, Glob
argument-hint: "[area-da-analizzare]"
---

Qui il prompt del comando. Puoi usare $ARGUMENTS per riferire l'eventuale
argomento passato (es. /security-audit src/auth).
```

Il **frontmatter YAML** è opzionale ma consigliato:

- `description` — appare nel picker `/` e nel listing dei comandi disponibili.
- `allowed-tools` — lista di tool che il comando può usare. Se omessa, tutti i tool sono disponibili.
- `argument-hint` — stringa visualizzata nel picker come suggerimento per l'argomento.

#### Esempio base: audit di sicurezza

```markdown
<!-- .claude/commands/security-audit.md -->
---
description: Audit OWASP top-10 per il codice PHP del plugin
allowed-tools: Read, Grep, Glob
---
Esegui un audit di sicurezza focalizzato su:
1. SQL injection nelle query dirette
2. XSS negli output non escaped
3. CSRF senza nonce verification
4. Path traversal nelle operazioni filesystem
5. Credenziali hardcoded

Per ogni issue trovata: file, riga, severity (low/medium/high/critical),
fix suggerito.
```

#### Ricetta: `/audit-context` — snapshot del consumo prima di un task pesante

```markdown
<!-- .claude/commands/audit-context.md -->
---
description: Snapshot contesto: uso token, dimensioni config, server MCP attivi
allowed-tools: Bash
---
Esegui in sequenza:
1. /context per mostrare l'uso attuale del contesto per categoria.
2. /cost per mostrare i token consumati e il costo stimato della sessione.
3. wc -l CLAUDE.md .claude/settings.json 2>/dev/null per mostrare le dimensioni
   dei file di configurazione del progetto.

Poi riepiloga in tre righe: percentuale di contesto usata, voci più pesanti,
e se c'è qualcosa da fare prima di continuare (compattare, disabilitare un
server MCP inutilizzato, ecc.).
```

Da sessione: `/audit-context` ti dà in pochi secondi il quadro completo prima di iniziare un task pesante. Equivalente al check preventivo descritto in [sezione 8.4](#il-comando-context-leggere-ed-agire), ma on-demand e con la sintesi finale prodotta dal modello.

#### Ricetta: `/snapshot` — preservare lo stato prima di compattare

```markdown
<!-- .claude/commands/snapshot.md -->
---
description: Salva un brief della sessione in docs/snapshots/ prima di /compact
allowed-tools: Bash, Write
---
Prima di procedere con /compact o /clear, crea uno snapshot testuale dello
stato attuale della sessione.

1. Elenca i file modificati: git diff --name-only HEAD (o git status --short).
2. Riepiloga in massimo 10 bullet le decisioni architetturali prese, i problemi
   risolti, e i task ancora aperti.
3. Scrivi il riassunto in docs/snapshots/ con nome snapshot-YYYYMMDD-HHMM.md.

Il file di snapshot serve come brief per la sessione successiva che riprende
questo lavoro con --resume. Tienilo conciso: 200-300 parole, bullet point,
niente introduzioni.
```

Da sessione: `/snapshot` seguito da `/compact` è la sequenza che preserva i dettagli chiave senza tenere tutto il transcript in contesto. La prossima sessione `--resume` trova il brief pronto in `docs/snapshots/`.

> **Slash command vs hook.** I custom slash command sono **on-demand**: li invochi tu quando servono. Gli hook (cap. 13) sono **automatici**: scattano su eventi del lifecycle indipendentemente dalla tua decisione. Per esempio, il backup transcript dell'[Esempio E](#esempio-e--backup-transcript-prima-di-compact) in cap. 13 è complementare a `/snapshot`: l'hook salva automaticamente, lo slash command produce un sommario leggibile.

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


---

> ← [14. Plugin](14-plugin.md) | [Index](README.md) | [16. Conclusioni](16-conclusioni.md) →
