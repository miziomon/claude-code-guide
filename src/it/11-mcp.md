# Guida Pratica a Claude Code CLI

> **Versione 4.23 — maggio 2026** — verificata su Claude Code v2.1.123
> Licenza [Creative Commons BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

> ← [10. Skill](10-skill.md) | [Index](README.md) | [12. Subagent](12-subagent.md) →

---

## 11. MCP: integrare servizi esterni

Il **Model Context Protocol (MCP)** è il modo in cui Claude Code parla con sistemi esterni — API, database, servizi SaaS, file system fuori dalla working directory. Mentre le skill (cap. 10) estendono cosa Claude *sa fare* con istruzioni e codice locali, MCP estende a quali sistemi *si può collegare*. Per il confronto rapido fra i meccanismi di estensione vedi la mappa in [14.1](#meccanismi-di-estensione-di-claude-code-una-mappa).

### 11.1 Cos'è MCP e perché esiste

**Model Context Protocol (MCP)** è un protocollo aperto, open-sourced da Anthropic a novembre 2024, che standardizza il modo in cui un'applicazione AI (l'**host**) si connette a sorgenti di dati e strumenti esterni — file di un sistema, database, API di servizi, repository git, calendari, ticket system, qualunque cosa sia raggiungibile via codice.

L'idea è semplice e nasce da un problema concreto. Prima di MCP, ogni IDE AI (Claude Code, Cursor, Continue, ChatGPT desktop, Cline, decine d'altri) aveva il proprio meccanismo per connettersi a GitHub, Postgres, Slack, ecc. Per chi sviluppava un'integrazione, questo significava scriverla N volte — una per ogni client. Per chi usava più strumenti, ogni client aveva una matrice di connettori incompatibili tra loro: l'integrazione GitHub di Cursor non funzionava in Claude Code, e viceversa.

