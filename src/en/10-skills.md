# Practical Guide to Claude Code CLI

> **Version 4.23 — May 2026** — verified on Claude Code v2.1.123
> Licensed under [Creative Commons BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

> ← [9. Security and permissions](09-security.md) | [Index](README.md) | [11. MCP](11-mcp.md) →

---

## 10. Skills: the extension mechanism

Skills are specialized "playbooks" that Claude can consult automatically when it detects that a certain type of task is in play. **Important**: unlike slash commands, **Skills aren't invoked by a command**. They activate automatically based on their `description`.

### 10.1 How a Skill works

A Skill is a folder with a `SKILL.md` file structured like this:

```markdown
---
name: wordpress-block-builder
description: "Use this skill when building or modifying WordPress
Gutenberg blocks. Triggers on: block.json, @wordpress/scripts,
JSX files in WordPress plugins, Edit/Save components."
---

# WordPress Block Builder

## Project conventions
- Always use @wordpress/scripts for the build
- Every block must have block.json, edit.js, save.js, style.scss
- Attributes must be typed in block.json

## Recommended patterns
[...]
```

The `description` field determines **when** Claude will use the Skill. It's the most important piece: write it thinking of the concrete triggers of your workflow.

A well-made skill leverages **progressive disclosure**: the `SKILL.md` file contains only what's essential to activate it; heavier resources (auxiliary Python scripts, configuration JSON, reference documents) live in adjacent folders and are loaded only when Claude decides they're needed. Result: the skill doesn't bloat the context until the moment of actual use.

### 10.2 Bundled native skills — deep dive

Anthropic distributes a set of official skills in the public repository [`github.com/anthropics/skills`](https://github.com/anthropics/skills). Some are bundled with Claude Code, others must be installed separately (see [section 10.4](#installing-and-managing-skills)). Below are the eight most relevant native skills, each with reference metadata, an operational description, and a concrete usage example. All have the same author, the same monorepo repository, and Apache 2.0 license; the "Invocation" field indicates the typical triggers Claude reacts to by activating the skill.

#### 10.2.1 pdf

| Key | Value |
|---|---|
| **Author / repo** | Anthropic — [`github.com/anthropics/skills/pdf`](https://github.com/anthropics/skills/tree/main/pdf) |
| **License** | Apache 2.0 |
| **Invocation** | `.pdf` attachments, requests for extraction/fill/merge on PDF files |

**Extended description.** Creation, text extraction, form filling, and merge/split of PDF files. The skill handles field positioning and typing when the user indicates a template and the data to insert. It activates automatically when PDF attachments appear in conversation or when the user requests operations on this format.

**Usage example.**

```bash
> "Open invoice-2026-04.pdf and extract the rows of the
   articles table in CSV format (code, description, qty, amount)"
```

#### 10.2.2 docx

| Key | Value |
|---|---|
| **Author / repo** | Anthropic — [`github.com/anthropics/skills/docx`](https://github.com/anthropics/skills/tree/main/docx) |
| **License** | Apache 2.0 |
| **Invocation** | `.docx` files, requests to generate/modify Word documents from templates |

**Extended description.** Creation and modification of Word documents preserving styles, headings, tables, and images. Typical for periodic reports produced from corporate templates, maintaining formatting and existing layout while replacing dynamic content.

**Usage example.**

```bash
> "Open template-monthly-report.docx and fill it with the data
   in stats-april.csv. Replace only the {{...}} placeholders,
   leave the rest of the formatting unchanged."
```

#### 10.2.3 pptx

| Key | Value |
|---|---|
| **Author / repo** | Anthropic — [`github.com/anthropics/skills/pptx`](https://github.com/anthropics/skills/tree/main/pptx) |
| **License** | Apache 2.0 |
| **Invocation** | `.pptx` files, requests to generate presentations or slide decks |

**Extended description.** Generation and modification of PowerPoint presentations with layouts, images, tables, and shapes. Particularly useful for repetitive slide decks (status meetings, training sessions) generated from outlines in Markdown or JSON.

**Usage example.**

```bash
> "Generate an 8-slide presentation starting from the file
   training-claude-code.md. One slide for each h2 found,
   bullet list of contents below."
```

#### 10.2.4 xlsx

| Key | Value |
|---|---|
| **Author / repo** | Anthropic — [`github.com/anthropics/skills/xlsx`](https://github.com/anthropics/skills/tree/main/xlsx) |
| **License** | Apache 2.0 |
| **Invocation** | `.xlsx`, `.csv` files, requests for spreadsheets / dashboards / pivot tables |

**Extended description.** Excel spreadsheets with formulas, conditional formatting, pivot tables, and charts. Suited for quick dashboards, data consolidations, and reports that would require a lot of manual setup in a new sheet.

**Usage example.**

```bash
> "Starting from sales-q1.csv generate an xlsx with a 'Data'
   sheet (raw), a 'Pivot' sheet (pivot by client x month),
   a 'Top10' sheet (top 10 articles with bar chart)."
```

#### 10.2.5 frontend-design

| Key | Value |
|---|---|
| **Author / repo** | Anthropic — [`github.com/anthropics/skills/frontend-design`](https://github.com/anthropics/skills/tree/main/frontend-design) |
| **License** | Apache 2.0 |
| **Invocation** | Requests for web pages, React components, HTML layouts, landing pages |

**Extended description.** Guidelines and patterns to produce distinctive UIs that avoid the "generic AI" style (gradients, excessive shadows, pastel palette). Pushes Claude toward more targeted typographic choices, palettes, and compositions, reducing the tendency to banal visual defaults.

**Usage example.**

```bash
> "Create a React landing page for a new B2B SaaS product.
   Professional tone, sober palette, hero + features +
   pricing + cta sections. No generic gradients and
   'shiny' buttons."
```

#### 10.2.6 webapp-testing

| Key | Value |
|---|---|
| **Author / repo** | Anthropic — [`github.com/anthropics/skills/webapp-testing`](https://github.com/anthropics/skills/tree/main/webapp-testing) |
| **License** | Apache 2.0 |
| **Invocation** | Requests to "test" a web app, smoke tests, end-to-end verification |

**Extended description.** End-to-end testing of web applications with Playwright in headless mode. Activates when Claude is asked to test a web app running locally: the skill orchestrates navigation, form filling, assertions, and comparison screenshots.

**Usage example.**

```bash
> "Start the app on localhost:3000, navigate to /signup,
   fill the form with valid data, verify that after
   submit the confirmation message appears. Then repeat
   with malformed email and verify the error."
```

#### 10.2.7 skill-creator

| Key | Value |
|---|---|
| **Author / repo** | Anthropic — [`github.com/anthropics/skills/skill-creator`](https://github.com/anthropics/skills/tree/main/skill-creator) |
| **License** | Apache 2.0 |
| **Invocation** | Explicit requests to "create a skill" or "skill scaffolding" |

**Extended description.** Meta-skill that interviews the user, gathers requirements, and produces a new skill (frontmatter, content, any auxiliary scripts). Recommended entry point for those who have never written a skill: Claude poses targeted questions (triggers, output format, examples) and generates the `.claude/skills/<name>/` folder ready to use.

**Usage example.**

```bash
> "I want to create a skill that helps me write ADRs
   (Architecture Decision Records) consistent with my
   team's template. Help me set it up with skill-creator."
```

#### 10.2.8 mcp-builder

| Key | Value |
|---|---|
| **Author / repo** | Anthropic — [`github.com/anthropics/skills/mcp-builder`](https://github.com/anthropics/skills/tree/main/mcp-builder) |
| **License** | Apache 2.0 |
| **Invocation** | Requests for MCP server scaffolding or exposure of an external API |

**Extended description.** Meta-skill mirror of `skill-creator` but for MCP servers (see [section 11](#mcp-integrating-external-services)). Generates the scaffold of an MCP server starting from a description of the API or service to expose, including SDK and basic tool structure.

**Usage example.**

```bash
> "Build an MCP server that exposes our internal ticketing
   API. Base endpoint: api.mavida.local/v2.
   Operations: list_tickets, get_ticket, create_ticket,
   add_comment. Auth via X-API-Key header."
```

> **Note** — The subset of skills bundled with Claude Code may vary over time. The source of truth is always the official repository [`github.com/anthropics/skills`](https://github.com/anthropics/skills), also cited in Appendix B.

### 10.3 Community skills: a curated selection

The ecosystem produces dozens of skills every month and quality is highly variable. Those that follow have been selected with criterion: official repository of a recognizable author or organization, clear open license, adequate documentation, recent maintenance activity. For each you'll find a card with essential data, an extended description, cases when it's worth installing, cases when it's not, an editorial assessment, and — where useful — a usage example.

> **Disclaimer** — The ecosystem is in very rapid evolution. The skills selected here were active and well-maintained at the time of writing (May 2026); always verify the repo's health (last commit date, open issues, license) before installing them.

#### 10.3.1 Superpowers

| Key | Value |
|---|---|
| **Author / repo** | Jesse Vincent — [`github.com/obra/superpowers`](https://github.com/obra/superpowers) |
| **License** | MIT |
| **Stars** | ~173k |
| **Invocation** | Activates on non-trivial tasks: new features, complex bugs, structural refactorings |

**Extended description.** Complete methodology for agents: brainstorming → planning → TDD → review → execution. Not a single skill but a framework of composable skills that imposes a structured, multi-platform workflow (Claude, Cursor, OpenAI Codex, Gemini). Forces Claude not to skip the analysis and planning phases even when the task seems solvable at a glance.

**When to use it.**

- You develop complex features where "diving into the code" leads to rewrites
- You want a rigorous workflow out-of-the-box without building conventions from scratch
- You work in teams where adherence to a shared methodology is important

**When NOT to use it.**

- You have to make small, localized changes (a three-line bug fix doesn't deserve brainstorm + plan + TDD)
- You're used to your own consolidated workflow and want flexibility

**My judgment.** For those coming from the "chat + copy-paste" pattern it's a gear shift. The value isn't in the individual skills but in the **discipline** it imposes: thinking before writing. It works better if adoption is team-wide — because a single developer can quickly find it heavy for daily short tasks and disable it. Worth trying for some non-trivial features before making it the basis of your workflow.

**Usage example.** After installation, ask Claude a non-trivial task (*"Add 2FA authentication to the login module"*). Superpowers forces the brainstorm → plan → test-first → implement → review sequence before touching code.

#### 10.3.2 Vercel Labs Agent Skills

| Key | Value |
|---|---|
| **Author / repo** | Vercel Labs — [`github.com/vercel-labs/agent-skills`](https://github.com/vercel-labs/agent-skills) |
| **License** | MIT |
| **Stars** | ~26k |
| **Invocation** | Activates on React/Next.js files, frontend code review requests, accessibility audits |

**Extended description.** Package of 7 high-level frontend skills: `react-best-practices` (40+ performance rules), `web-design-guidelines` (100+ accessibility/UX rules), `react-native-guidelines`, `composition-patterns`, `react-view-transitions`, `vercel-deploy-claimable`. Codifies the rules published by Vercel Engineering in its best practices docs.

**When to use it.**

- You develop React/Next.js professionally and want code reviewed against known standards
- You need to do accessibility or performance audits on already-written components
- You work with a team that wants uniformity on the frontend stack

**When NOT to use it.**

- The stack is different from React/Next.js (the rules don't apply)
- You're prototyping fast and the rules slow down iteration

**My judgment.** More than a skill, it's a **codified style guide** that Vercel publishes for free. It works for those inside the React ecosystem: if you are, the investment is zero (one install command) and the return is high (more solid code at the first attempt). If you're not, it's useless to install it.

**Usage example.** During a review you ask *"apply `vercel-labs/web-design-guidelines` to all files modified in the last commit"*. Claude executes a punctual audit (focus state, color contrast, form error handling, animations) producing an issue report with reference to the rules violated.

#### 10.3.3 WordPress Agent Skills

| Key | Value |
|---|---|
| **Author / repo** | WordPress (official organization) — [`github.com/WordPress/agent-skills`](https://github.com/WordPress/agent-skills) |
| **License** | GPL-2.0-or-later |
| **Stars** | ~1.4k |
| **Invocation** | Presence of `wp-config.php`, plugin/theme files, references to `block.json` or WP REST API |

**Extended description.** Bundle of 14 WordPress domain skills built on the official docs, to mitigate the known problem of LLMs generating obsolete WordPress patterns (code from WP 4.x, deprecated ACF APIs, `query_posts()` instead of `WP_Query`, etc.). Includes a "router" skill (`wordpress-router`) that classifies the task and routes to the right specific skill.

**When to use it.**

- You develop WordPress plugins or themes, particularly with block editor and Interactivity API
- You want code adhering to official documentation and not to dated patterns
- You work on projects where WordPress security is important (capability, sanitize/escape, nonce)

**When NOT to use it.**

- You only work on WordPress content (posts, pages) and not on code
- The site is headless and WP only acts as CMS via REST/GraphQL (little benefit)

**My judgment.** For those who do WordPress daily, it's the most useful skill in circulation. The problem of "LLMs generating obsolete WP patterns" is real and costly (I've seen AI-generated code use `query_posts()` or ACF v4 in 2026), and this skill eliminates it at the root. Three stars out of three for those working with WordPress; zero for those who don't.

**Usage example.** In a WordPress project ask *"Create a new Gutenberg block to insert a callout box with icon, title, and text"*. `wordpress-router` recognizes the domain and activates `wp-block-development`, which imposes correct `block.json`, deprecation handling, and security patterns from the official docs.

#### 10.3.4 Trail of Bits Skills

| Key | Value |
|---|---|
| **Author / repo** | Trail of Bits — [`github.com/trailofbits/skills`](https://github.com/trailofbits/skills) |
| **License** | CC-BY-SA-4.0 |
| **Stars** | ~5k |
| **Invocation** | Security audit requests, code review for vulnerability assessment, malware analysis |

**Extended description.** 40+ security skills for AI-assisted analysis, testing, and auditing: smart contract security, code auditing (CodeQL/Semgrep), malware analysis, reverse engineering, mobile security, verification techniques. Trail of Bits is one of the most recognizable security consulting companies in the open source space: these skills codify methodologies used in their professional audits.

**When to use it.**

- You need to review third-party code before integrating a library
- You're a security engineer and want to orchestrate CodeQL/Semgrep in a guided way
- You work on projects with external exposure where vulnerability risk is high

**When NOT to use it.**

- You're doing greenfield application development without critical exposure (overkill)
- You're not familiar with the underlying tools (CodeQL, Semgrep): the skill orchestrates but debugging false positives requires expertise

**My judgment.** Serious skill for a serious audience. The CC-BY-SA-4.0 license imposes share-alike on derivatives: if you modify the skills and redistribute them you're bound — verify compatibility with your corporate constraints. For those doing security it's a notable boost; for the rest it's a toolbox you probably won't use.

**Usage example.** Before integrating a third-party PHP library ask *"Run a security audit on the `vendor/foo-lib` folder using Trail of Bits skills. Look for SQLi, command injection, insecure deserialization patterns"*. The skills orchestrate CodeQL/Semgrep and produce a report with file, line, and type of vulnerability.

#### 10.3.5 Caveman

| Key | Value |
|---|---|
| **Author / repo** | Julius Brussee — [`github.com/JuliusBrussee/caveman`](https://github.com/JuliusBrussee/caveman) |
| **License** | MIT |
| **Stars** | ~24k |
| **Invocation** | `/caveman`, `/caveman lite`, `/caveman ultra` commands; natural triggers like *"talk like caveman"* |

**Extended description.** Skill that forces Claude to respond in telegraphic style: no articles, no pleasantries, no hedging, no meta-commentary. Only technical substance. Three compression levels (`lite`, `full`, `ultra`) for increasing intensity. The skill is surgical: it compresses the discursive part of responses (filler, articles, courtesy phrases) but leaves intact code blocks, technical terms, cited error messages, and commit messages.

**When to use it.**

- Mechanical and repetitive coding (refactoring, debugging, linting)
- You're an experienced user and don't need the detailed "why"
- You're orchestrating multiple agents or background tasks where verbose output is just noise
- You're close to your plan limit and want to squeeze out more sessions

**When NOT to use it.**

- You're learning a new framework: you need pedagogy, the "why" is the value
- You're onboarding to an unknown codebase: you want complete explanations
- You're doing architectural review: you want nuances, alternatives, trade-offs

**My judgment.** Caveman is an interesting case of a **viral claim worth reading carefully**. The README promises "75% token savings" and has become the project's reference number, but it's worth disaggregating the data to understand where the savings actually land on your bill:

| Number | What it really measures |
|---|---|
| **65%** | Average compression on the model's **output** (range 22-87%, measured by the repo's benchmarks). |
| **0.6-2.5%** | Share of tokens that the output represents on the **total** of a typical Claude Code session. The bulk of consumption is input: `CLAUDE.md`, conversation history, read files, tool output. |
| **1-2%** | Net savings on the bill in a **normal interactive session** (small output, dominant input). |
| **up to 15-25%** | Savings in **multi-agent parallel scenarios** or headless batch pipelines, where output becomes a larger share of the total (more subagents producing final text, less repeated input). |

In short: the viral "75%" applies only to a tiny slice of consumption in most human sessions, while the higher numbers you read around apply to particular scenarios — not typical, presented as typical. The product itself is honest (open source MIT, reproducible benchmarks in the repo), and the principle is what I take away: thinking of **AI verbosity as a measurable cost**. Once you start reasoning about it, you write lighter `CLAUDE.md` files, more targeted prompts, and efficiency grows even without plugins.

**Usage example.** Normal Claude response (69 tokens):

> *"The reason your React component is re-rendering is likely because you're creating a new object reference on each render cycle. When you pass an inline object as a prop, React's shallow comparison sees it as a different object every time, which triggers a re-render. I'd recommend using `useMemo` to memoize the object."*

Caveman mode response (19 tokens):

> *"New object ref each render. Inline object prop = new ref = re-render. Wrap in `useMemo`."*

Same diagnosis, same solution, no padding.

### 10.4 Installing and managing skills

Skills are installed in three ways depending on how they're distributed.

**Plugin marketplace** — when a skill is packaged as a plugin (typical case for the more structured community skills):

```bash
# Add the author's marketplace
claude plugin marketplace add owner/repo

# Install the specific skill
claude plugin install <skill>@<plugin>
```

**`npx skills` tool** — for standalone skills distributed via Git repo:

```bash
# Install a single skill from a multi-skill repo
npx skills add anthropics/skills --skill frontend-design

# Install the entire skill package from a repo
npx skills add vercel-labs/agent-skills
```

**Manual copy** — for custom or experimental skills. Two possible locations:

```
~/.claude/skills/<name>/SKILL.md       # global (all projects)
.claude/skills/<name>/SKILL.md         # only this project
```

Resolution follows the same hierarchy as other Claude Code resources: global as default, local to project as override.

#### Where to look for new skills

The ecosystem grows very quickly. The most reliable sources today:

- **[`github.com/anthropics/skills`](https://github.com/anthropics/skills)** — official Anthropic repository, first place to check
- **[`skills.sh`](https://skills.sh)** — public community directory, indexes third-party skills with basic metadata
- **Public plugin marketplaces** — authors of mature skills often publish a dedicated marketplace (Trail of Bits, Vercel Labs, JuliusBrussee for Caveman)
- **GitHub topics `claude-skills` and `agent-skills`** — useful for targeted exploration

Before installing anything from third parties, read [section 10.6](#security-of-third-party-skills).

### 10.5 Creating a custom Skill

Nothing prevents you from writing your own skills: indeed, this is the point where Claude Code really becomes "yours". Let's see an end-to-end example of a `mavida-wordpress` skill that codifies your team's conventions.

**Step 1 — Scaffolding**:

```bash
# Skill local to project (override) or global (~/.claude/skills/)
mkdir -p .claude/skills/mavida-wordpress
```

**Step 2 — Writing `SKILL.md`** in `.claude/skills/mavida-wordpress/SKILL.md`:

```markdown
---
name: mavida-wordpress
description: "Use this skill when working on Mavida WordPress
projects. Triggers on: presence of wp-config.php, plugin
files in /wp-content/plugins/, theme files, references to
ACF or Block Editor."
---

# Mavida Conventions — WordPress

## Build and tooling
- Always use @wordpress/scripts for blocks (no custom webpack)
- Composer for PHP dependencies, never manual library upload
- Minimum versions: PHP 8.2, WordPress 6.4

## Mandatory patterns
- All new blocks must have block.json + edit.js + save.js + style.scss
- Strict sanitize/escape: `sanitize_text_field` on input, `esc_html`/`esc_attr` on output
- Nonce on all forms and AJAX actions
- Capability check with `current_user_can()` before privileged operations

## Patterns to avoid
- `query_posts()` (deprecated): use `WP_Query`
- Functions that bypass cache: `wp_cache_flush()` only in seed, never in runtime
- Loading JS via inline wp_head: always via `wp_enqueue_script`

## Common build commands
- `npm run build`: production build of blocks
- `composer test`: PHPUnit + PHPStan level 6
- `wp-env start`: local development environment
```

**Step 3 — Verification**: open Claude Code in a WordPress project and ask for a trivial modification (e.g., "Add a metabox to the Article post type"). If the skill is well-written, you'll see Claude automatically apply the conventions (capability check, sanitize, correct enqueue) without you having explicitly asked.

To check that the skill is loaded: `/skills list` (or `/help skills` depending on the version).

The same pattern applies to other team skills that will come in handy daily:

```
.claude/skills/
├── mavida-wordpress/          # WP conventions
│   └── SKILL.md
├── n8n-workflow/              # patterns for N8N workflows
│   └── SKILL.md
└── php-legacy-review/         # checklist refactoring PHP legacy
    └── SKILL.md
```

A well-written skill is a piece of "team memory" that survives session changes, developer changes, and — increasingly often — tooling changes. When a prompt you use often becomes a rule to systematically impose, it's the signal that it's worth promoting to a skill (see also the reflection on prompt "promotion" in [section 6.8](#promoting-a-prompt-when-it-goes-in-claude.md-or-in-a-custom-command)).

### 10.6 Security of third-party skills

A third-party skill is code that becomes part of Claude's context and can influence its decisions. It doesn't run autonomously — Claude still asks for confirmation before running commands — but it can **instruct Claude to call tools with real effects** (Bash, file system, WebFetch). Treat it as you would treat a library you include in `composer.json` or `package.json`: with the same diligence.

**Checklist before installing a third-party skill:**

- **Mandatory code review** — read `SKILL.md` in full and inspect all auxiliary scripts (Python, Bash, JS) present in the folder. Look for references to destructive commands, data exfiltration, undocumented calls to external domains.
- **Compatible license** — verify that the skill's license is compatible with your project and any NDA clauses. CC-BY-SA (like Trail of Bits) imposes share-alike on derivatives; GPL-2.0 (like WordPress agent-skills) has known copyleft implications; MIT (Vercel Labs, Superpowers) is generally the most permissive.
- **Repo health** — check last commit date, number of stars, ratio of open/closed issues, presence of security advisories. A skill abandoned for a year is a risk for any codebase that uses it actively.
- **Permissions it requests** — some skills request access to powerful tools (Bash unrestricted, WebFetch on external domains, global writing). Compare them with your `settings.json` policy (see [section 9](#security-and-permission-management)) and reject those that ask for more than they justify.
- **Sandbox in dev** — test new skills on a throwaway project before installing them globally in `~/.claude/skills/`. If you need an additional layer of defense, a `PreToolUse` hook (see [section 13](#hooks-automating-claude-codes-lifecycle)) can block commands the skill tries to execute outside the allowed perimeter.

The mental schema is the same you would apply to any dependency: you don't include code you haven't read, you don't trust an author just because they have many stars, and you don't enable more than what's needed. The difference is that here the "code" is an instruction in natural language that Claude will read and execute — and natural language is ambiguous by definition. Double attention.

---


---

> ← [9. Security and permissions](09-security.md) | [Index](README.md) | [11. MCP](11-mcp.md) →
