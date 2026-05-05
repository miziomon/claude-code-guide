# Practical Guide to Claude Code CLI

> **Version 4.30 — May 2026** — verified on Claude Code v2.1.123
> Licensed under [Creative Commons BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

> ← [7. Persistent memory](07-memory.md) | [Index](README.md) | [9. Security, permissions, and guardrails](09-security.md) →

---

## 8. Context management

The context window is Claude Code's most precious resource, and the one most users handle worst. Understanding what fills it, how it degrades when it's too full, and how to intervene before it becomes a problem, is the difference between a casual use and a professional one of the CLI.

### 8.1 What context is and why it matters

The **context** is the total amount of information the model sees in a single turn: Claude Code's system prompt, loaded `CLAUDE.md` files, conversation history, output of executed tools, contents of read files, definitions of active skills and MCP tools. All this is measured in **tokens** — units of text (one token corresponds roughly to 4 characters in English, slightly fewer in Italian).

Claude models in April 2026 have two window sizes:

- **200,000 tokens** — the default. Sufficient for the vast majority of tasks.
- **1,000,000 tokens** — available on specific models (see 8.7), designed for analysis of large codebases and very wide contexts.

Having a large window doesn't mean having constant performance over the entire length. Anthropic has explicitly documented a phenomenon called **context rot**: as the number of tokens grows, the model's accuracy and recall degrade. It's not a bug: it's an architectural consequence of the attention-based structure of transformers (peer relationships between tokens that explode quadratically with size). In practice, a model with context at 90% occupation **doesn't work like a fresh one at 10%**, even if the window is the same.

Concretely, this means context should be treated as a **scarce resource, not a dump**. Good practice isn't "load everything and see what happens": it's choosing carefully what enters, what leaves, and when to reset and restart.

### 8.2 What weighs in the context

A Claude Code session, before you even write the first prompt, has already loaded a certain number of tokens. Knowing what the categories are helps you understand where to intervene.

| Category | Indicative weight | When it loads |
|---|---|---|
| **System prompt** | ~4,200 tokens | Always, at startup |
| **Environment info** (cwd, OS, shell, git status) | ~280 tokens | Always, at startup |
| **MCP tools (deferred)** | ~120 tokens (only names, schemas on-demand) | Always, at startup |
| **MEMORY.md (Auto Memory index)** | up to ~6,500 tokens (max 200 lines / 25 KB) | Always, if Auto Memory active |
| **CLAUDE.md (hierarchical)** | depends on length | Always, **in full**, every session |
| **Skill descriptions** | ~1% of the window (~2,000 tokens, default 8 KB chars) | Always for every active skill not disabled |
| **Tool results** (read files, Bash output, etc.) | very variable, often the biggest item | Dynamically, during work |
| **Conversation** (your prompts + responses) | variable | Dynamically |

> Values are indicative and derived from the [Explore the context window](https://code.claude.com/docs/en/context-window) page of the Claude Code documentation. They vary by session, model, configuration. To measure your real ones, use `/context`.

Three points worth fixing:

**1. `CLAUDE.md` files are loaded in full every session.** There's no caching or indexing: all content enters the context. Anthropic recommends keeping each `CLAUDE.md` under **200 lines**: beyond that, both because the model has more difficulty following all the instructions, and because you consume tokens uselessly. If you find yourself with a 400-line `CLAUDE.md`, you're probably putting things in there that should be in skills, project documentation, or `CLAUDE.local.md`.

**2. Installed skills occupy context even if not triggered.** It's the most underestimated point. Every active skill contributes to the context with its own **description** (necessary to allow the model to decide whether to invoke it). The full skill content is loaded only when triggered, but the description is always there. A user who has 50 skills installed "just in case" starts with a significantly reduced context budget compared to someone who has 10 well-chosen ones. **Install only the skills you actually use**: for the others, evaluate `disable-model-invocation: true` in the frontmatter (also removes the description from the context).

**3. Tool results are the category that explodes.** Reading 30 PHP files to look for a pattern can easily mean 50,000+ tokens of tool results. An `npm run build` with verbose output, even more. This is where most of the saturation plays out, and this is where subagents (see 8.6) make the biggest difference.

### 8.3 Signals of a saturated context

When the context approaches the limit, the model starts behaving in recognizable ways:

- **"Forgets" things said earlier** — responses that ignore a decision made two turns ago, or repeat explanations already given
- **Slower responses** — more tokens to process = more response time
- **"Stupid" errors** it didn't make before — uses the wrong convention, refers to a non-existent file name, proposes code inconsistent with the rest of the project
- **Warnings in the status line** if you've configured it with a context indicator

> **What NOT to do when you see these signals.** Continuing to "explain again" is the instinctive reaction, and it's exactly the wrong one: every new explanation further inflates the context. Likewise, repeating the prompt more detailed doesn't help — it makes things worse. The remedy is structural, not linguistic: use `/context`, read what weighs, act with `/compact` or `/clear`. See 8.4 and 8.5.

### 8.4 The `/context` command: reading and acting

`/context` is the most direct way to **see how much context you're consuming** before the problem becomes visible from the model's behavior. Launched at any time, it shows:

- the **percentage of context used** out of the total available
- the **breakdown by category**: system prompt, CLAUDE.md, skills, conversation, read files, tool output

Reading example:

```
/context

Context usage: 42% (84,000 / 200,000 tokens)

  System prompt:           ~4,200 tokens
  Environment + MCP:         ~400 tokens
  CLAUDE.md (3 levels):    ~2,800 tokens
  Skills (8 active):       ~3,100 tokens
  MEMORY.md:                 ~680 tokens
  Conversation:           ~18,000 tokens
  Tool results:           ~54,800 tokens
```

#### Strategic reading by category

The useful part is understanding **where the weight lies**, because it determines the right cure:

- **Tool results bloated (>50% of total)** → you've read many files or executed verbose commands. Solution: `/compact` summarizes while keeping decisions and key files, throws away the noise.
- **Conversation bloated** → you've mixed too many tasks in the same session, or you've dragged along old clarifications no longer relevant. Solution: consider `/clear` if you're at a task change.
- **System + CLAUDE.md + Skills high** → the session "tare" is too heavy. It's not solved with `/compact` or `/clear`: it's structural. You need to review how many skills you have active, how long your `CLAUDE.md` files are, if Auto Memory has accumulated too much in `MEMORY.md`.

#### Indicative thresholds

> **Note on the numbers that follow.** The percentages in this table are empirical: they reflect common practice and the author's experience in real sessions with medium-sized PHP/JS codebases. Anthropic doesn't publish official thresholds beyond the genericity of "context rot": take these values as a starting point, not as a prescriptive guideline. If you work on monorepos of 1M+ tokens, on synthetic tasks, or with a very particular pipeline, your useful thresholds will be different.

- **Below 50%** — relaxed, work normally.
- **50-75%** — start evaluating: close the current task and then `/compact` before opening a new one.
- **Above 75%** — it's time to intervene: `/compact` if you want to keep the thread, `/clear` if you're completely changing topic. Above 85% also consider switching to a 1M window model (see 8.7) if the task justifies it.

#### When to launch it

`/context` is particularly useful in three moments:

- **Before a heavy task** — if you're about to ask for a Plan Mode on a large area or an audit of many files, knowing you're starting at 70% saves you from discovering halfway through that the model starts forgetting.
- **When you sense the model "slowing down"** — before concluding that "Claude is stupid today", check the context. Often it's just saturated.
- **In long, routine sessions** — even without signals, launching it every 30-40 minutes gives you proactive instead of reactive control.

### 8.5 Compression: `/compact` and `/clear`

These are the two main compression tools. Important difference:

- **`/compact`** compresses the conversation into a summary, keeping decisions and key context. **You continue to work with the thread of discourse**, but with much fewer tokens. Ideal mid-session when you've closed a phase and are opening another related one.

  Optional syntax to give a focus to the summary:

  ```
  /compact keeping the architectural decisions
           of the auth refactor and the pattern
           adopted for rate limiting
  ```

  Without instructions, Claude decides what's important. With instructions, you tell it what to focus on and what it can throw away without regrets.

- **`/clear`** completely resets the context. **Fresh session**, but `CLAUDE.md`, skills, system prompt, and Auto Memory remain (they're system, not part of the conversation). Use when you change task completely and don't need anything from the previous one.

Example of typical flow:

```
[Morning start]
> Refactor the auth module to use JWT
[2 hours of work, /context says 78%]

/compact keeping decision of JWT with refresh token rotation

[Opening new phase]
> Now add unit tests on the new auth module

[Afternoon, completely different task]
/clear

> Update the API documentation to reflect the endpoint change
```

### 8.6 Subagents: the structural strategy

`/compact` and `/clear` are **reactive remedies**: you act when the context is already full. Subagents are the **preventive** tool: they work so the main agent never bloats for things it doesn't need.

Anthropic's documentation states it explicitly: subagents allow you to *"preserve context by keeping exploration and implementation outside the main conversation"*. The mechanism, already seen in detail in [section 12](#subagents-orchestrating-specialized-work), is simple:

- The main agent **delegates** a specific task to a subagent (built-in like `Explore`, or custom).
- The subagent runs in its **separate context window**, with dedicated tools and instructions.
- When done, it returns to the main agent **only a summary** of the result — not the 30 read files, not the 80 KB build output, only the distillate.

Three cases where the pattern pays off the most:

- **Pattern search across many files**. *"Find all PHP functions that don't have nonce verification in the plugin"* — done by the main agent means reading ~50 files and keeping them in context forever. Delegated to a subagent it means receiving a summary of 7 vulnerable functions with line and file, and that's it.
- **Massive audits**. Automatic code review on an entire plugin: three parallel subagents (security, performance, style) produce three independent summaries, the main agent aggregates them without seeing the detail of the individual files read.
- **Exploration of an unknown area**. Before starting a refactor, *"understand how the notifications module is structured"* given to an `Explore` subagent returns an architectural summary — 1,500 tokens — instead of 60,000 tokens of code files in the main context.

A good heuristic: **if you find you've read 30 files just to produce 200 tokens of output, it was a subagent**.

### 8.7 Models with 1M token window: when to switch

For most tasks, 200K tokens are more than sufficient. There are however scenarios where the jump to 1M qualitatively changes what can be done. The important thing: in API plans and enabled Pro/Max plans, **it doesn't cost more per token** — pricing is identical between 200K and 1M, you only pay for the tokens you use.

#### Activation syntax

Three officially documented ways:

```bash
# During a session
/model sonnet[1m]
/model opus[1m]
/model claude-opus-4-7[1m]

# At launch from terminal
claude --model "sonnet[1m]"
claude --model "opus[1m]"

# Environment variable (default for every new session)
ANTHROPIC_DEFAULT_SONNET_MODEL=claude-sonnet-4-6[1m]
ANTHROPIC_DEFAULT_OPUS_MODEL=claude-opus-4-7[1m]
```

The `[1m]` suffix is the official syntax and appears in the `/model` picker when the model supports 1M.

#### Models with native 1M (April 2026)

| Model | Window | Notes |
|---|---|---|
| `claude-opus-4-7` | 200K / 1M | Stable, default |
| `claude-opus-4-6` | 200K / 1M | Stable |
| `claude-sonnet-4-6` | 200K / 1M | Stable |

> **Current state (verified April 30, 2026 on the [official docs](https://platform.claude.com/docs/en/build-with-claude/context-windows))**: the 1M window is available on Opus 4.7, Opus 4.6, and Sonnet 4.6. Sonnet 4.5 has 200K context, and Sonnet 4 is explicitly *deprecated*. The 1M beta that was available on Sonnet 4 / 4.5 has been retired: those with pipelines requiring it must migrate to Sonnet 4.6 or Opus 4.6/4.7. For the always-updated state, refer to the [official models table](https://platform.claude.com/docs/en/about-claude/models/overview).

#### When it makes sense to switch to 1M

Concrete scenarios:

- **Audit of a plugin with over 80 PHP files** where you need to keep much of the code together to reason about cross-cutting patterns (e.g., all the points where the database is accessed, mapped in a single pass).
- **Structured comparison between two large branches** before a complex merge.
- **Cross-module migration** where decisions in one area depend on how 5-6 other areas of the codebase work.
- **Extensive legacy documentation** you want to keep complete in context to generate a new guide coherent with everything.

#### When it's NOT needed

- **Tasks focused on a few files** (3-10): 200K is plenty.
- **Punctual debugging** or fix of an isolated bug.
- **Incremental refactoring** where you work on one function at a time.
- **Exploratory sessions** where you change direction often: better a `/clear` from time to time than a monstrous window to manage.

Even with 1M, the [context rot](#what-context-is-and-why-it-matters) remains. It's not an excuse to "throw everything in there": it's a tool for scenarios where breadth is truly needed, to be used with the same discipline as 200K.

### 8.8 Practical rule and mindset

> If you find you've done three different things in the same session, you probably should have used `/clear` twice.

Focused sessions produce better output and consume fewer tokens. The principle underneath everything: context is **a scarce resource, not a dump**. Everything that enters must earn its place.

#### Context management tools: where they are in the guide

Context management cuts across the entire guide, not just here. Here's where to dig deeper:

- **Right model for the task** — [section 5](#plan-mode-think-before-you-write) (`opusplan`, model selection)
- **Well-sized `CLAUDE.md`** — [section 7](#persistent-memory-claude.md-and-auto-memory) (under 200 lines)
- **Auto Memory not bloated** — [section 7](#persistent-memory-claude.md-and-auto-memory) (`MEMORY.md` as index, topic files on-demand)
- **Skills only those you need** — [section 10](#skills-the-extension-mechanism)
- **Subagent as structural strategy** — [section 12](#subagents-orchestrating-specialized-work)
- **Hooks to reduce noise in session** — [section 13](#hooks-automating-claude-codes-lifecycle) (e.g., filters on tool output)

### 8.9 Choosing the right architecture: decision table

Claude Code's five extension mechanisms (`CLAUDE.md`, Auto Memory, Skill, Subagent, Hook) overlap in use cases and easily generate the question *"which one do I use for what?"*. Design decisions intertwine: does a code convention go in `CLAUDE.md` or in a skill? Does an automation go in a hook or in a custom slash command? Does an exploration of an unknown area get done by the main agent or delegated to a subagent? The following sections are the unified map.

#### 8.9.1 CLAUDE.md

| Key | Value |
|---|---|
| **Use case** | Conventions, stack, hard rules that apply to every session of a project (language, framework, folder structure, build commands, anti-patterns to avoid). |
| **Context cost** | High — loaded in full every session. Keep the file < 200 lines. |
| **When to use it** | You have stable rules the model must always know before starting to work. |
| **Limit** | Doesn't adapt to cross-project preferences nor to dynamic learnings (for those, Auto Memory). |

**Extended description.** `CLAUDE.md` is the first thing Claude reads when opening a session on a project. It contains the rules that apply *always*: programming language and version, framework in use, expected folder structure, build and test commands, anti-patterns that must never enter the code. Every line is an operational constraint that Claude must respect on any task, at any time.

**When to use it.** The practical test is simple: should this rule still apply the next time I open Claude Code on this project? If yes, it goes in `CLAUDE.md`. If it's only valid for the current session or a single task, it goes in chat or in Auto Memory.

**Limit.** It doesn't scale to cross-project preferences — Auto Memory handles those. It's not suited for discursive documentation: it's for concise operational rules, not tutorials. And it doesn't dynamically adapt to what Claude learns over time: it's static by design.

#### 8.9.2 Auto Memory

| Key | Value |
|---|---|
| **Use case** | Learnings that cross sessions and projects: user preferences, corrections to remember, stable architectural decisions. |
| **Context cost** | Low — only `MEMORY.md` (index, max ~6.5K tokens) is loaded; topic files are on-demand. |
| **When to use it** | You want Claude to learn over time from how you work, without repeating the same instructions at every new session. |
| **Limit** | Not a documentation repository: only concise rules/preferences. If it grows beyond 200 lines it should be pruned. |

**Extended description.** Auto memory is a persistent on-disk memory system organized in two layers: `MEMORY.md` as an index (~6.5K tokens, always loaded) and on-demand topic files (loaded only when relevant). Claude writes to it autonomously when it learns something worth remembering: your way of working, a stylistic preference, a correction you've had to give multiple times.

**When to use it.** When you notice having to correct Claude on the same thing every three sessions — that's the signal the learning should be persisted. Unlike `CLAUDE.md` (which stores *project* rules), Auto Memory captures *user* rules that are valid regardless of which project is open.

**Limit.** It's not a wiki or a knowledge base: if it exceeds 200 entries in the index, the benefit reverses (too much context loaded, index hard to maintain). Periodically pruning stale entries is part of the maintenance.

#### 8.9.3 Skill

| Key | Value |
|---|---|
| **Use case** | Codified and reusable playbook (procedure, analysis framework, writing pattern) invokable from any session. |
| **Context cost** | Medium — ~1% window for description (always present), full content only if invoked. |
| **When to use it** | A recurring procedure you want to standardize or distribute (`/security-review`, `/simplify`, corporate skills). |
| **Limit** | The sum of descriptions of many installed skills erodes context: 10 targeted skills > 50 "just in case". |

**Extended description.** A skill is a Markdown file that the system injects into context when invoked via slash command (`/skill-name`). It can contain detailed instructions, checklists, references to patterns or frameworks — in practice a specialized "operational manual" that Claude executes on request. Skills can orchestrate subagents, use tools, and produce structured output.

**When to use it.** You have a procedure you repeat often and want to execute consistently — or you want to share it with the team. The writing cost is one-time; the consistency benefit accumulates with every invocation. Typical cases: security reviews, performance analyses, refactoring to an agreed style.

**Limit.** Every skill has its description loaded *always* in context (~1% of the window), regardless of whether it gets used in that session. With 50 installed skills, descriptions alone occupy ~50% of the window. Practical rule: only install skills you use at least once a week.

#### 8.9.4 Subagent

| Key | Value |
|---|---|
| **Use case** | Read-heavy tasks that would bloat the main context: audits, codebase exploration, pattern search across many files, comparative analyses. |
| **Context cost** | Almost zero on main — runs in a separate window, returns only the summary. The real structural saving of tokens. |
| **When to use it** | You're about to read 20+ files to produce a synthetic output, or you want to parallelize 3 independent audits. |
| **Limit** | Higher latency (it's another call), no shared state between subagent and main, the summary may lose details. |

**Extended description.** A subagent is a separate Claude instance operating in an independent context window. The main agent spawns it with a precise task; the subagent executes (reads files, navigates the codebase, builds an analysis), then returns *only the synthetic result*. The main agent never sees any of the files the subagent read internally — that's the point: the cost of massive reading doesn't pollute the main context.

**When to use it.** Every time you're about to load more than 10–20 files into the main context to produce a few lines of output. Particularly effective in parallel: three subagents exploring three areas of the codebase simultaneously complete faster and with fewer total tokens than a single main agent exploring them sequentially.

**Limit.** The subagent shares no state with the main: if the main agent has already analyzed something or has in-progress reasoning, the subagent won't see it. And the returned summary may lose nuances that were in the original files — if the decision requires the details, don't delegate.

#### 8.9.5 Hook

| Key | Value |
|---|---|
| **Use case** | Deterministic automation on lifecycle events (`PreToolUse`, `PostToolUse`, `UserPromptSubmit`, etc.): formatting, validation, log, security blocks. |
| **Context cost** | Zero or negative — often a hook *reduces* context by filtering noisy output before it reaches the model. |
| **When to use it** | You want something to happen **always** in response to an event, regardless of the model's decision. |
| **Limit** | It's deterministic, not semantic: it doesn't "understand", it executes. It doesn't replace a subagent or skill when model judgment is needed. |

**Extended description.** A hook is a shell command (or script) that the system executes automatically when a Claude Code lifecycle event occurs: before Claude uses a tool, after it has used it, when the user sends a message, when the session ends. Unlike a skill (which Claude *chooses* to invoke) or a subagent (which Claude *decides* to spawn), a hook fires *always* — Claude has no say in it.

**When to use it.** When the rule is absolute: it must happen always, or never. `prettier` after every `Edit`, lint check before every `Bash`, blocking dangerous command patterns — these are all hooks. Certainty of execution is the key property: no model ever "forgets" a hook.

**Limit.** A hook doesn't understand context: it runs its script without knowing *why* Claude is using that tool. It's not suited for semantic decisions ("format only if it's a production file") — those require Claude's judgment, so a skill or an instruction in `CLAUDE.md`.

**How to choose the right mechanism.** The point isn't choosing "the best in absolute" but the one that sits in the right place of the chain. Three practical principles:

- **`CLAUDE.md` is the base**, not an aspiration: if the rule doesn't apply to every session of the project, it doesn't go there.
- **Skill and subagent** work together: often a skill orchestrates a subagent (e.g., `/security-review` delegates to an `Explore` subagent for the massive reading, then composes the report).
- **Hook is lateral**: it doesn't replace any of the other four, it *integrates* them at zero cost when automatic and predictable action is needed.

When you find yourself repeating the same instruction to three sessions in a row, you have a candidate for `CLAUDE.md` or Auto Memory. When you find yourself reading dozens of files to produce a summary, you have a candidate for a subagent. When you find yourself wanting to guarantee that something *happens regardless*, you have a candidate for a hook.

### 8.10 Prompt cache and consumption observability

Claude Code automatically applies Anthropic's **prompt cache** to the system prompt and the tool definitions of active MCP servers: these blocks — identical from turn to turn — are written to cache on the first turn and read back at reduced cost in subsequent turns. Understanding how it works and how to monitor it lets you work informed instead of paying tokens unknowingly.

#### How the prompt cache works

**Prompt cache** is an Anthropic mechanism that stores the stable prefixes of a prompt — the system prompt, MCP tool definitions, initial few-shot examples — so they can be reused in subsequent turns without reprocessing them. In practice, the first time Claude processes a long, stable block of text it writes it to cache; on subsequent turns that block is read from cache instead of being retransmitted and computed from scratch.

**Why it matters economically:** reading from cache costs **10% of the normal input token price** — a 90% saving on the fixed prefix. It also reduces latency: already-processed tokens skip the model's forward pass. In a long session with a sizeable system prompt and several active MCP servers, the difference is noticeable both in cost and response speed.

The cache operates on **stable prefixes** of the prompt, in hierarchical order: first the MCP tools, then the system prompt, then the conversation messages. For the cache to activate on a block, that block must be identical to the previous turn — even a single changed character invalidates the cache from that point on — and must exceed a **minimum token threshold**:

| Model | Minimum tokens |
|---|---|
| Opus 4.7 / 4.6 | 4,096 tokens |
| Sonnet 4.6 | 2,048 tokens |
| Haiku 4.5 | 4,096 tokens |

Claude Code's system prompt (~4,200 tokens) exceeds the threshold on all models and is always a cache candidate. CLAUDE.md, skill descriptions, and MEMORY.md are included only if the prefix preceding them is already stable and the block reaches the threshold.

**Cache TTL.** Default is 5 minutes: if you don't send another turn within 5 minutes, the cache expires and on the next turn the block is rewritten. Actions that invalidate the prefix — adding or removing an MCP server, modifying CLAUDE.md mid-session, compressing with `/compact` — have the same effect.

**What isn't cached.** Files that Claude reads with `Read` enter the `messages` field at a variable position and generally don't benefit from caching. Tool results remain the live cost hardest to amortize.

#### Monitoring with `/cost` and `/usage`

`/cost` (alias `/usage` or `/stats`) shows the current session's consumption. Example output:

```
/cost

Current session:
  Input tokens:                 12,450
  Cache write (5 min):          82,000
  Cache read:                  248,000
  Output tokens:                 3,820

Estimated cost:    $0.42
```

The useful reading is the ratio between `cache_write` and `cache_read`:

- **Many `cache_read`, few `cache_write`** → great: the fixed "tare" is amortized over many turns.
- **`cache_write` grows every turn** → the prefix keeps invalidating: check if an MCP changes its descriptions, if CLAUDE.md is modified mid-session, or if a compaction just happened.
- **`cache_read` at zero** → cache never activated: session too short or blocks below the minimum threshold.

Run it every 15-20 turns in long sessions. If you see a spike in `input_tokens` on a specific turn, you've found where something very heavy was read — a candidate for delegation to a subagent (see [§8.6](#subagents-the-structural-strategy)).

#### Relevant env vars

```bash
# Reduces the extended thinking budget: if you're not doing complex tasks,
# lowering it often halves output token cost
MAX_THINKING_TOKENS=8000

# Excludes dynamic sections of the system prompt to stabilize the cache prefix
# — useful if you have MCP servers that change descriptions every turn
claude --exclude-dynamic-system-prompt-sections
```

> For disabling Auto Memory (another item that enters the prefix) see [section 7](#persistent-memory-claudemd-and-auto-memory). For monitoring MCP server weight and disabling unused servers, see [section 11.7](#managing-the-cost-of-mcp-servers-on-context).

---


---

> ← [7. Persistent memory](07-memory.md) | [Index](README.md) | [9. Security, permissions, and guardrails](09-security.md) →