MCP risolve questo problema con la stessa logica con cui USB-C ha sostituito le decine di connettori proprietari: definisce **un protocollo standard** tra client (host AI) e server (l'integrazione). Chi scrive un'integrazione la scrive una volta, e funziona ovunque MCP è supportato. Anthropic ha rilasciato gli SDK ufficiali (Python, TypeScript, Java, C#, Rust, Kotlin, Swift) e una decina di server di riferimento per i casi d'uso più comuni (filesystem, fetch HTTP, GitHub, Postgres, SQLite, Puppeteer, Slack, Brave Search).

A maggio 2026 l'adozione è ampia: **Claude Code, Cursor, Windsurf, Cline, Continue, GitHub Copilot e diversi altri client supportano MCP** in modo nativo. Esistono centinaia di server community sui registry pubblici, e marketplace dedicati ([anthropic.com/mcp](https://anthropic.com/mcp), [glama.ai/mcp](https://glama.ai/mcp), [smithery.ai](https://smithery.ai)). Il protocollo è arrivato alla versione stabile 1.0 dopo le iterazioni del 2025.

Per chi scrive in italiano: pensare a MCP come al **driver standard tra Claude Code e il resto del mondo**. Se vuoi che Claude faccia qualcosa che non sa fare nativamente — leggere il tuo CRM, postare su WordPress, interrogare una base dati interna — la risposta moderna è: scrivi un server MCP (o trova quello che fa già al caso tuo) e lo registri.

### 11.2 Architettura del protocollo

MCP è un protocollo **client-server** basato su **JSON-RPC 2.0**. Tre i componenti principali:

- **Host** — l'applicazione AI dell'utente (per noi: Claude Code). Non parla direttamente coi server MCP: usa uno o più *client*.
- **Client** — una connessione 1:1 verso un singolo server. Claude Code crea un client per ogni server MCP configurato. Il client gestisce la connessione (avvio del processo, scambio messaggi, lifecycle) e isola il server dal resto dell'host.
- **Server** — il processo che espone funzionalità. Può essere scritto in qualsiasi linguaggio per cui esiste un SDK MCP (Python, TypeScript, Rust, Java, C#, Swift, Kotlin sono tutti supportati ufficialmente). Comunica con il client tramite uno standard di trasporto.

```
┌──────────────────────────────────────────────────────────┐
│                    HOST (Claude Code)                    │
│                                                          │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐              │
│  │ Client A │   │ Client B │   │ Client C │              │
│  └────┬─────┘   └────┬─────┘   └────┬─────┘              │
└───────┼──────────────┼──────────────┼────────────────────┘
        │ stdio        │ stdio        │ HTTP+SSE
        │              │              │
┌───────▼──────┐ ┌─────▼──────┐ ┌────▼─────────────────┐
│  Server WP   │ │   Server   │ │  Server cloud        │
│  (Python loc)│ │  Postgres  │ │  (Linear / Notion)   │
└──────────────┘ └────────────┘ └──────────────────────┘
```

**Trasporti** — due modalità principali:

- **stdio** (input/output standard) — il client lancia il server come sotto-processo e comunica via stdin/stdout. È il transport più comune per server locali (filesystem, database, processi nostri). Semplice, sicuro per default (resta nel sistema utente), niente rete da gestire.
- **HTTP+SSE** (Server-Sent Events) — server raggiungibili via HTTP. È usato per server ospitati (cloud) o condivisi tra client diversi. Richiede gestione di auth e considerazioni di latenza che non si pongono per stdio. La guida si concentra sui server stdio locali; i server remoti li accenneremo nella sezione 11.6.

**Capability negotiation** — all'avvio della sessione, client e server si scambiano un handshake (`initialize`) in cui dichiarano cosa supportano: il server elenca i suoi tool, le sue resource, i suoi prompt; il client elenca le proprie capability (es. supporto a sampling, logging). Da quel punto in avanti la conversazione è un'alternanza di richieste JSON-RPC.

Le **tre primitive** di un server MCP:

- **Tools** — funzioni che il server espone e che Claude può invocare. Ognuno ha un nome (`wp_create_post`), una descrizione testuale leggibile dall'AI, e uno schema JSON degli argomenti. Quando Claude decide di chiamarlo, manda una richiesta `tools/call`, il server esegue, restituisce il risultato. È la primitiva più usata.
- **Resources** — dati indirizzabili via URI (`wp://posts/123`, `file:///etc/hosts`). Il server li espone come "biblioteca" da cui Claude può leggere. Resource ≠ Tools: leggere una resource è una pura GET, non ha effetti collaterali.
- **Prompts** — template di prompt riutilizzabili che il server può fornire all'utente come "preset". Tipicamente esposti come comando `/server-name:prompt-name` nell'host.

Per il nostro esempio WordPress useremo solo i **tools** (creazione/aggiornamento post, lista categorie). Tools sono la parte più produttiva del protocollo; resources e prompts sono utili ma meno comuni nei server custom.

### 11.3 Configurare un server MCP esistente

La configurazione è dichiarativa: si elenca il server in un JSON e Claude Code lo lancia in automatico all'avvio della sessione. Due scope:

- **`.claude/settings.json`** del progetto — il server è disponibile solo dentro quel progetto. Adatto a integrazioni progetto-specifiche (un server per parlare col DB di staging del cliente).
- **`~/.claude/settings.json`** dell'utente — il server è disponibile in ogni sessione dell'utente. Adatto a integrazioni globali (il tuo server MCP per il proprio CRM aziendale).

Esempio di configurazione di tre server contemporaneamente (un GitHub e due locali):

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
      }
    },
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/maurizio/progetti"
      ]
    },
    "postgres": {
      "command": "uvx",
      "args": [
        "mcp-server-postgres",
        "postgresql://localhost/staging_db"
      ]
    }
  }
}
```

Punti chiave:

- **`command` + `args`** — eseguibile e argomenti. `npx -y` è il pattern standard per server distribuiti su npm (li scarica al volo). Per Python si usa tipicamente `uvx` o `python -m`.
- **`env`** — variabili d'ambiente passate al server. Le interpolazioni `${VAR}` sono risolte dalla shell che ha lanciato Claude Code: il modo corretto di passare segreti è metterli in `.env`/`.envrc` ed esportarli prima di lanciare Claude, non hardcodarli nel JSON committato.
- **Niente segreti in repo** — un `mcpServers` entry committato che contiene un token in chiaro è un incidente di sicurezza in attesa. Sempre `${VAR}` con segreti caricati esternamente.

**Slash command e CLI dedicati.** Una volta configurato un server, Claude Code lo gestisce con questi comandi:

```bash
# Slash command interno (in sessione interattiva)
/mcp                       # elenco server attivi e loro tool

