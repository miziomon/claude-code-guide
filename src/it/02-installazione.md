# Guida Pratica a Claude Code CLI

> **Versione 4.30 — maggio 2026** — verificata su Claude Code v2.1.123
> Licenza [Creative Commons BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

> ← [1. Cos'è Claude Code](01-cosè-claude-code.md) | [Index](README.md) | [3. Il primo progetto end-to-end](03-primo-progetto.md) →

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


---

> ← [1. Cos'è Claude Code](01-cosè-claude-code.md) | [Index](README.md) | [3. Il primo progetto end-to-end](03-primo-progetto.md) →
