# Practical Guide to Claude Code CLI

> **Version 4.23 — May 2026** — verified on Claude Code v2.1.123
> Licensed under [Creative Commons BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

> ← [13. Hooks](13-hooks.md) | [Index](README.md) | [15. Advanced workflows](15-advanced-workflows.md) →

---

## 14. Plugins: distributable packages

Plugins are the mechanism Claude Code uses to **distribute and install extensions**: skills, MCP servers, custom subagents, slash commands — all grouped into a single package installable with a command. If a skill teaches Claude *what to do* (chapter 10) and MCP tells it *what to talk to* (chapter 11), the plugin is the **container** that puts them together and distributes them. For those coming from the development world: think of the plugin as the npm/Composer package of the Claude Code ecosystem.

### 14.1 Claude Code's extension mechanisms: a map

By this point in the book you've seen **all four** of Claude Code's extension mechanisms that the plugin packages: **Skills** ([chapter 10](#skills-the-extension-mechanism)), **MCP** ([chapter 11](#mcp-integrating-external-services)), **Subagents** ([chapter 12](#subagents-orchestrating-specialized-work)), and **Hooks** ([chapter 13](#hooks-automating-claude-codes-lifecycle)). Before entering plugins, it's useful to reposition them in a unified map, to understand where each one operates and what relationship they have with the container we're about to examine.

| Mechanism | What it does / where it acts | Where it lives | How it's distributed |
|------------|------------------------|-----------|----------------------|
| **Skill** ([chapter 10](#skills-the-extension-mechanism)) | Extends what Claude *knows how to do* | Markdown + local scripts | Folder in user system, plugin |
| **MCP** ([chapter 11](#mcp-integrating-external-services)) | Exposes tools/data of external systems | Server (local stdio or remote HTTP+SSE) | Open protocol, any language |
| **Subagent** ([chapter 12](#subagents-orchestrating-specialized-work)) | Executes specialized work in isolation | YAML in `.claude/agents` | Config file, plugin |
| **Hook** ([chapter 13](#hooks-automating-claude-codes-lifecycle)) | Intercepts lifecycle events | `settings.json` `hooks` | Local config, plugin |
| **Plugin** (this chapter) | Package that groups the other four | Folder with manifest + payload | Marketplace, Git repo |

In a vertical view: **Plugin** is the container, the other four are the **contents** that can be bundled inside a plugin. A "GitHub PR Assistant" plugin can contain: a review skill, an MCP server that talks to the GitHub API, a specialized subagent for writing PR descriptions, and a `/review` slash command that orchestrates everything. All distributed as a single package.

### 14.2 What a plugin is and why it exists

A plugin is born to solve a practical problem: when a person or organization maintains a set of skills, MCP servers, and custom workflows, distributing them individually is inconvenient. The consumer has to find the skill repo, copy the files to `.claude/skills/`, configure the MCP server in `settings.json`, register the slash commands — separate steps that don't scale if the author updates the components frequently.

The plugin standardizes all this:

- **A single installation** collects all components
- **Centralized versioning** — the author releases a new version, you do `claude plugin update`
- **Clean uninstall** — removes everything in one shot
- **Shared marketplace** — authors publish the plugin on a public or private marketplace

Plugins are particularly precious for **organizations** that want to distribute to teams a coherent set of extensions (corporate skills + MCP for internal APIs + specialized subagents), and for **community authors** who produce thematic packages (Vercel Labs, WordPress Agent Skills, JuliusBrussee/caveman are all distributed as plugins).

### 14.3 Anatomy of a plugin

A plugin is a folder with a standardized structure. Minimal example:

```
my-plugin/
├── plugin.yml             # plugin manifest
├── skills/                # included skills (optional)
│   └── my-skill/
│       └── SKILL.md
├── mcp/                   # included MCP servers (optional)
│   └── my-server/
│       ├── server.py
│       └── pyproject.toml
├── agents/                # custom subagents (optional)
│   └── my-agent.yaml
├── commands/              # custom slash commands (optional)
│   └── my-command.md
└── README.md              # documentation
```

The **`plugin.yml`** file is the manifest that declares metadata, dependencies, and what the plugin contains:

```yaml
name: my-plugin
version: 1.0.0
description: "Example plugin"
author: "Maurizio Pelizzone <maurizio@mavida.com>"
license: MIT
homepage: "https://github.com/mavida/my-plugin"

# Included components
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

The manifest declares everything the plugin installs. When the user does `claude plugin install`, Claude Code reads the manifest, copies/registers the components in the right slots (`~/.claude/skills/`, `mcpServers` in `settings.json`, etc.), and activates the plugin.

### 14.4 Plugin marketplace

A **marketplace** is a published index of available plugins, typically a Git repository with an expected structure. Claude Code supports:

- **Anthropic official marketplaces** (`anthropics/skills` and similar)
- **Community marketplaces** (Vercel Labs, Trail of Bits, JuliusBrussee)
- **Private organizational marketplaces** (an internal Git repo with corporate plugins)

Basic commands:

```bash
# Add a marketplace to your instance
/plugin marketplace add anthropics/skills

# Explore available plugins (opens interactive picker)
/plugin

# Install a specific plugin
/plugin install <plugin-name>

# Update installed plugins
claude plugin update

# Uninstall a plugin
claude plugin uninstall <plugin-name>
```

The `/plugin` picker shows plugin metadata (name, version, description, author) and a preview of included components, so you know what you're installing before download. Once installed, the plugin goes to `~/.claude/plugins/<name>/` and its components automatically become available in all sessions.

### 14.5 Creating a custom plugin

Let's see the minimal structure of a demo plugin. The scenario: a "hello-world" plugin containing a single `/hello` slash command and a welcome skill.

**Step 1 — Create the folder and manifest** in `~/my-plugins/hello-world/`:

```yaml
# plugin.yml
name: hello-world
version: 0.1.0
description: "Example plugin"
author: "Maurizio Pelizzone"
license: MIT

includes:
  skills:
    - skills/hello-skill
  commands:
    - commands/hello.md
```

**Step 2 — Add the skill** in `skills/hello-skill/SKILL.md`:

```markdown
---
name: hello-skill
description: "Use this skill when the user asks for greetings or examples of plugin usage."
---

# Hello Skill

When the user asks for plugin examples or greetings, respond with:
- A brief greeting
- A note that this response comes from a skill installed via plugin
```

**Step 3 — Add the slash command** in `commands/hello.md`:

```markdown
---
description: "Quick greeting from the hello-world plugin"
---

Greet the user in a friendly way and remind that this command comes
from the hello-world plugin (version 0.1.0).
```

**Step 4 — Install locally for testing** (without publishing):

```bash
# Install the plugin in development mode (link, not copy)
claude plugin install ~/my-plugins/hello-world --dev
```

Open Claude Code: type `/hello` and you should see the greeting. Ask Claude something that activates the skill — the `description` mentions "greetings" — and you should see the response that explicitly cites the plugin origin.

### 14.6 Distributing a plugin

Once the plugin works locally, distributing it requires three steps:

1. **Publish the Git repo** with the plugin structure in the root. The `plugin.yml` must be at the root of the folder.
2. **Create a marketplace** (even minimal: a second Git repo with a `marketplace.yml` file listing your plugins):

```yaml
# marketplace.yml
name: mavida
description: "Mavida plugins for Claude Code"

plugins:
  - name: hello-world
    repo: https://github.com/mavida/hello-world
    versions: [0.1.0]
```

3. **Document the installation** in the README:

```bash
/plugin marketplace add mavida/marketplace
/plugin install hello-world
```

To manage versions, use semantic Git tags (`0.1.0`, `0.2.0`, `1.0.0`). Claude Code respects the version requested in the consumer's manifest.

### 14.7 Security and operational considerations

A plugin can contain **executable code** (MCP servers in Python/Node, hooks in Bash, auxiliary scripts in skills). Installing a third-party plugin is equivalent to installing an npm or Composer package: you trust the author with the permissions the plugin will require.

Three practical rules:

- **Audit before installing**. Read the manifest, inspect the included skills, check what the MCP servers launch. A checklist: `plugin.yml` what does it declare to install? Do the skills require access to sensitive tools? Do the MCP servers contact external services to which you wouldn't want to give your credentials?
- **Verify the repo's health** of the author: last commit date, open/closed issues, presence of security policy. A plugin abandoned two years ago is a constant risk.
- **Use private marketplaces** for corporate use. For plugins with corporate secrets (API keys, internal URLs) keep the marketplace on a corporate Git repo, not public.

For plugins from known organizations (Anthropic, Vercel Labs, WordPress) the risk is low: they publish under their names, the code is scrutinized by the community, updates are regular. For individual plugins, apply the same caution you would use for a third-party library.

An additional protection: MCP tools exposed by plugins flow into Claude Code's permission system (chapter 9), so you can precisely denylist destructive operations with `permissions.deny` on `mcp__<server>__<tool>` patterns (see 12.6 for examples).

---


---

> ← [13. Hooks](13-hooks.md) | [Index](README.md) | [15. Advanced workflows](15-advanced-workflows.md) →