# CLI esterna
claude mcp list            # stesso elenco da terminale
claude mcp add <name>      # aggiunge un server (intervista guidata)
claude mcp remove <name>   # lo rimuove
```

**Debug.** Se un server non parte (errore di avvio, dipendenza mancante, env var non risolta), Claude Code stampa l'errore al lancio della sessione e marca il server come "disconnected" in `/mcp`. Per inseguire problemi più sottili, lanciare il server manualmente da terminale ed esercitarlo via stdin con qualche `echo '{"jsonrpc":"2.0","method":"initialize",...}'` — la documentazione MCP ha esempi precisi.

### 11.4 Server MCP utili: una selezione curata

A maggio 2026 l'ecosistema MCP è vasto. Una selezione di server con cui vale la pena familiarizzare:

- **`@modelcontextprotocol/server-github`** — gestione completa di repository, issue, PR, action. È il primo MCP da installare per chi sviluppa su GitHub. Ufficiale, manutenuto da Anthropic.
- **`@modelcontextprotocol/server-filesystem`** — accesso controllato a directory specifiche del filesystem. Utile per lavorare su progetti fuori dalla working directory di Claude Code (es. leggere documentazione in `~/Documents/specs`). I path autorizzati sono passati come argomenti.
- **`mcp-server-postgres`** / **`mcp-server-sqlite`** — query, schema inspection, generazione di migration. Ottimi per esplorare basi dati di staging senza permessi di scrittura sul prod.
- **`@modelcontextprotocol/server-puppeteer`** — automazione browser headless: screenshot, scraping, click test. Coppia molto bene con la skill `webapp-testing` (cap. 10).
- **`mcp-server-slack`** — invio di messaggi e lettura di canali, utile per notifiche di completamento di task lunghi o report automatici.
- **`mcp-server-sentry`** — accesso ai dati di error tracking; può recuperare lo stack trace di un'eccezione recente e darlo a Claude per il bug fix. Coppia con cap. 15.2 (Bug hunting con TDD).
- **`mcp-server-linear`** / **`mcp-server-notion`** — ticket system e knowledge base. Permettono a Claude di leggere il contesto di un task da Linear e produrre il PR collegato.

I marketplace della community ne hanno centinaia altri: prima di scrivere un MCP da zero, cercare se esiste già un server adatto. La regola è: **MCP esistente > MCP custom > skill > script locale**, in ordine di preferenza per soluzioni nuove.

### 11.5 Creare un server MCP da zero: pubblicare su WordPress

Caso d'uso: vogliamo che Claude Code possa **pubblicare contenuti su un sito WordPress** senza dover aprire la dashboard wp-admin. Lo scenario tipico: stai discutendo con Claude un articolo (lo scrivi in Markdown, lui ti suggerisce taglio editoriale), e vuoi chiudere la sessione con *"pubblica questo articolo come bozza nella categoria 'Tutorial'"*. Senza MCP, Claude può tutt'al più dirti "ecco i passaggi da fare in admin". Con MCP, lo fa lui.

#### Prerequisiti

1. Un sito WordPress con REST API attiva (default da WP 5.0+).
2. Un'**Application Password** generata dal profilo utente WordPress (utente → modifica profilo → "Application Passwords"). È una password monouso, lunga, separata dalla password principale: si revoca senza dover cambiare la password vera.
3. **Python 3.10+** e l'SDK ufficiale: `pip install mcp httpx python-dotenv`.

#### Struttura del progetto

```
~/mcp/wordpress-publisher/
├── server.py
├── pyproject.toml
└── .env
```

`.env` (mai committare):

```
WP_BASE_URL=https://miosito.example.com
WP_USERNAME=maurizio
WP_APP_PASSWORD=xxxx xxxx xxxx xxxx xxxx xxxx
```

#### Codice del server (`server.py`)

```python
"""
Server MCP che pubblica articoli su WordPress via REST API.
Tre tool esposti:
  - wp_create_post     : crea una bozza (o pubblica direttamente)
  - wp_publish_post    : promuove una bozza esistente a "publish"
  - wp_list_categories : elenca le categorie del sito
"""

import os
import base64
import httpx
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

