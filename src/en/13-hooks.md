# Practical Guide to Claude Code CLI

> **Version 4.23 — May 2026** — verified on Claude Code v2.1.123
> Licensed under [Creative Commons BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

> ← [12. Subagents](12-subagents.md) | [Index](README.md) | [14. Plugins](14-plugins.md) →

---

## 13. Hooks: automating Claude Code's lifecycle

**Hooks** are Claude Code's third extension mechanism, and the one that operates at the lowest level. While Subagents and Skills influence *what* the main agent does, Hooks intercept *when* certain events happen — the start of a session, the moment before a tool execution, the end of a response — and can validate, modify, block, register those events before or after they happen.

They're the right tool when the extension isn't "let it know how it works" (Skill) or "delegate this task" (Subagent), but "intervene automatically at this precise point of the flow, without me having to remember to ask".

### 13.1 What they are and what they're for

A Hook is a script — bash, HTTP, prompt to another model, subagent, or MCP tool — configured to fire at a determined event of Claude Code's lifecycle. The script receives via input a JSON payload describing the event (e.g., which tool is about to be executed, with what arguments) and produces an output that can:

- **block** the action (e.g., prevent `rm -rf` on a protected folder)
- **validate** and let it pass (e.g., check that every edit of a `.php` file respects style rules)
- **register** in a structured log (audit trail of all modifications)
- **inject** automatic context (e.g., remind Claude of the project conventions at every session start)

At first glance they look like a linter or a git hook, but with an important difference: the linter acts *after* the code has been written by you, Hooks act *during* Claude Code's execution, before its actions become effective. It's an internal automation level, not an external check.

> A good rule: if what you want to do is "every time Claude does X, you must do Y", it's probably a Hook. If it's "Claude must know that the project uses X", it's a Skill or a `CLAUDE.md`. If it's "delegate this specific work to another agent", it's a Subagent.

### 13.2 Anatomy of a hook

Hooks are configured in the `settings.json` file along with permissions and other directives (see [section 9.2](#configuring-permissions-in-settings.json) for the basic setup and for the `$schema` line that enables autocomplete and validation also of `hooks` blocks). The basic syntax is the same for all events:

```json
{
  "hooks": {
    "<EventName>": [
      {
        "matcher": "<pattern>",
        "hooks": [
          {
            "type": "command",
            "command": "<script-path>"
          }
        ]
      }
    ]
  }
}
```

Configuration files live at three levels (plus two reduced-scope locations):

- **`~/.claude/settings.json`** — user, valid on all machines. Personal, not shareable.
- **Project's `.claude/settings.json`** — committed in Git, shared with the team.
- **Project's `.claude/settings.local.json`** — gitignored by default. For Hooks specific to your local copy.
- **Skill or Agent frontmatter** (`hooks` field) — Hooks that run only when that Skill/Agent is active.
- **Installed plugins' `hooks/hooks.json`** — Hooks that come with a plugin.

There are **five types of Hooks**, chosen via the `type` field:

| **Type** | **When to use it** | **Example scenario** |
|---|---|---|
| `command` (default) | Deterministic logic, file access, JSON parsing | Block a command, write a log, launch a script |
| `http` | Centralized audit, cloud integration (introduced Feb 2026) | POST to a corporate endpoint for immutable logs |
| `prompt` | "Yes/no" decision requiring LLM judgment | "Are all prompt tasks completed before terminating?" |
| `agent` | Complex verification requiring tools and codebase search | A subagent that runs the test suite before Stop |
| `mcp_tool` | Integration with an already configured MCP server | Save context in an external MCP memory |

For 90% of practical cases you use `command`. Other types are for advanced scenarios or when the decision requires capabilities a simple script doesn't have.

### 13.3 Lifecycle events

Claude Code exposes more than twenty interceptable events, groupable into seven categories. Synthetic table of the events most used in practice:

| **Category** | **Event** | **When it fires** | **Can it block?** |
|---|---|---|---|
| Session | `SessionStart` | Session start or resume | No — can inject context |
| Session | `SessionEnd` | Session end | No — only cleanup |
| Session | `UserPromptSubmit` | User submits a prompt | Yes — can modify/block the prompt |
| Session | `Stop` | Claude finishes a response | Yes — can force to continue |
| Tool | `PreToolUse` | Before a tool's execution | Yes — can deny/modify the input |
| Tool | `PostToolUse` | After a tool's execution | No — the action is already done |
| Tool | `PostToolUseFailure` | After a failed tool | No |
| Permissions | `PermissionRequest` | Shows permissions dialog | Yes — can decide allow/deny/ask |
| Subagent | `SubagentStart` | Subagent spawn | No |
| Subagent | `SubagentStop` | Subagent terminates | Yes — can force a retry |
| Compaction | `PreCompact` | Before `/compact` | No — can save backup |
| Compaction | `PostCompact` | After `/compact` | No — can re-inject context |
| File | `FileChanged` | Watched file modified | No |

There are other more specialized events (`UserPromptExpansion`, `ConfigChange`, `CwdChanged`, `WorktreeCreate/Remove`, `Notification`, `Elicitation`, and the Agent Teams events like `TaskCreated`, `TaskCompleted`, `TeammateIdle`). For the complete list the canonical source is [code.claude.com/docs/en/hooks](https://code.claude.com/docs/en/hooks).

The two events you'll use most often are `PreToolUse` and `PostToolUse`. The whole "tool guardian" pattern is built on them.

### 13.4 Matchers and inspection (`/hooks`)

The `matcher` field filters **which invocations** of the event must activate the Hook. Four supported patterns:

- **Wildcard** `"*"` or empty string — matches all
- **Exact** `"Bash"` — only invocations of the `Bash` tool
- **Pipe** `"Edit|Write"` — alternation, matches `Edit` or `Write`
- **Regex** `"mcp__.*"` — standard regex syntax, here to match all MCP tools

The matcher's meaning depends on the event: for `PreToolUse`/`PostToolUse` it's the tool name; for `SessionStart` it's the source (`startup`, `resume`, `clear`, `compact`); for `SubagentStart`/`SubagentStop` it's the agent name. Without matcher (or with `"*"`), the Hook always fires.

From v2.1.85+ there's also the `if` field for secondary filters on the tool's **arguments**, not just on the name:

```json
{
  "matcher": "Bash",
  "hooks": [
    {
      "type": "command",
      "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/validate-git.sh",
      "if": "Bash(git *)"
    }
  ]
}
```

This Hook fires only for `git ...` and ignores other Bash commands — useful to restrict further.

**`/hooks` command.** Once a Hook is written it's easy to wonder if the configuration was actually loaded. `/hooks` opens an interactive (read-only) browser of the active configuration: for each event it shows how many Hooks are registered, from which settings file they come, with which matcher. It doesn't allow **editing** or **disabling** Hooks on the fly: for that you need to modify `settings.json` and wait for it to be reloaded (or restart the session). The typical development flow is: edit `settings.json` → `/hooks` for loading verification → invoke a target tool to test the behavior.

### 13.5 Input and output

A `command` type Hook receives via **stdin** a JSON object describing the event. Fields common to all events:

```json
{
  "session_id": "abc123",
  "cwd": "/home/user/wp-plugins/access-control",
  "hook_event_name": "PreToolUse",
  "transcript_path": "/home/user/.claude/projects/.../transcript.jsonl"
}
```

For `PreToolUse` `tool_name` and `tool_input` are added:

```json
{
  "session_id": "abc123",
  "hook_event_name": "PreToolUse",
  "tool_name": "Bash",
  "tool_input": { "command": "rm -rf wp-content/uploads" }
}
```

The **output behavior** is governed by:

- **Script exit code**:
  - `0` — success. If stdout is valid JSON, it's interpreted as structured output; if it's plain text, it's added to the context as `additionalContext`.
  - `2` — **block**: the action doesn't proceed. stderr is shown to Claude as the reason for the block.
  - Other values — non-blocking error, the action proceeds but is registered in the transcript.

- **Structured JSON output** (on stdout, exit 0):

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "rm -rf on wp-content is forbidden",
    "updatedInput": { "command": "echo 'command blocked'" },
    "additionalContext": "To delete uploads use the backup script."
  }
}
```

Most-used fields:

- **`permissionDecision`** (PreToolUse): `allow` / `deny` / `ask` / `defer`
- **`decision`** (PostToolUse, Stop): `allow` / `block`
- **`additionalContext`**: text injected to Claude as a system reminder
- **`updatedInput`**: modify the tool input before execution (e.g., force safe flags)
- **`continue`** / **`stopReason`**: control of the flow in `Stop` events

**Multiple Hooks on the same event? "Most restrictive wins".** If two Hooks on `PreToolUse` return one `allow` and the other `deny`, `deny` wins. All `additionalContext`s are concatenated. If two Hooks set `updatedInput`, the order isn't guaranteed: avoid configurations where two different Hooks modify the same input.

### 13.6 Practical examples

Four examples in the WordPress space, from the simplest to the most articulated. For each: scenario, configuration, script, observed behavior.

#### Example A — Block `rm -rf` in `wp-content/`

**Scenario.** You're working on a plugin and want a safety net that prevents Claude from launching `rm -rf` on any path containing `wp-content/`. An oversight in a shell command could destroy uploads, cache, or backups of a production site.

**`.claude/settings.json`:**

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/block-rm-wpcontent.sh"
          }
        ]
      }
    ]
  }
}
```

**`.claude/hooks/block-rm-wpcontent.sh`:**

```bash
#!/bin/bash
INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // ""')

if echo "$COMMAND" | grep -qE 'rm\s+(-[a-z]*r[a-z]*\s+|-r\s+).*wp-content'; then
  echo "Blocked: recursive rm on wp-content forbidden by hook" >&2
  exit 2
fi
exit 0
```

**Behavior.** When Claude tries to launch `rm -rf wp-content/uploads`, the Hook intercepts, detects the pattern, and returns exit 2 with a message in stderr. Claude sees the block, receives the reason, and decides how to proceed (asking you for confirmation or changing approach). `rm` commands on other paths pass normally.

#### Example B — JSON Lines audit log on Edit/Write

**Scenario.** You want an audit trail of all modifications made by Claude to the plugin's PHP files, in JSON Lines format for subsequent analysis (grep, jq, dashboard).

**`.claude/settings.json`:**

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/audit-php.sh"
          }
        ]
      }
    ]
  }
}
```

**`.claude/hooks/audit-php.sh`:**

```bash
#!/bin/bash
INPUT=$(cat)
FILE=$(echo "$INPUT" | jq -r '.tool_input.file_path // ""')

