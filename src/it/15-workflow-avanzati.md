# Guida Pratica a Claude Code CLI

> **Versione 4.23 — maggio 2026** — verificata su Claude Code v2.1.123
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


---

> ← [14. Plugin](14-plugin.md) | [Index](README.md) | [16. Conclusioni](16-conclusioni.md) →