# Carica le credenziali da .env (mai hardcodare in repo)
load_dotenv()
BASE_URL = os.environ["WP_BASE_URL"].rstrip("/")
USERNAME = os.environ["WP_USERNAME"]
APP_PASS = os.environ["WP_APP_PASSWORD"]

# Auth Basic con Application Password (formato standard WP)
auth_token = base64.b64encode(
    f"{USERNAME}:{APP_PASS}".encode("utf-8")
).decode("ascii")
HEADERS = {
    "Authorization": f"Basic {auth_token}",
    "Content-Type": "application/json",
}

# Istanza FastMCP: il server si chiamerà "wordpress-publisher"
mcp = FastMCP("wordpress-publisher")


@mcp.tool()
def wp_create_post(
    title: str,
    content: str,
    status: str = "draft",
    categories: list[int] | None = None,
) -> dict:
    """
    Crea un nuovo articolo su WordPress.

    Args:
        title:      titolo del post
        content:    corpo HTML o Gutenberg-block
        status:     "draft" (default) o "publish"
        categories: lista di ID categoria (opzionale)

    Returns:
        Dict con id, status, link, modified del post creato.
    """
    payload = {"title": title, "content": content, "status": status}
    if categories:
        payload["categories"] = categories

    response = httpx.post(
        f"{BASE_URL}/wp-json/wp/v2/posts",
        headers=HEADERS,
        json=payload,
        timeout=30.0,
    )
    response.raise_for_status()
    data = response.json()
    return {
        "id": data["id"],
        "status": data["status"],
        "link": data["link"],
        "modified": data["modified"],
    }


@mcp.tool()
def wp_publish_post(post_id: int) -> dict:
    """
    Promuove una bozza esistente a stato "publish".

    Args:
        post_id: ID del post da pubblicare

    Returns:
        Dict con id, status, link aggiornato.
    """
    response = httpx.post(
        f"{BASE_URL}/wp-json/wp/v2/posts/{post_id}",
        headers=HEADERS,
        json={"status": "publish"},
        timeout=30.0,
    )
    response.raise_for_status()
    data = response.json()
    return {
        "id": data["id"],
        "status": data["status"],
        "link": data["link"],
    }


@mcp.tool()
def wp_list_categories() -> list[dict]:
    """
    Elenca tutte le categorie del sito.

    Returns:
        Lista di dict con id, name, slug, count per ogni categoria.
    """
    response = httpx.get(
        f"{BASE_URL}/wp-json/wp/v2/categories",
        headers=HEADERS,
        params={"per_page": 100},
        timeout=30.0,
    )
    response.raise_for_status()
    return [
        {"id": c["id"], "name": c["name"], "slug": c["slug"], "count": c["count"]}
        for c in response.json()
    ]


if __name__ == "__main__":
    # Avvio del server in modalità stdio (default per MCP locali)
    mcp.run()
```

#### Registrazione in Claude Code

Aggiungere al proprio `.claude/settings.json` (o a quello globale):

```json
{
  "mcpServers": {
    "wordpress-publisher": {
      "command": "python",
      "args": ["/Users/maurizio/mcp/wordpress-publisher/server.py"]
    }
  }
}
```

#### Test interattivo

Lanciare Claude Code, eseguire `/mcp` per verificare che il server `wordpress-publisher` sia connesso e che mostri tre tool. Poi una conversazione tipica:

> **Tu**: ho appena finito di scrivere un articolo su Plan Mode, lo trovi in `articolo-plan-mode.md`. Pubblicalo come bozza nella categoria "Tutorial".
>
> **Claude**: Leggo prima il file per estrarne titolo e contenuto.
> *[Read articolo-plan-mode.md]*
> Ho letto l'articolo: 1840 parole, titolo *"Plan Mode: pensare prima di scrivere"*. Recupero gli ID delle categorie per trovare "Tutorial".
> *[wp_list_categories]*
> Categoria "Tutorial" ha ID **7**. Procedo con la creazione della bozza.
> *[wp_create_post(title=..., content=..., status="draft", categories=[7])]*
> ✓ Bozza creata. ID **142**, link [https://miosito.example.com/?p=142&preview=true](https://...). Vuoi che la pubblichi adesso o resta bozza per la revisione?
>
> **Tu**: Lasciala in bozza, devo riguardare le immagini.

#### Cosa succede sotto il cofano

Claude Code ha:

1. Letto `articolo-plan-mode.md` con il proprio tool nativo Read.
2. Capito che serviva l'ID categoria — ha chiamato `wp_list_categories` (un tool MCP).
3. Cercato "Tutorial" tra le categorie restituite e estratto l'ID 7.
4. Chiamato `wp_create_post` con titolo, contenuto e categorie.
5. Riportato l'esito con il link di anteprima.

Tutto via JSON-RPC tra il client (Claude Code) e il nostro server Python che gira come sotto-processo locale. Niente hop di rete sui dati sensibili — solo le richieste HTTPS al server WordPress, esattamente come se l'utente le avesse fatte da un client REST.

#### Estensioni naturali

Da questo scheletro è facile crescere:

- aggiungere `wp_upload_media` per caricare immagini in libreria;
- aggiungere `wp_list_drafts` per recuperare bozze esistenti;
- aggiungere `wp_schedule_post` per pubblicazioni schedulate (`status: "future"` con `date`);
- esporre le categorie e i post come **resources** (URI `wp://categories`, `wp://posts/{id}`) per dare a Claude visibilità del catalogo senza dover invocare un tool ogni volta.

