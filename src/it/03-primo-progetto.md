# Guida Pratica a Claude Code CLI

> **Versione 4.30 — maggio 2026** — verificata su Claude Code v2.1.123
> Licenza [Creative Commons BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

> ← [2. Installazione e setup](02-installazione.md) | [Index](README.md) | [4. Comandi e scorciatoie](04-comandi.md) →

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


---

> ← [2. Installazione e setup](02-installazione.md) | [Index](README.md) | [4. Comandi e scorciatoie](04-comandi.md) →