if [[ "$FILE" == *.php ]]; then
  jq -nc --arg ts "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
         --arg session "$(echo "$INPUT" | jq -r '.session_id')" \
         --arg tool   "$(echo "$INPUT" | jq -r '.tool_name')" \
         --arg file   "$FILE" \
    '{ts: $ts, session: $session, tool: $tool, file: $file}' \
    >> "$CLAUDE_PROJECT_DIR/.claude/audit/php-edits.jsonl"
fi
exit 0
```

**Behavior.** Every edit or write on a `.php` file adds a line to the file `audit/php-edits.jsonl`. Other modifications (CSS, MD, JSON) are ignored. The log is structured and readable with `jq -s '.[] | select(.file | contains("admin"))' audit/php-edits.jsonl` to filter retrospectively.

#### Example C — `phpcs` with WordPress-Extra automatic, async

**Scenario.** Every PHP file modified by Claude must be passed to `phpcs` with the `WordPress-Extra` standard. You want the lint to run **in background** without blocking Claude (async is available since January 2026).

**`.claude/settings.json`:**

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/phpcs-wp.sh",
            "async": true
          }
        ]
      }
    ]
  }
}
```

**`.claude/hooks/phpcs-wp.sh`:**

```bash
#!/bin/bash
INPUT=$(cat)
FILE=$(echo "$INPUT" | jq -r '.tool_input.file_path // ""')

if [[ "$FILE" == *.php ]] && command -v phpcs >/dev/null; then
  phpcs --standard=WordPress-Extra "$FILE" \
        > "$CLAUDE_PROJECT_DIR/.claude/lint/$(basename "$FILE").log" 2>&1 || true
fi
exit 0
```