Per chi viene dal mondo plugin WordPress: questo server MCP è in pratica un **client REST lato AI**. Tutto quello che il tuo plugin può fare via API REST, il tuo MCP può esporlo come tool.

### 11.6 Sicurezza e considerazioni operative

Tre punti d'attenzione che separano un server MCP da un esperimento e un server MCP pronto per il mestiere.

**Nessuna sandbox automatica.** Un server MCP gira come *te*: ha le tue credenziali file system, accesso alla rete, e i token che gli passi via env. Niente lo isola dal resto del sistema. Conseguenze pratiche:

- **Audita il codice** prima di installare server MCP di terzi, specialmente se ottenuti da marketplace meno presidiate. Un server malevolo può leggerti il `~/.ssh` o esfiltrare segreti dalle env.
- **Mantieni i tuoi server MCP custom in repo che controlli**, non come dipendenze npx anonime.
- **Usa Application Password / API key con scope minimo**, mai la password personale principale. Le revochi con un click se serve.

**Permission deny per i tool sensibili.** I tool MCP confluiscono nel sistema dei permessi di Claude Code (cap. 9). Per server con tool rischiosi (cancellare post, eseguire query DELETE) vale la pena denylistare i tool distruttivi in `permissions.deny`:

```json
{
  "permissions": {
    "deny": [
      "mcp__wordpress-publisher__wp_delete_post",
      "mcp__postgres__query_write"
    ]
  }
}
```

Il pattern `mcp__<server>__<tool>` permette di colpire con precisione il tool che non vuoi auto-approvato; Claude continuerà a chiedere conferma esplicita ad ogni invocazione.

**Logging e audit.** Per capire cosa il tuo MCP sta davvero combinando in produzione, accoppia un **hook PostToolUse** (cap. 13) che logga ogni invocazione di tool MCP in JSON Lines. Patterns concreti nel cap. 13.6 (esempio B). Effetto: tracciabilità totale di chi (utente, modello), cosa (quale tool MCP), quando e con quali argomenti.

**MCP remoti.** I server raggiunti via HTTP+SSE (server hostati, condivisi tra team) aggiungono una dimensione: latenza e auth di rete. Per integrazioni stabili a livello di team conviene un server hostato; per sperimentazione e per integrazioni personali stdio locale è più semplice e più sicuro per default. Il protocollo è lo stesso, cambia solo il transport.

**Quando NON serve un MCP.** Se il task è puramente locale (lettura di un file, esecuzione di uno script), Claude Code ha già Read/Write/Bash come tool nativi: scriversi un MCP per fare quello che già fa Bash è overkill. La regola è: **MCP per servizi esterni o protocolli di rete; tool nativi per il sistema utente locale**. In dubbio, prima skill (cap. 10) o slash command custom; MCP solo quando si tratta di un sistema esterno con cui Claude deve dialogare via API.

---


---

> ← [10. Skill](10-skill.md) | [Index](README.md) | [12. Subagent](12-subagent.md) →
