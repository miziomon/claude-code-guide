# Practical Guide to Claude Code CLI

> **Version 4.23 — May 2026** — verified on Claude Code v2.1.123
> Licensed under [Creative Commons BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

> ← [6. Prompt engineering](06-prompt-engineering.md) | [Index](README.md) | [8. Context management](08-context.md) →

---

## 7. Persistent memory: CLAUDE.md and Auto Memory

Claude Code has **two persistent memory mechanisms** that coexist and complement each other: `CLAUDE.md` (a static contract written by you) and Auto Memory (dynamic learnings written by the model). Understanding how they work together is what separates a casual use from a professional one of the CLI.

The first part of this chapter (7.1-7.5) covers `CLAUDE.md`: what it is, how to generate it, what it contains, project examples, hierarchy on monorepos. The second (7.6-7.12) covers Auto Memory: the system introduced in v2.1.59 in which Claude autonomously notes what it learns from your corrections and reapplies it in subsequent sessions.

The `CLAUDE.md` file in the project root is the **contract** between you and Claude. It's automatically read at every session and provides the persistent context you would otherwise have to repeat every time. It's also the **natural destination for prompts that work and recur**: when you find yourself writing the same instruction in many different sessions, its place is here (see [section 6](#prompt-engineering-writing-effective-prompts) on prompt engineering, in particular the principle of prompt "promotion").

### 7.1 Generating CLAUDE.md with /init

On a new project where `CLAUDE.md` doesn't yet exist, the fastest way to start is the `/init` command. Launched from the project root, Claude analyzes the codebase (folder structure, `package.json`/`composer.json`/`requirements.txt`, configuration files, README, any tests) and generates a draft `CLAUDE.md` with detected stack, main commands, and inferred conventions.

```bash
# From the project root
claude
> /init
```

The output is a **good starting point**, not a definitive file. It should always be re-read and enriched by hand for two reasons:

- Claude can poorly infer conventions when existing code isn't uniform (e.g., half the project in camelCase, half in snake_case)
- The **tribal rules** not written in the code — "we don't use jQuery here", "every endpoint must have a Zod schema", "tests hit the real database, never mock" — Claude can't make them up: you have to add them.

Consider `/init` as scaffolding: it saves you 20 minutes of initial writing, then it's up to you.

### 7.2 What to put in CLAUDE.md

A good structure includes:

1. **Project description** — what it is, who it's for
2. **Technology stack** — languages, frameworks, versions
3. **Code conventions** — naming, patterns, comment style
4. **Main commands** — build, test, lint, deploy
5. **High-level architecture** — key folders, data flow
6. **What NOT to do** — anti-patterns, hard rules

### 7.3 Example 1: WordPress plugin

```markdown
# WP Access Control Block

## Description
WordPress plugin that adds a Gutenberg block to control
content visibility based on user login state.

## Stack
- PHP 8.1+
- WordPress 6.0+
- JavaScript with @wordpress/scripts (JSX)
- SCSS with BEM methodology

## Conventions
- Code comments: **Italian**
- README and user documentation: **English**
- PHP naming: PSR-12, namespace `Mavida\WPAccessControl\`
- JS naming: camelCase, React components in PascalCase
- CSS: BEM strict (`.block__element--modifier`)

## Commands
- Build: `npm run build`
- Dev watch: `npm run start`
- PHP lint: `composer lint`
- JS lint: `npm run lint:js`
- PHP tests: `composer test`

## Structure
- `src/` — JS/SCSS sources (JSX, SCSS)
- `build/` — compiled output (don't touch manually)
- `includes/` — server-side PHP logic
- `block.json` — block manifest

## Hard rules
- DO NOT use jQuery in new components
- DO NOT commit files in `build/`
- Every PHP hook must have nonce verification
- Server-side render callbacks must be **escaped** with WP functions
```

### 7.4 Example 2: generic Node/TypeScript project

```markdown
# API Analytics Service

## Description
REST microservice to collect and aggregate analytics events.

## Stack
- Node.js 22 LTS
- TypeScript 5.4 (strict mode)
- Fastify 4
- PostgreSQL 16 + Prisma ORM
- Vitest for tests

## Conventions
- All exported types must be in `src/types/`
- Zod schemas for input validation (never trust the client)
- JSDoc comments for all public functions
- No `any`, use `unknown` and narrow

## Commands
- Dev: `pnpm dev`
- Build: `pnpm build`
- Test: `pnpm test`
- Test coverage: `pnpm test:coverage`
- DB migrations: `pnpm prisma migrate dev`

## Architecture
- `src/routes/` — HTTP endpoints
- `src/services/` — business logic
- `src/repositories/` — data access
- `src/schemas/` — Zod validation

## Hard rules
- DO NOT directly import the Prisma client into `routes/` — go through `repositories/`
- Every endpoint must have a Zod schema for body/params/query
- Mandatory tests for every new service
```

### 7.5 Hierarchical CLAUDE.md

Claude Code doesn't read just one `CLAUDE.md`: it reads **more than one**, in order, from the general to the specific. More specific files **integrate** (and where needed override) more general ones. The typical hierarchy is:

1. `~/.claude/CLAUDE.md` — **global user rules**
2. `<monorepo-root>/CLAUDE.md` — **monorepo rules**
3. `<project>/CLAUDE.md` — **single project rules**

#### Global user rules (`~/.claude/CLAUDE.md`)

This is your personal file, valid for **all projects** you open from this machine. You'll find it in:

- **Linux/macOS**: `~/.claude/CLAUDE.md`
- **Windows**: `C:\Users\<your-user>\.claude\CLAUDE.md`

You put your **cross-cutting preferences** in there: comment language, response style, tools you always use, things never to do regardless of project. It's the right place for "I write comments in Italian" or "never propose me solutions with jQuery if a vanilla alternative exists".

#### What is a monorepo

A **monorepo** is a single Git repository that contains **multiple related projects** instead of having one for each. It's very common in modern development: a company that maintains multiple WordPress plugins together, or a team that keeps an API, a frontend, and a shared library in the same repo.

A typical structure:

```
my-monorepo/
├── CLAUDE.md                    ← rules common to all sub-projects
├── plugins/
│   ├── access-control/
│   │   └── CLAUDE.md            ← rules specific to this plugin
│   └── analytics/
│       └── CLAUDE.md            ← rules specific to this plugin
└── shared/
    └── utils/
```

The monorepo-level `CLAUDE.md` captures what's **common**: naming conventions, base stack, orchestrated build commands. The single-project `CLAUDE.md`s cover **specifics**: rules that only apply to that sub-project.

#### Differences from a single project

When you work on an isolated project (not in a monorepo), the hierarchy reduces to two levels: user rules + project rules. The project's `CLAUDE.md` contains everything that in a monorepo would be spread across two files. Nothing wrong with this: the hierarchy exists to avoid duplication, not to be mandatory.

#### Practical three-level example

Suppose you develop WordPress plugins and keep your work in a monorepo.

**`~/.claude/CLAUDE.md`** — personal preferences, valid everywhere:

```markdown
# Personal preferences

- Code comments: Italian
- Responses: concise, get to the point, no preambles
- When proposing PHP code, always follow PSR-12
- Don't propose solutions with jQuery if a vanilla JS alternative exists
- Before large structural changes, ask for confirmation
```

**`<monorepo-root>/CLAUDE.md`** — rules common to all plugins in the monorepo:

```markdown
# WordPress Plugins Monorepo

## Common stack
- PHP 8.1+, WordPress 6.4+
- Build with @wordpress/scripts (npm)
- Tests with PHPUnit + WP Test Suite

## Common conventions
- Root namespace: `MyCompany\`
- All plugins are prefixed `mc-` (e.g., `mc-access-control`)
- Translation files live in `<plugin>/languages/`

## Orchestrated commands
- Build all plugins: `npm run build:all`
- Test all plugins: `composer test:all`

## Hard rules
- Every hook must verify nonce and capability
- No unescaped output: use `esc_html`, `esc_attr`, `wp_kses_post`
```

**`<monorepo-root>/plugins/access-control/CLAUDE.md`** — rules only for this plugin:

```markdown
# Plugin: Access Control

## Description
Gutenberg block to control content visibility
based on user login state.

## Specifics
- Block name: `mycompany/access-control`
- Server-side rendering via `render_callback` (no JS in frontend)
- Visibility rules are in `includes/Visibility/Rules.php`

## What NOT to touch
- Don't modify `block.json` without regenerating the asset manifest
- The `mc_access_control_can_view` filters are public API: no breaking changes
```

When you open Claude Code inside `plugins/access-control/`, it sees all three levels combined: your preferences + monorepo conventions + plugin specifics. You write each rule **once, at the right level**, and reuse it automatically wherever it makes sense.

`CLAUDE.md` is the **static** half of Claude Code's persistent memory: you write it, it contains the rules. There's also a **dynamic** half that Claude feeds itself over time — that's Auto Memory, introduced in v2.1.59 and covered in the second part of this chapter.

---

Starting from **version 2.1.59** Claude Code introduced a second persistent memory mechanism, complementary to `CLAUDE.md`: **Auto Memory**. The difference is sharp:

- **`CLAUDE.md`** is **static** — you write it once, it's read at every session, contains rules and instructions.
- **Auto Memory** is **dynamic** — Claude writes it itself while working, accumulating what it has learned from your corrections and from past sessions.

These are two mechanisms that coexist: one is the **contract** you set, the other is the **learning diary** the model keeps for itself.

### 7.6 Auto Memory: what it is and what changes

The idea is simple: today if you correct Claude three times on the same thing — *"don't use `var`, here we use `let`/`const`"* — by the fourth time, in a different session, it does it again. Without persistent memory, every session starts from zero. Auto Memory closes this loop: Claude autonomously notes the rule and reapplies it to subsequent sessions.

When Claude decides to save something, it does so based on an internal criterion: will the information be useful in future conversations? Recurring build commands, naming conventions you've corrected, project architectural patterns, typical errors to avoid. Anthropic's documentation doesn't describe the mechanism in detail; in practice it works better on recurring patterns than on individual occurrences.

> **Concrete example.** You work on a PHP codebase that uses `snake_case` for function names. Claude initially proposes `camelCase` (JavaScript-style default). You correct once, twice, three times. Auto Memory notes the project convention. By the fourth session, before you even open your mouth, Claude already proposes `snake_case`. The explicit correction is no longer needed: the model has learned.

### 7.7 Requirements and enabling

- **Minimum version**: Claude Code 2.1.59. Verify with `claude --version` and update if necessary.
- **Default state**: **active**. You don't have to do anything to enable it.
- **Management command**: `/memory` shows all `CLAUDE.md`, `CLAUDE.local.md` files and rules loaded in the current session, allows toggling Auto Memory on/off, and provides a direct link to open the memories folder in the editor.
- **Persistent disabling**: in `settings.json` (user or local, **not** project, for security reasons):

  ```json
  { "autoMemoryEnabled": false }
  ```

- **Disabling via env**: the environment variable `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1` turns off the feature for a single session. Useful in CI/CD or one-off sessions.
- **Moving the folder**: the `autoMemoryDirectory` setting (always in user/local settings) lets you save memories to a custom path — for example a directory synchronized with another device via cloud, or an encrypted location.

### 7.8 Where memories live

Standard path:

- **Linux/macOS**: `~/.claude/projects/<project>/memory/`
- **Windows**: `C:\Users\<your-user>\.claude\projects\<project>\memory\`

The `<project>` segment is derived from the **Git repository** (remote URL). Outside a Git repo, the working directory root is used. Important consequence: **worktrees and subdirectories of the same repo share the same memory**. If you keep two copies of the repo to work in parallel on two branches, Claude learns from both sessions as if they were one.

### 7.9 Anatomy of the memory folder

Inside `memory/` there isn't a single file: there's an **index** plus **topic files**.

```
~/.claude/projects/myproject/memory/
├── MEMORY.md              ← index, loaded at every session
├── debugging.md           ← topic file: recurring debug patterns
├── api-conventions.md     ← topic file: project API rules
└── build-commands.md      ← topic file: orchestrated build commands
```

- **`MEMORY.md`** is the index. It's loaded at **every session**, but only for the **first 200 lines** (about 25 KB). Anthropic recommends keeping it within this limit so as not to waste context.
- **Topic files** (`debugging.md`, `api-conventions.md`, etc.) are loaded **on-demand**: only when their content is relevant to the current task. They can be arbitrarily long without saturating the session context.

This is the **key technical difference compared to CLAUDE.md**, which is always read in full. Auto Memory is designed to **scale**: you can accumulate knowledge over time without paying for it in tokens at every session.

### 7.10 Auto Memory and subagents

Subagents (see section 12) can maintain their **own** Auto Memory, separate from the main session's. It's designed for specialized subagents that perform recurring tasks — for example, a code review agent that learns over time the preferred review style — without polluting the general work memory. Configuration is set at the subagent definition level.

### 7.11 When to disable it

Auto Memory doesn't leave the computer: everything lives in `~/.claude/projects/...` on your local machine, and memories **are not sent to Anthropic for training**. Disabling is therefore not a privacy issue toward Anthropic, but one of **local control** in specific scenarios:

- **Codebase with sensitive data**: if fragments of real data (PII, secrets, clinical data) appear in chat, you prefer not to leave traces even in a local file that could be copied for backup, synced elsewhere, or read by someone with physical access to the machine.
- **Regulated projects**: in healthcare, finance, or GDPR contexts, some corporate policies prohibit any form of persistent memory outside controlled systems. Disabling Auto Memory is the safe choice to remain compliant.
- **Exploratory sessions**: you're experimenting with an approach you'll likely abandon. You don't want Claude to learn patterns from a transient solution and re-propose them in the future as if they were established rules.

When in doubt, start active and disable per session or project when needed.

### 7.12 CLAUDE.md vs Auto Memory: when to use what

| **Aspect** | **CLAUDE.md** | **Auto Memory** |
|---|---|---|
| Who writes it | You | Claude |
| What it contains | Instructions and rules | Learnings and patterns emerged while working |
| Scope | Project, user, organization | Per repository (a single folder per repo) |
| Loaded in session | Always, in full | `MEMORY.md` always (max 200 lines), topic files on-demand |
| Typical content | Stack, conventions, commands, hard rules | Recurring build commands, style nuances, already-corrected errors |

**Recommended pattern**: use `CLAUDE.md` for **hard rules** — the things you don't want to renegotiate every time — and leave Auto Memory for the **nuances** that emerge while working. If you notice that a learned memory is important and stable, **promote it** by manually transferring it to `CLAUDE.md`. From that moment it's a contractual rule, not just an observation that Claude could forget if it revises the file.

> For those who already know the distinction, there's a complementary third way: **`CLAUDE.local.md`**, a manual Markdown file like `CLAUDE.md` but **gitignored** by default. You write it, it's specific to your local copy, isn't committed. It's useful for personal preferences of a single dev on a shared project (paths to local tools, your own shortcuts), without imposing them on the team.

---


---

> ← [6. Prompt engineering](06-prompt-engineering.md) | [Index](README.md) | [8. Context management](08-context.md) →