**Behavior.** `phpcs` runs in background after each edit, writing the report to `.claude/lint/`. Claude doesn't wait for completion (it's async, decision fields would be ignored anyway). You review the logs at the end of the session or with a watcher in the IDE. For hard commit blocking, use a separate Git pre-commit hook — Claude Code Hooks don't replace Git hooks, they work at a different level.

#### Example D — Conventions reminder at `SessionStart`

**Scenario.** Every time you open Claude Code inside the plugin, you want the main agent to receive a reminder of the project conventions (in addition to what's already written in `CLAUDE.md`).

**`.claude/settings.json`:**

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/wp-session-reminder.sh"
          }
        ]
      }
    ]
  }
}
```

**`.claude/hooks/wp-session-reminder.sh`:**

```bash
#!/bin/bash
cat <<'REMINDER'
Reminder for this session:
- All PHP hooks must verify nonce and capability.
- Output always escaped (esc_html, esc_attr, wp_kses_post).
- SQL queries only via $wpdb->prepare().
- Code style: PSR-12 + WordPress-Extra where the two diverge, WordPress wins.
REMINDER
exit 0
```

**Behavior.** At session startup (matcher `startup`, not on `resume`), the main agent receives the reminder as `additionalContext`. It's complementary to `CLAUDE.md`: the Markdown file covers stable rules, the Hook can inject dynamic reminders (e.g., building the message by reading the plugin state, the current branch, or recent events).

### 13.7 Security

Hooks are powerful because they execute **arbitrary code** with your user permissions. There's no sandbox: a Hook script can read `.env`, make network requests, leave traces on the filesystem. This power is the same that makes them an attack vector if not handled with attention.

**CVE-2025-59536 (RCE via hook injection).** In early 2026 a case of Remote Code Execution was documented exploiting the fact that `.claude/settings.json` is automatically loaded from the project root. A malicious repository can register a Hook that executes arbitrary script at the first launch of Claude Code in that directory. You find it tracked as [CVE-2025-59536 on Check Point Research](https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/).

**Five practical security rules.**

1. **Mandatory code review on `.claude/settings.json`.** Treat it as an executable script, not as a passive configuration file. Changes to that file require review exactly like a modification to the project's `Makefile`.
2. **Untrusted repositories: clone, inspect, then open Claude Code.** Don't launch `claude` inside a freshly cloned repo without having opened `.claude/settings.json` and `.claude/hooks/` to check what they contain.
3. **HTTP hooks: explicit env var whitelist.** The `allowedEnvVars` field defines which environment variables can be interpolated in headers. Don't whitelist secrets that aren't needed for the specific endpoint.
4. **Sanitize input before injecting it as `additionalContext`.** A Hook payload contains `tool_input` coming from the session. If you pass that raw text to Claude as context, you open the door to prompt injection (a malicious `tool_input` injected in turn by a file read by Claude).
5. **Global disabling for debug.** The `"disableAllHooks": true` flag in `settings.json` turns off all Hooks. Useful in debug phase when you suspect a Hook is interfering, or if you have doubts about the origin of a loaded configuration.

> Hooks configured at **user** level (`~/.claude/settings.json`) are under your control and follow you everywhere. Hooks configured at **project** level (`.claude/settings.json`) are under the control of anyone who can commit to the repo. Keep this distinction in mind when you receive a pull request that touches that file.

### 13.8 Gotchas and when NOT to use them

Hooks have a number of common traps. The six most frequent:

- **Relative paths in scripts.** The Hook runs with a non-guaranteed cwd. Always use `$CLAUDE_PROJECT_DIR` or absolute paths, never relative paths like `./scripts/check.sh`.
- **JSON parsing with regex.** The payload is JSON: use `jq` or a real parser. Trying to extract fields with `grep`/`sed` produces fragile scripts that break at the first special character.
- **Stop hook in loop.** If a Hook on `Stop` returns `continue: true`, Claude continues and at the end triggers `Stop` again, which triggers the Hook again... infinite loop. The payload contains `stop_hook_active: true` when you're in re-execution: read that flag and exit immediately if it's `true`.
- **`async: true` doesn't block.** Asynchronous Hooks are useful only for side-effects (logging, lint, notifications). If they return `decision: "block"` or `permissionDecision: "deny"`, those fields are **ignored**. To block you must be synchronous.
- **`PostToolUse` cannot undo.** The event is called "Post" because the tool has already been executed. You can log, format, send notifications, but you can't undo the action. To block you need `PreToolUse`.
- **Shell profile output that pollutes stdout.** If your `~/.bashrc` or `~/.zshrc` prints something even in non-interactive mode, that text ends up in front of the Hook's JSON output and breaks the parser. Wrap profile `echo`s in `if [[ $- == *i* ]]; then ... fi`.

**When NOT to use a Hook.**

- **Complex logic requiring LLM reasoning**. A `command` Hook is a deterministic script. If the decision requires judgment ("is this edit a good idea?"), you need a dedicated subagent (see [section 12](#subagents-orchestrating-specialized-work)) or a `prompt` type Hook.
- **Style and formatting post-edit**. To apply a style guide to all modified files, a normal linter (Prettier, phpcs, eslint) launched from pre-commit or IDE is almost always more transparent and debuggable than a PostToolUse Hook.
- **One-off exploratory workflows**. The overhead of writing a script + configuring it + testing the matcher + verifying with `/hooks` isn't justified if you'll use the workflow only once.

When in doubt: **Hook for automatic and repeated behaviors you want to be invisible and infallible**. For everything else, more suitable tools exist.

---


---

> ← [12. Subagents](12-subagents.md) | [Index](README.md) | [14. Plugins](14-plugins.md) →
