# wordpress-publisher-mcp

Server MCP che espone tre tool a Claude Code per pubblicare contenuti su WordPress via REST API.

Estratto dalla **Guida Pratica a Claude Code CLI**, capitolo 11.5.
Repository della guida: https://github.com/miziomon/claude-code-guide

## Tool esposti

| Tool | Descrizione |
|------|-------------|
| `wp_create_post` | Crea un articolo (bozza o pubblicato) con titolo, contenuto e categorie |
| `wp_publish_post` | Promuove una bozza esistente a stato "publish" |
| `wp_list_categories` | Elenca tutte le categorie del sito con id, name, slug, count |

## Prerequisiti

1. **WordPress 5.0+** con REST API attiva (default da WP 5.0)
2. **Application Password** generata dal profilo utente WordPress:
   - Dashboard → Utenti → Il tuo profilo → Application Passwords
   - Dai un nome all'app (es. "Claude Code") e clicca "Aggiungi"
   - Copia la password generata (formato: `xxxx xxxx xxxx xxxx xxxx xxxx`)
3. **Python 3.11+**

## Installazione

```bash
# Clona o copia questa cartella, poi:
pip install -e .

# Oppure senza pyproject.toml:
pip install mcp httpx python-dotenv
```

## Configurazione

```bash
cp .env.example .env
# Modifica .env con URL, username e Application Password del tuo sito
```

## Registrazione in Claude Code

Aggiungi al file `.claude/settings.json` del tuo progetto (o a quello globale in `~/.claude/settings.json`):

```json
{
  "mcpServers": {
    "wordpress-publisher": {
      "command": "python",
      "args": ["/percorso/assoluto/verso/server.py"]
    }
  }
}
```

Sostituisci `/percorso/assoluto/verso/server.py` con il percorso reale sulla tua macchina.

## Test

1. Avvia Claude Code nella directory del tuo progetto
2. Esegui `/mcp` — deve apparire `wordpress-publisher` con i tre tool
3. Prova: `elenca le categorie del mio sito`

## Sicurezza

- Non committare mai il file `.env` reale (è già in `.gitignore` se usi il repo della guida)
- L'Application Password si revoca dalla dashboard WordPress senza toccare la password principale
- Usa un utente WordPress con permessi minimi (solo "Autore" se non devi pubblicare direttamente)
