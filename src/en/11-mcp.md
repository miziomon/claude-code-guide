# Practical Guide to Claude Code CLI

> **Version 4.30 — May 2026** — verified on Claude Code v2.1.123
> Licensed under [Creative Commons BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

> ← [10. Skills](10-skills.md) | [Index](README.md) | [12. Subagents](12-subagents.md) →

---

## 11. MCP: integrating external services

The **Model Context Protocol (MCP)** is the way Claude Code talks to external systems — APIs, databases, SaaS services, file systems outside the working directory. While skills (chapter 10) extend what Claude *knows how to do* with local instructions and code, MCP extends *which systems it can connect to*. For a quick comparison between the extension mechanisms, see the map in [14.1](#claude-codes-extension-mechanisms-a-map).

### 11.1 What MCP is and why it exists

**Model Context Protocol (MCP)** is an open protocol, open-sourced by Anthropic in November 2024, that standardizes the way an AI application (the **host**) connects to external data sources and tools — files of a system, databases, service APIs, git repositories, calendars, ticket systems, anything reachable via code.

The idea is simple and arises from a concrete problem. Before MCP, every AI IDE (Claude Code, Cursor, Continue, ChatGPT desktop, Cline, dozens of others) had its own mechanism to connect to GitHub, Postgres, Slack, etc. For those developing an integration, this meant writing it N times — one for each client. For those using multiple tools, every client had a matrix of incompatible connectors: Cursor's GitHub integration didn't work in Claude Code, and vice versa.

MCP solves this problem with the same logic with which USB-C replaced dozens of proprietary connectors: it defines **a standard protocol** between client (AI host) and server (the integration). Whoever writes an integration writes it once, and it works wherever MCP is supported. Anthropic released the official SDKs (Python, TypeScript, Java, C#, Rust, Kotlin, Swift) and a dozen reference servers for the most common use cases (filesystem, HTTP fetch, GitHub, Postgres, SQLite, Puppeteer, Slack, Brave Search).

By May 2026 adoption is widespread: **Claude Code, Cursor, Windsurf, Cline, Continue, GitHub Copilot, and several other clients support MCP** natively. There are hundreds of community servers in public registries, and dedicated marketplaces ([anthropic.com/mcp](https://anthropic.com/mcp), [glama.ai/mcp](https://glama.ai/mcp), [smithery.ai](https://smithery.ai)). The protocol reached stable version 1.0 after the iterations of 2025.

For those writing in English: think of MCP as the **standard driver between Claude Code and the rest of the world**. If you want Claude to do something it can't do natively — read your CRM, post to WordPress, query an internal database — the modern answer is: write an MCP server (or find one that already does the case for you) and register it.

### 11.2 Protocol architecture

MCP is a **client-server** protocol based on **JSON-RPC 2.0**. Three main components:

- **Host** — the user's AI application (for us: Claude Code). It doesn't talk directly to MCP servers: it uses one or more *clients*.
- **Client** — a 1:1 connection to a single server. Claude Code creates a client for each configured MCP server. The client manages the connection (process startup, message exchange, lifecycle) and isolates the server from the rest of the host.
- **Server** — the process that exposes functionality. It can be written in any language for which an MCP SDK exists (Python, TypeScript, Rust, Java, C#, Swift, Kotlin are all officially supported). It communicates with the client through a standard transport.

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

**Transports** — two main modes:

- **stdio** (standard input/output) — the client launches the server as a sub-process and communicates via stdin/stdout. It's the most common transport for local servers (filesystem, database, our own processes). Simple, secure by default (stays in the user system), no network to manage.
- **HTTP+SSE** (Server-Sent Events) — servers reachable via HTTP. Used for hosted servers (cloud) or shared between different clients. Requires auth handling and latency considerations that don't arise for stdio. The guide focuses on local stdio servers; we'll touch on remote servers in section 11.6.

**Capability negotiation** — at session startup, client and server exchange a handshake (`initialize`) in which they declare what they support: the server lists its tools, its resources, its prompts; the client lists its capabilities (e.g., support for sampling, logging). From that point on the conversation is an alternation of JSON-RPC requests.

The **three primitives** of an MCP server:

- **Tools** — functions the server exposes that Claude can invoke. Each has a name (`wp_create_post`), a textual description readable by the AI, and a JSON schema of arguments. When Claude decides to call it, it sends a `tools/call` request, the server executes, returns the result. It's the most used primitive.
- **Resources** — data addressable via URI (`wp://posts/123`, `file:///etc/hosts`). The server exposes them as a "library" Claude can read from. Resource ≠ Tools: reading a resource is a pure GET, with no side effects.
- **Prompts** — reusable prompt templates the server can provide to the user as "presets". Typically exposed as `/server-name:prompt-name` command in the host.

For our WordPress example we'll only use **tools** (post creation/update, category list). Tools are the most productive part of the protocol; resources and prompts are useful but less common in custom servers.

### 11.3 Configuring an existing MCP server

Configuration is declarative: you list the server in a JSON and Claude Code launches it automatically at session startup. Two scopes:

- **Project's `.claude/settings.json`** — the server is available only inside that project. Suited for project-specific integrations (a server to talk to the client's staging DB).
- **User's `~/.claude/settings.json`** — the server is available in every user session. Suited for global integrations (your MCP server for your own corporate CRM).

Example of configuring three servers simultaneously (one GitHub and two local):

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
        "/Users/maurizio/projects"
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

Key points:

- **`command` + `args`** — executable and arguments. `npx -y` is the standard pattern for servers distributed on npm (downloads them on the fly). For Python you typically use `uvx` or `python -m`.
- **`env`** — environment variables passed to the server. The `${VAR}` interpolations are resolved by the shell that launched Claude Code: the correct way to pass secrets is to put them in `.env`/`.envrc` and export them before launching Claude, not hardcode them in the committed JSON.
- **No secrets in repo** — a committed `mcpServers` entry containing a token in clear is a security incident waiting to happen. Always `${VAR}` with secrets loaded externally.

**Dedicated slash command and CLI.** Once a server is configured, Claude Code manages it with these commands:

```bash
# Internal slash command (in interactive session)
/mcp                       # list of active servers and their tools

# External CLI
claude mcp list            # same list from terminal
claude mcp add <name>      # adds a server (guided interview)
claude mcp remove <name>   # removes it
```

**Debug.** If a server doesn't start (startup error, missing dependency, unresolved env var), Claude Code prints the error at session startup and marks the server as "disconnected" in `/mcp`. To chase more subtle problems, launch the server manually from the terminal and exercise it via stdin with some `echo '{"jsonrpc":"2.0","method":"initialize",...}'` — the MCP documentation has precise examples.

### 11.4 Useful MCP servers: a curated selection

By May 2026 the MCP ecosystem is vast. A selection of servers worth getting familiar with:

- **`@modelcontextprotocol/server-github`** — complete management of repositories, issues, PRs, actions. It's the first MCP to install for those who develop on GitHub. Official, maintained by Anthropic.
- **`@modelcontextprotocol/server-filesystem`** — controlled access to specific filesystem directories. Useful for working on projects outside Claude Code's working directory (e.g., reading documentation in `~/Documents/specs`). The authorized paths are passed as arguments.
- **`mcp-server-postgres`** / **`mcp-server-sqlite`** — query, schema inspection, migration generation. Excellent for exploring staging databases without write permissions on prod.
- **`@modelcontextprotocol/server-puppeteer`** — headless browser automation: screenshots, scraping, click tests. Pairs very well with the `webapp-testing` skill (chapter 10).
- **`mcp-server-slack`** — sending messages and reading channels, useful for completion notifications of long tasks or automatic reports.
- **`mcp-server-sentry`** — access to error tracking data; can retrieve the stack trace of a recent exception and give it to Claude for the bug fix. Pairs with chapter 15.2 (Bug hunting with TDD).
- **`mcp-server-linear`** / **`mcp-server-notion`** — ticket system and knowledge base. Allow Claude to read the context of a task from Linear and produce the connected PR.

Community marketplaces have hundreds more: before writing an MCP from scratch, look for whether a suitable server already exists. The rule is: **existing MCP > custom MCP > skill > local script**, in order of preference for new solutions.

### 11.5 Creating an MCP server from scratch: publishing to WordPress

Use case: we want Claude Code to be able to **publish content to a WordPress site** without having to open the wp-admin dashboard. Typical scenario: you're discussing an article with Claude (writing it in Markdown, it suggests editorial cuts), and you want to close the session with *"publish this article as a draft in the 'Tutorial' category"*. Without MCP, Claude can at most tell you "here are the steps to do in admin". With MCP, it does it.

#### Prerequisites

1. A WordPress site with active REST API (default since WP 5.0+).
2. An **Application Password** generated from the WordPress user profile (user → edit profile → "Application Passwords"). It's a single-use password, long, separate from the main password: it's revoked without having to change the real password.
3. **Python 3.10+** and the official SDK: `pip install mcp httpx python-dotenv`.

#### Project structure

The complete code lives in the guide's repository, under `src/examples/wordpress-publisher-mcp/`:

```
src/examples/wordpress-publisher-mcp/
├── server.py        ← MCP server with the three tools
├── pyproject.toml   ← dependencies (mcp, httpx, python-dotenv)
├── .env.example     ← credentials template (copy to .env)
└── README.md        ← install and configuration instructions
```

`.env` (never commit — use `.env.example` as a base):

```
WP_BASE_URL=https://mysite.example.com
WP_USERNAME=maurizio
WP_APP_PASSWORD=xxxx xxxx xxxx xxxx xxxx xxxx
```

#### Server code (`server.py`)

The core of the server is the authentication setup and the FastMCP tool decorators. Here's the structure with the main tool:

```python
import os, base64, httpx
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

load_dotenv()
# Basic Auth with WP Application Password
auth_token = base64.b64encode(
    f"{os.environ['WP_USERNAME']}:{os.environ['WP_APP_PASSWORD']}".encode()
).decode("ascii")
HEADERS = {"Authorization": f"Basic {auth_token}", "Content-Type": "application/json"}
BASE_URL = os.environ["WP_BASE_URL"].rstrip("/")

mcp = FastMCP("wordpress-publisher")

@mcp.tool()
def wp_create_post(
    title: str,
    content: str,
    status: str = "draft",
    categories: list[int] | None = None,
) -> dict:
    """
    Creates a new article on WordPress.
    Args: title, content (HTML), status ("draft"/"publish"), categories (list of IDs)
    Returns: dict with id, status, link, modified of the created post.
    """
    payload = {"title": title, "content": content, "status": status}
    if categories:
        payload["categories"] = categories
    response = httpx.post(f"{BASE_URL}/wp-json/wp/v2/posts",
                          headers=HEADERS, json=payload, timeout=30.0)
    response.raise_for_status()
    data = response.json()
    return {"id": data["id"], "status": data["status"],
            "link": data["link"], "modified": data["modified"]}

if __name__ == "__main__":
    mcp.run()
```

The other two tools follow the same pattern:

- **`wp_publish_post(post_id)`** — changes a draft's status to `"publish"` via `POST /wp-json/wp/v2/posts/{id}`.
- **`wp_list_categories()`** — retrieves all site categories via `GET /wp-json/wp/v2/categories`.

::: note
Full code, `.env.example`, `pyproject.toml` and `README` in [src/examples/wordpress-publisher-mcp/](https://github.com/miziomon/claude-code-guide/tree/main/src/examples/wordpress-publisher-mcp) in the guide's repository.
:::

#### Registration in Claude Code

Add to your `.claude/settings.json` (or the global one):

```json
{
  "mcpServers": {
    "wordpress-publisher": {
      "command": "python",
      "args": ["/absolute/path/to/src/examples/wordpress-publisher-mcp/server.py"]
    }
  }
}
```

#### Interactive test

Launch Claude Code, run `/mcp` to verify that the `wordpress-publisher` server is connected and showing three tools. Then a typical conversation:

> **You**: I just finished writing an article on Plan Mode, you'll find it in `article-plan-mode.md`. Publish it as a draft in the "Tutorial" category.
>
> **Claude**: I'll first read the file to extract title and content.
> *[Read article-plan-mode.md]*
> I read the article: 1840 words, title *"Plan Mode: thinking before writing"*. I'll fetch the category IDs to find "Tutorial".
> *[wp_list_categories]*
> "Tutorial" category has ID **7**. Proceeding with draft creation.
> *[wp_create_post(title=..., content=..., status="draft", categories=[7])]*
> ✓ Draft created. ID **142**, link [https://mysite.example.com/?p=142&preview=true](https://...). Do you want me to publish it now or keep it as a draft for review?
>
> **You**: Keep it as a draft, I need to review the images.

#### What happens under the hood

Claude Code:

1. Read `article-plan-mode.md` with its native Read tool.
2. Understood that the category ID was needed — called `wp_list_categories` (an MCP tool).
3. Searched for "Tutorial" among the returned categories and extracted ID 7.
4. Called `wp_create_post` with title, content, and categories.
5. Reported the outcome with the preview link.

All via JSON-RPC between the client (Claude Code) and our Python server running as a local sub-process. No network hops on sensitive data — only HTTPS requests to the WordPress server, exactly as if the user had made them from a REST client.

#### Natural extensions

From this skeleton it's easy to grow:

- add `wp_upload_media` to upload images to the library;
- add `wp_list_drafts` to retrieve existing drafts;
- add `wp_schedule_post` for scheduled publications (`status: "future"` with `date`);
- expose categories and posts as **resources** (URI `wp://categories`, `wp://posts/{id}`) to give Claude visibility of the catalog without having to invoke a tool every time.

For those coming from the WordPress plugin world: this MCP server is essentially an **AI-side REST client**. Everything your plugin can do via REST API, your MCP can expose as a tool.

### 11.6 Security and operational considerations

Three points of attention that separate an MCP server from an experiment and an MCP server ready for the trade.

**No automatic sandbox.** An MCP server runs as *you*: it has your file system credentials, network access, and tokens you pass it via env. Nothing isolates it from the rest of the system. Practical consequences:

- **Audit the code** before installing third-party MCP servers, especially if obtained from less-supervised marketplaces. A malicious server can read your `~/.ssh` or exfiltrate secrets from env.
- **Keep your custom MCP servers in repos you control**, not as anonymous npx dependencies.
- **Use Application Password / API key with minimum scope**, never the main personal password. You revoke them with one click if needed.

**Permission deny for sensitive tools.** MCP tools flow into Claude Code's permission system (chapter 9). For servers with risky tools (delete posts, run DELETE queries) it's worth denylisting destructive tools in `permissions.deny`:

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

The `mcp__<server>__<tool>` pattern allows precision targeting of the tool you don't want auto-approved; Claude will continue to ask for explicit confirmation at every invocation.

**Logging and audit.** To understand what your MCP is really doing in production, pair a **PostToolUse hook** (chapter 13) that logs every MCP tool invocation in JSON Lines. Concrete patterns in chapter 13.6 (example B). Effect: total traceability of who (user, model), what (which MCP tool), when, and with what arguments.

**Remote MCPs.** Servers reached via HTTP+SSE (hosted servers, shared between teams) add a dimension: latency and network auth. For stable team-level integrations a hosted server is preferable; for experimentation and personal integrations, local stdio is simpler and more secure by default. The protocol is the same, only the transport changes.

**When you DON'T need an MCP.** If the task is purely local (reading a file, executing a script), Claude Code already has Read/Write/Bash as native tools: writing an MCP to do what Bash already does is overkill. The rule is: **MCP for external services or network protocols; native tools for the local user system**. When in doubt, first skill (chapter 10) or custom slash command; MCP only when it's an external system Claude needs to dialogue with via API.

### 11.7 Managing the cost of MCP servers on context

Every active MCP server contributes to the session context with its tool definitions: name, description, JSON schema of arguments. The weight ranges from a few hundred tokens for simple servers to thousands for servers with many tools or elaborate descriptions. With ten active servers, the "MCP tare" can easily exceed 10,000 tokens per session and compromise the cache prefix (see [§8.10](#prompt-cache-and-consumption-observability)).

#### Audit with `/context`

The `/context` command shows the "MCP tools" entry in the category breakdown. Audit procedure:

1. Run `/mcp` to see the list of active servers and the tools they expose.
2. Run `/context` and read the weight of the MCP entry.
3. Identify servers not used in this project.
4. Disable them at the project level in `.claude/settings.json`:

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": { "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}" }
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/Users/maurizio/projects"]
    }
  },
  "disabledMcpjsonServers": ["slack", "linear", "notion"]
}
```

The `disabledMcpjsonServers` key disables the listed servers without removing them from the configuration — re-enable them by removing the entry. This configuration in the project's `.claude/settings.json` takes precedence over the global `~/.claude/settings.json`, so you can have different server sets per project.

**Practical rule**: a server you don't use in this project shouldn't be active in this project. Three well-chosen servers weigh less and cache better than ten "just in case".

---


---

> ← [10. Skills](10-skills.md) | [Index](README.md) | [12. Subagents](12-subagents.md) →
