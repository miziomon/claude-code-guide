# Practical Guide to Claude Code CLI

> **Version 4.30 — May 2026** — verified on Claude Code v2.1.123
> Licensed under [Creative Commons BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

> ← [14. Plugins](14-plugins.md) | [Index](README.md) | [16. Conclusions](16-conclusions.md) →

---

## 15. Advanced workflows and tips

The previous chapters built the conceptual foundations — commands, Plan Mode, memory, context, security, skills, plugins, subagents, hooks. This chapter is the toolbox: first four **practical workflows** (15.1-15.4) that combine the foundations into concrete daily use scenarios, then six **tips** (15.5-15.10) for those who want to push the tool's efficiency further.

### 15.1 Onboarding to an existing repository

```
Prompt: "You've just been assigned to this project. Analyze the
structure, identify:
1. Main architectural patterns (MVC, hexagonal, etc.)
2. How authentication is managed
3. Where the integration points with external services are
4. Naming and style conventions
5. Any evident technical debts

Produce an onboarding document in docs/ONBOARDING.md.
Don't modify any other code."
```

**Why it works:**
- Clear objective with numbered list
- Specific output (a file in known position)
- Explicit constraint ("don't modify anything else")

### 15.2 Bug hunting with TDD

```
Prompt: "Bug report: when a user with 'editor' role tries to
modify a 'private' post, they get a 500 error. Log attached:
[paste log].

Required workflow:
1. Activate Plan Mode and analyze the code involved
2. FIRST write a test that reproduces the bug (must fail)
3. Fix the bug with the MINIMAL modification needed
4. Verify that the test passes
5. Run the full suite to exclude regressions"
```

**Why it works:**
- Forces a disciplined TDD approach
- Avoids "quick fixes" that suppress symptoms
- The test written first becomes documentation of the bug

### 15.3 Safe refactoring

```
Prompt: "The includes/class-order-processor.php module has become
unmanageable (800 lines, multiple responsibilities). I want
to refactor it.

Phase 1 — CHARACTERIZATION (Plan Mode):
- Identify all currently mixed responsibilities
- Propose a decomposition into smaller classes
- List the tests that MUST exist before touching the code

Stop here and wait for my approval of the plan."
```

After approval:

```
"Proceed with Phase 2:
- Write characterization tests that lock the current
  behavior
- Run them and confirm they all pass
- Make a commit with message 'test: pre-refactoring characterization'"
```

And then:

```
"Phase 3 — incremental refactoring:
- Extract one responsibility at a time
- After each extraction, run the tests
- If even ONE test fails, stop and ask"
```

### 15.4 Performance audit

```
Prompt: "Analyze the production build and identify the 5 highest-impact
performance problems. For each one:
- File and lines involved
- Estimated impact (ms, KB, HTTP requests)
- Proposed fix
- Fix complexity (low/medium/high)

Sort by impact/complexity ratio. Don't modify anything."
```

The tips that follow (15.5-15.10) are individual tricks, to pick at will when the use case arises.

### 15.5 Vim mode

If you come from Vim, enable the mode in `/config` → Editor mode. You'll have navigation with `hjkl`, commands `d`, `y`, `p`, etc.

### 15.6 Custom slash commands

You can create custom slash commands by saving Markdown files in `.claude/commands/`. The file becomes the prompt Claude executes when you invoke the command.

#### Structure of a command file

```markdown
---
description: Short description shown in the picker (max ~80 chars)
allowed-tools: Read, Bash, Glob
argument-hint: "[area-to-analyze]"
---

Here the command prompt. You can use $ARGUMENTS to reference the optional
argument passed to the command (e.g. /security-audit src/auth).
```

The **YAML frontmatter** is optional but recommended:

- `description` — appears in the `/` picker and the command listing.
- `allowed-tools` — list of tools the command can use. If omitted, all tools are available.
- `argument-hint` — string shown in the picker as an argument hint.

#### Basic example: security audit

```markdown
<!-- .claude/commands/security-audit.md -->
---
description: OWASP top-10 audit for the plugin's PHP code
allowed-tools: Read, Grep, Glob
---
Run a security audit focused on:
1. SQL injection in direct queries
2. XSS in unescaped output
3. CSRF without nonce verification
4. Path traversal in filesystem operations
5. Hardcoded credentials

For each issue found: file, line, severity (low/medium/high/critical),
suggested fix.
```

#### Recipe: `/audit-context` — consumption snapshot before a heavy task

```markdown
<!-- .claude/commands/audit-context.md -->
---
description: Context snapshot: token usage, config sizes, active MCP servers
allowed-tools: Bash
---
Run in sequence:
1. /context to show current context usage by category.
2. /cost to show tokens consumed and estimated session cost.
3. wc -l CLAUDE.md .claude/settings.json 2>/dev/null to show the sizes
   of project configuration files.

Then summarize in three lines: context percentage used, heaviest entries,
and whether there's anything to do before continuing (compact, disable an
unused MCP server, etc.).
```

From a session: `/audit-context` gives you the full picture in seconds before starting a heavy task. Equivalent to the preventive check described in [section 8.4](#the-context-command-reading-and-acting), but on-demand and with a final synthesis produced by the model.

#### Recipe: `/snapshot` — preserve state before compacting

```markdown
<!-- .claude/commands/snapshot.md -->
---
description: Save a session brief to docs/snapshots/ before /compact
allowed-tools: Bash, Write
---
Before proceeding with /compact or /clear, create a textual snapshot of
the current session state.

1. List modified files: git diff --name-only HEAD (or git status --short).
2. Summarize in at most 10 bullets the architectural decisions made, problems
   solved, and tasks still open.
3. Write the summary to docs/snapshots/ with name snapshot-YYYYMMDD-HHMM.md.

The snapshot file serves as a brief for the next session that resumes this
work with --resume. Keep it concise: 200-300 words, bullet points, no
introductions.
```

From a session: `/snapshot` followed by `/compact` is the sequence that preserves key details without keeping the full transcript in context. The next `--resume` session finds the brief ready in `docs/snapshots/`.

> **Slash commands vs hooks.** Custom slash commands are **on-demand**: you invoke them when needed. Hooks (chapter 13) are **automatic**: they fire on lifecycle events regardless of your decision. Use slash commands for recipes you want to control; use hooks for automations that must always happen.

### 15.7 Headless mode for CI/CD

The `-p` (print) flag executes Claude in non-interactive mode, perfect for pipelines:

```bash
# GitHub Actions example
claude -p "Review the changes in this PR and flag any security issues" \
       --output-format json > review.json
```

The `--output-format json` produces structured output parseable by subsequent steps.

### 15.8 Session recap

If you leave the terminal and return after 3+ minutes, Claude Code automatically shows a summary of what was done. Great for context-switching. You can force it with `/recap`.

### 15.9 Strategic Git checkpoints

Before risky tasks, ask explicitly:

> *"Before proceeding, make a commit with message 'pre-refactoring checkpoint' so we have a safe return point."*

If something goes wrong, `git reset --hard HEAD~1` brings you back to the previous point.

### 15.10 Conversation forks

Press `Esc` twice to go back to a previous message and re-edit it. Creates a "branch" of the conversation — useful when a prompt didn't give the desired result and you want to reformulate without losing everything.

---


---

> ← [14. Plugins](14-plugins.md) | [Index](README.md) | [16. Conclusions](16-conclusions.md) →
