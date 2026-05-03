# Guida Pratica a Claude Code CLI

> **Versione 4.23 — maggio 2026** — verificata su Claude Code v2.1.123
> Licenza [Creative Commons BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

> ← [13. Hook](13-hook.md) | [Index](README.md) | [15. Workflow avanzati](15-workflow-avanzati.md) →

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


---

> ← [13. Hook](13-hook.md) | [Index](README.md) | [15. Workflow avanzati](15-workflow-avanzati.md) →
