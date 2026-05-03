# Practical Guide to Claude Code CLI

> **Version 4.23 — May 2026** — verified on Claude Code v2.1.123
> Licensed under [Creative Commons BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

> ← [8. Context management](08-context.md) | [Index](README.md) | [10. Skills](10-skills.md) →

---

## 9. Security and permission management

Claude Code is an **autonomous** agent that runs commands on your system. Without the right precautions, it's a real risk vector.

### 9.1 The permissions system

By default, Claude asks for confirmation before performing any modification operation (file write, shell commands, MCP calls that modify state). Read operations are auto-approved:

- `Read`, `Glob`, `Grep`, `WebSearch`, `LSP` → no confirmation
- `Edit`, `Write`, `Bash`, write MCP → confirmation required

### 9.2 Configuring permissions in `settings.json`

You can define granular rules in the project's `.claude/settings.json` file:

```json
{
  "permissions": {
    "allow": [
      "Bash(npm run test:*)",
      "Bash(npm run lint:*)",
      "Bash(git status)",
      "Bash(git diff)",
      "Read(**)"
    ],
    "deny": [
      "Read(.env*)",
      "Read(**/secrets/**)",
      "Read(**/.aws/credentials)",
      "Bash(rm -rf *)",
      "Bash(sudo *)",
      "Bash(curl * | bash)",
      "Bash(wget * | sh)"
    ]
  }
}
```

**Step-by-step explanation:**

1. `allow` — operations Claude can execute **without asking for confirmation**
2. `deny` — operations **physically blocked**, even if Claude tries nothing happens
3. Patterns use glob (`**` for any path, `*` for single segment)
4. `deny` has **precedence** over `allow`

#### Validating the file with the official JSON schema

Anthropic publishes a JSON schema for `settings.json` hosted on SchemaStore. By adding the `$schema` line as the first key, JSON Schema-aware editors (VS Code, Cursor, JetBrains, Vim with coc-json, etc.) give you autocomplete of allowed properties, inline value validation, and tooltips with the description of each field:

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "permissions": {
    "allow": ["Bash(npm run test:*)"],
    "deny":  ["Read(.env*)"]
  }
}
```

The official docs ([code.claude.com/docs/en/settings](https://code.claude.com/docs/en/settings)) warn that the schema is updated periodically: a validation warning on a property recently introduced in a recent release doesn't necessarily mean the configuration is invalid. The same schema also covers other sections of `settings.json`, including `hooks` (see [section 13 — Hooks](#hooks-automating-claude-codes-lifecycle)), `env`, `model`, `availableModels`.

### 9.3 Protecting secrets

Despite `.claudeignore`, there are scenarios in which Claude could read sensitive files (prompt injection, configuration errors). **Always** use `permissions.deny` for `.env` files, credentials, private keys.

### 9.4 Dangerous modes

**`--dangerously-skip-permissions`** skips all confirmations. It's useful for:
- Autonomous execution in sandbox/Docker environments
- Long tasks where you don't want to be interrupted every 30 seconds

The name is explicit: **it's not a flag to use lightly**. Guidelines:

- **Never** on machines containing production credentials
- **Never** with access to sensitive corporate repositories
- **Only** in isolated containers or VMs dedicated to the purpose

For lifecycle-level block automation (e.g., preventing `rm -rf` on protected paths even within `--dangerously-skip-permissions`), Hooks offer an additional programmatic layer: see [section 13](#hooks-automating-claude-codes-lifecycle).

### 9.5 Prompt injection

An attacker could insert malicious instructions in:

- Code comments that Claude reads
- README files downloaded from dependencies
- Responses from untrusted MCP services
- Manipulated file names

**Practical defenses:**

1. Always use Plan Mode for tasks on third-party code
2. Always review the plan before approving it
3. Don't run Claude Code with administrator privileges
4. Isolate external projects in separate directories with restrictive `settings.json`

---


---

> ← [8. Context management](08-context.md) | [Index](README.md) | [10. Skills](10-skills.md) →
