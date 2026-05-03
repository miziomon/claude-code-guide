# Practical Guide to Claude Code CLI

> **Version 4.23 — May 2026** — verified on Claude Code v2.1.123
> Licensed under [Creative Commons BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

> ← [11. MCP](11-mcp.md) | [Index](README.md) | [13. Hooks](13-hooks.md) →

---

## 12. Subagents: orchestrating specialized work

**Subagents** are one of Claude Code's most powerful mechanisms, and also one of the least understood. They aren't "secondary agents" doing minor things: they are instances of Claude with **their own context, their own tools, their own prompt personality**, that the main session can invoke to delegate specialized work. An entire chapter is needed to frame them well because they change the way you set up complex workflows.

### 12.1 What they are and why you need them

The most useful analogy is **browser tabs**. When you work on a complex task, the main agent is like a main tab that fills with child tabs (read files, tool output, searches): the further it goes, the heavier the tab gets. Subagents are **separate tabs**: they have their own context, do their work, and when finished pass to the main tab only the result — not everything they read to get there.

In practice they solve three distinct problems:

1. **Saturated context**. A search that requires reading 50 files to find a pattern, done by the main agent, leaves 50 files in the context. Done by a subagent, it leaves only the final summary. See also [section 8](#context-management) on context management.
2. **Specialization**. A generalist main agent can do a code review, but a subagent with a system prompt targeted at "code reviewer specialized in WordPress security" does it better, with stable criteria from one session to another.
3. **Multiple delegation**. On an articulated task — *"review this PR for security, performance, and style"* — you can delegate the three angles of analysis to three different subagents and receive three independent summaries, instead of keeping everything in the same tab.

### 12.2 Subagent vs main agent: the concrete difference

Technically, a subagent differs from the main agent on four dimensions:

- **Separate context window**: starts from zero, sees only the prompt the main session passes to it.
- **Tool restrictions**: you can limit available tools (e.g., only `Read`, `Grep`, `Glob` for a read-only agent).
- **Dedicated system prompt**: it has its own instructional "personality", independent from the main session.
- **Model override**: it can run on a different model (e.g., Haiku for speed on massive tasks while the main session stays on Sonnet).

The subagent isn't directly invokable by you: Claude invokes it via the `Agent` tool (renamed from `Task` in v2.1.63 — the `Task(...)` alias is still active for backward compatibility). You ask the main agent for a result, and the main agent decides whether to delegate to a subagent based on the latter's `description`.

### 12.3 Built-in subagents

Claude Code includes some subagents available out-of-the-box. The three relevant for daily use are:

- **Explore** — runs on Haiku, is read-only (`Glob`, `Read`, `Grep`, `Bash`). The main agent invokes it for codebase searches when a query requires reading many files. Accepts a depth level: `quick` (targeted lookup), `medium` (moderate exploration), `very thorough` (exhaustive search across multiple naming conventions).
- **Plan** — used in Plan Mode (see [section 5](#plan-mode-think-before-you-write)). Inherits the session's model, is read-only, exists because in Plan Mode searches must also remain in the non-destructive perimeter.
- **general-purpose** — the generalist agent for multi-step tasks when you don't have a specialized agent. Inherits the model and has access to all tools. It's the one the main agent invokes when you say *"delegate this thing to a subagent"* without specifying which one.

There are two more built-in agents for more internal use: `statusline-setup` (configures the status line, activated by `/statusline`) and `Claude Code Guide` (runs on Haiku, answers questions about the CLI itself). I name them only for completeness.

### 12.4 Creating a custom subagent

You have two ways to create a subagent: **interactive** with the `/agents` command, or **manual** by writing the file.

**Via `/agents`.** Opens a tabbed interface: "Running" lists active agents in the session, "Library" shows available ones with the option to create new ones. The creation flow asks you for scope (Personal / Project), agent description, allowed tools, model, display color, memory. Claude can also **generate the first draft of the system prompt** starting from your description — useful as scaffolding, to be refined by hand.

**Via file.** A subagent is a Markdown file with YAML frontmatter. The path determines the scope:

- **Project**: `.claude/agents/<name>.md` — committed in the repo, shared with the team.
- **User**: `~/.claude/agents/<name>.md` — personal, accompanies you on all the machine's projects.

Concrete example in the WordPress space, a subagent dedicated to security audit of plugins:

```markdown
---
name: wp-security-auditor
description: |
  Use this agent to audit WordPress plugin code for security issues.
  Triggers on: PHP files in wp-content/plugins, mentions of nonce,
  capability checks, sanitize_*, esc_*, $wpdb queries, REST API
  endpoints, AJAX handlers.
tools: Read, Grep, Glob
model: sonnet
color: red
---

You are a security auditor specialized in WordPress plugins.

For every PHP file you analyze, verify in order:

1. **Nonce verification** on every handler that modifies state
   (form submit, AJAX action, REST endpoint).
2. **Capability check** (`current_user_can()`) before privileged
   actions.
3. **Input sanitization**: all `$_GET`, `$_POST`, `$_REQUEST`
   passed through `sanitize_text_field`, `sanitize_email`,
   `absint`, etc., according to the expected type.
4. **Output escaping**: every printed string must pass through
   `esc_html`, `esc_attr`, `esc_url`, `wp_kses_post` according
   to context.
5. **SQL queries**: always use `$wpdb->prepare()` for queries with
   variables. Never direct concatenation.
6. **File operations**: validate path, avoid path traversal.

Regulatory references:

- Plugin Security Handbook: https://developer.wordpress.org/plugins/security/
- WordPress Coding Standards: https://developer.wordpress.org/coding-standards/

Structured output for each file:

- File and line
- Severity: critical / high / medium / low
- Vulnerability identified
- Recommended fix with example of correct code

Don't modify code. Limit yourself to the report.
```

The tools are limited to `Read`, `Grep`, `Glob`: the agent **cannot** modify files, launch shell commands, access the network. It's a read-only reviewer, by design — exactly what you want from a security audit.

The most relevant frontmatter fields:

| Field | Type | Function |
|---|---|---|
| `name` | string (required) | Unique ID, lowercase with hyphens, max 64 characters |
| `description` | string (required) | When the main agent should delegate to this subagent |
| `tools` | list | Allowlist of allowed tools (default: inherits all) |
| `disallowedTools` | list | Denylist of forbidden tools (applied before `tools`) |
| `model` | string | `haiku`, `sonnet`, `opus`, `inherit` or full ID |
| `permissionMode` | string | `default`, `acceptEdits`, `auto`, `plan`, `bypassPermissions` |
| `color` | string | Display color in the session |
| `memory` | string | Auto Memory scope: `user`, `project`, `local`, or absent |
| `isolation` | string | Set to `worktree` to isolate the agent in a temporary git worktree |

### 12.5 Precedence hierarchy

If a subagent with the same name exists at multiple levels, **the most specific one** wins. Order of precedence, from highest to lowest:

1. **Managed settings** (organizational configuration, rare in individual setups)
2. **`--agents` CLI flag** (subagents defined for the single session via launch flag)
3. **Project's `.claude/agents/`**
4. **User's `~/.claude/agents/`**
5. **Agents provided by installed plugins**

Practical convention: keep in `~/.claude/agents/` the **personal and generic** agents (e.g., `code-reviewer-style`, `commit-message-writer`), and in the repo's `.claude/agents/` the **project-specific** agents, shared with the team via Git. Plugin agents use the namespace `<plugin>:<agent-name>` so they don't collide.

### 12.6 Automatic vs explicit invocation

There are two ways to activate a subagent.

**Automatic.** The main agent reads the `description` of all available subagents and decides whether to delegate based on the match with the current task. That's why the `description` is the most important field of the frontmatter: write it thinking of the **concrete triggers** of the workflow, not as a marketing paragraph.

```yaml
# Bad (vague, doesn't trigger well)
description: Agent for WordPress security.

# Good (specific, indicates real triggers)
description: |
  Use this agent to audit WordPress plugin code for security issues.
  Triggers on: PHP files in wp-content/plugins, mentions of nonce,
  capability checks, sanitize_*, esc_*, $wpdb queries.
```

**Explicit.** When you want to force the use of a specific agent, you mention it with `@`:

```
@agent-wp-security-auditor analyze the latest changes to the
plugin in wp-content/plugins/access-control/
```

Typing `@` opens a typeahead picker showing the available agents. For agents provided by plugins the syntax is `@agent-<plugin>:<name>`.

### 12.7 Parallelism: multi-delegation patterns

A note of honesty on this point, because "parallel agents" are sold around with lightness.

Normal subagents in Claude Code run **sequentially** in foreground: the main agent launches one, waits for the result, launches another. There's no standard simultaneous concurrency. What we call "parallelism" is almost always a **multi-delegation with context isolation**: you launch three independent subagents one after the other, each with its own tab, and you receive three independent summaries — the advantage is the separation of context, not execution time.

"Parallel deep review" pattern (more correctly: delegated deep review):

```
You: "Review this PR with three angles: security, performance,
      style. Delegate each angle to a dedicated subagent and
      summarize the three reports at the end."

Claude:
  → Agent(wp-security-auditor)    [security analysis]   ← 60s
    Result: 3 security issues in 2 files

  → Agent(performance-reviewer)   [performance analysis] ← 45s
    Result: 2 N+1 queries, 1 missing cache

  → Agent(style-reviewer)         [style analysis]       ← 30s
    Result: 5 PSR-12 violations, 2 obsolete comments

  Unified summary for the PR.
```

The real advantage is that **the main agent didn't bloat** by reading the files: each subagent did it in its own tab, and only the final aggregation remains in the main. Total time: sum of the three.

**If true simultaneous parallelism is needed**, there's the **Agent Teams** feature: multiple independent instances of Claude Code that really run concurrently, coordinated via shared task list and message mailbox (teammates write to each other directly, not just to the lead like in subagents). Requires Claude Code v2.1.32+ and the env `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` (or equivalent in `settings.json`).

> **⚠️ Experimental feature, to be handled with caution.** Anthropic declares Agent Teams *experimental and disabled by default* in the [official page](https://code.claude.com/docs/en/agent-teams). Relevant known limitations:
>
> - `/resume` and `/rewind` don't restore in-process teammates — after a resume you may have to regenerate the team
> - task state can "lag behind": a task not marked completed blocks dependents
> - shutdown is slow (teammates finish the current turn before exiting)
> - **only one team per session**, no nested teams, lead non-reassignable
> - permissions settable only at spawn (subsequent changes per teammate)
> - **split-pane requires tmux or iTerm2**: doesn't work in VS Code terminal, Windows Terminal, Ghostty
>
> For most workflows, the standard multi-delegation to subagents (described above) is sufficient. Open Agent Teams when you really need teammates dialoguing among themselves — parallel code reviews on different perspectives, debugging with concurrent hypotheses, cross-layer refactor where each teammate owns a different layer.

If you decide to use them, the dedicated hook events `TeammateIdle`, `TaskCreated`, and `TaskCompleted` (see [section 13.3 — Lifecycle events](#lifecycle-events)) allow applying quality gates that the Anthropic docs suggest to discipline teammate behavior: block malformed tasks at creation, reject "completed" if tests fail, restart an idle teammate when it still has pending work.

### 12.8 Cost optimization via model routing

The frontmatter's `model` field enables one of Claude Code's most underestimated patterns: **routing simple tasks to Haiku** instead of Sonnet. Haiku costs a fraction of Sonnet (input/output) and on well-defined tasks — pattern matching across many files, classification, structured extraction — quality is more than adequate.

Typical case: you need to audit 50 PHP files to find which use `$wpdb->query()` with concatenation instead of `$wpdb->prepare()`. It's a pattern recognition task, not architectural reasoning.

```yaml
---
name: wp-sql-injection-scanner
description: |
  Use this agent to scan PHP files for direct concatenation in
  $wpdb queries (potential SQL injection). Triggers on: requests
  to audit SQL safety, mentions of $wpdb, manual SQL hardening.
tools: Read, Grep, Glob
model: haiku    # Haiku is plenty, costs much less
---

You are a WordPress SQL injection scanner.

Look for all files that call $wpdb->query(),
$wpdb->get_results(), $wpdb->get_var(), $wpdb->get_row()
with SQL strings that concatenate variables (`.` or interpolation).

For each occurrence:
- File and line
- Snippet of the offending query
- Corrected version using $wpdb->prepare()

Ignore cases where the query is 100% static (no variables).
```

The main agent (Sonnet) coordinates and produces the final report; the subagent (Haiku) does the massive scan work. The token bill drops significantly. The same principle applies to extractions, summaries, classifications — see also the logic of [`opusplan` in section 5](#plan-mode-think-before-you-write) for another application of the "right model for the right thing" pattern.

### 12.9 When NOT to use them

Subagents aren't always the right choice:

- **Short tasks**. If the task requires reading 2-3 files, the main agent does it directly in less time. The setup overhead (task description to subagent, wait, parsing the result) exceeds the benefit.
- **When the summary loses information**. If you need the main agent to see **the content** of certain files — not just a summary — delegation hobbles you. The subagent returns its synthesis, not the raw data.
- **Iterative work**. If you're doing incremental refactor that requires continuous back-and-forth (modify, test, modify again), a subagent doesn't help: the main agent is already the right tool, simply with periodic `/compact` to not bloat the context.
- **High-risk tasks where you want direct control**. Destructive operations (delete, force push, DB migrations), interpretation errors by the subagent are costly. Keep them on the main agent in Plan Mode.

When in doubt: start with the main agent. If you find you've read 30 files just to produce 200 tokens of output, it was a subagent.

### 12.10 Subagents, Skills and Hooks compared

Claude Code has **three extension mechanisms** that are easy to confuse. It's worth fixing them together because they do different things and often combine.

| **Aspect** | **Subagent** | **Skill** | **Hook** |
|---|---|---|---|
| What it is | Specialized agent with separate context | Reusable playbook inserted in the main context | Script that intercepts lifecycle events |
| Who writes it | You (`.md` file with YAML frontmatter) | You (`SKILL.md` file with YAML frontmatter) | You (bash/HTTP/prompt script) |
| How it activates | Main agent delegation or explicit `@agent-name` | Automatic match on `description` or `/skill-name` | Automatically on event |
| Context scope | Separate context window | Inline in main context | Side effect, doesn't add context |
| Output | Summary to main agent | Content integrated into the conversation | `allow/deny/ask` decision or action |
| Where they live | `.claude/agents/`, `~/.claude/agents/`, plugins | `.claude/skills/`, `~/.claude/skills/`, plugins | `settings.json` or `.claude/settings.json` |
| Typical use case | Isolated search, specialized review, massive tasks | Project conventions, recurring playbooks, domain knowledge | Command validation, audit, blocking risky operations |

Said in one line: **a Skill enriches the main agent, a Subagent replaces it for the delegated task, a Hook does something around the main agent without being part of it**.

The three mechanisms often **combine**: a Skill can instruct the main agent to delegate a certain task to a specific Subagent, and that Subagent can have a Hook that validates its tool calls before they're executed.

For complete treatment of Hooks — events, types, examples, security — see [section 13](#hooks-automating-claude-codes-lifecycle).

---


---

> ← [11. MCP](11-mcp.md) | [Index](README.md) | [13. Hooks](13-hooks.md) →
