# Practical Guide to Claude Code CLI

> **Version 4.23 — May 2026** — verified on Claude Code v2.1.123
> Licensed under [Creative Commons BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

> ← [5. Plan Mode](05-plan-mode.md) | [Index](README.md) | [7. Persistent memory](07-memory.md) →

---

## 6. Prompt engineering: writing effective prompts

You've learned the commands, the shortcuts, and Plan Mode. You know *what* you can ask of Claude Code. One piece is missing: learning *how* to ask. This is prompt engineering — the discipline that separates those who get what they want on the first try from those who retry three times and complain about the results. It's also the technical heart of the *vibe coding* mentioned in [Preface](#who-its-for): writing precise instructions so the model generates code aligned with your intentions, instead of writing the code by hand line by line.

There's a word that circulates among developers to describe the "naïve" way of working with AI: **Hope Coding**. You launch a generic request and *hope* the model guesses what you wanted. It works occasionally, often fails, and in worst cases produces code that looks right but isn't. The opposite path is to treat AI as an **extremely literal senior collaborator**: you tell it exactly what you need, in what context, with what constraints, in what format you want the answer. There's no magic, no "secret prompt": there's only a method.

A note of honesty before getting into the matter: prompt engineering in 2026 isn't what it was in 2023. The most "magical" techniques (act-as-an-expert, incantatory formulas, dramatic spellings) have deflated as models have improved. The discussion has shifted to two axes that still hold today: the **structure** of the prompt (context, task, constraints, output) and the **context** you load before asking. The real frontier of 2026 is *context engineering*: not *how* you ask, but *what information you make available to the model* before asking — a topic that in CLI translates into `CLAUDE.md`, Auto Memory, files read by subagents, and which we explore in chapters 7 and 8.

> **Evolution disclaimer.** The techniques that follow reflect the state of the art at April 2026 (Claude 4.x and equivalent models). Prompt engineering changes fast: for the up-to-date reference always consult the [official Anthropic docs](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices) and the [Prompting Guide](https://www.promptingguide.ai/).

### 6.1 What prompt engineering is and why it matters in CLI

Prompt engineering is the art (and partly the discipline) of formulating requests that produce predictable and useful output from an LLM. Three practical observations to frame it in the context of Claude Code:

- **It's not writing long descriptions.** The more verbose a prompt is, the more the model risks losing the point. Information density matters more than length.
- **It's not "making the prompt look intelligent".** A brilliant-to-read but vague prompt produces mediocre output. A prompt that looks like a public servant's checklist, but is specific, produces excellent output.
- **In CLI the prompt is an action, not just text.** In web chat, the prompt produces only text as a response; in Claude Code the prompt orchestrates **tools**: reads files, runs commands, modifies code. An ambiguous formulation doesn't just translate into a wrong answer: it translates into **wrong actions** on your filesystem. The margin for error is higher.

### 6.2 Anatomy of a well-made prompt

A well-made prompt contains four fundamental ingredients, plus an optional one we discuss right after:

1. **Context** — the background: what the project is, who the audience is (if relevant), what the technology stack is, what domain constraints apply.
2. **Task** — the requested action. Golden rule: **one task at a time**. Mixing different requests in a single prompt produces hybrid and confused output.
3. **Constraints** — what the model must do and must not do: length, tone, code standards, prohibitions ("don't use jQuery", "no external libraries", "max 100 lines").
4. **Output format** — how you want to receive the answer: Markdown table, JSON with a specific schema, "code only without explanations", bullet list, etc.
5. **(Optional) Role** — *"act as a senior backend engineer"*. It's the fifth ingredient, deliberately listed last: in 2026 its weight is significantly reduced. I dig into why right away.

Before/after example, to fix the idea. **Vague** version:

```
Write me a function to validate an email
```

**Structured** version:

```
Context: Node.js + TypeScript project, server-side validation
of user registration form. Compatibility constraint with
Node 22 LTS, no external dependencies.

Task: implement a function that validates an email string.

Constraints:
- Pure TypeScript, no libraries
- Returns a discriminated Result type { ok: true, email: string } |
  { ok: false, reason: 'invalid_format' | 'invalid_domain' | 'too_long' }
- Maximum accepted length: 254 characters (RFC 5321)
- Basic format validation + TLD presence check
- Vitest unit tests in a second code block

Output format: two distinct TypeScript code blocks
(implementation + tests), no explanation between them.
```

The two requests are the same task, but they produce output of completely different quality. Not because the model is more "intelligent" in the second case: because it has fewer degrees of freedom to make mistakes on.

### 6.3 From roles to structural constraints (the 2026 revolution)

For years the first piece of advice on prompts was: **start with the role**. *"Act as a senior security engineer"*, *"You are a cloud architecture expert"*, and so on. It worked: older models were sensitive to the role "frame" and modulated the style and depth of the response.

On 2026 frontier models this lever has shrunk significantly. The [Anthropic documentation for Claude 4.x](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices) indicates as the three primary levers of a good prompt: **explicit instructions**, **adequate context**, **curated examples** when needed. The role is no longer among the main levers. The technical reason is that modern models autonomously deduce the "competence" to call upon when context, task, and constraints are specific. Saying *"act as a senior PHP engineer"* adds little if in the context you're already saying *"WordPress plugin on PHP 8.1, PSR-4 namespace, code for production"*.

That said, **the role isn't dead**. It remains useful in specific scenarios. Here's when it's still worth using:

| Situation | Does the role help? |
|---|---|
| Well-specified technical task on frontier model (Claude 4, equivalent GPTs) | No — redundant with context+task |
| Strong narrative voice (storytelling, copy with distinctive tone) | Yes — guides style |
| Domains with ambiguous regulatory references (legal, fiscal, healthcare) | Yes — orients the interpretive frame |
| Smaller or free models | Yes — they're more sensitive to roles |
| Persistent system prompt (e.g., Claude Projects, custom subagents) | Yes — defines stable session identity |

For daily technical tasks on frontier models: focus on **structural constraints**, not on the role.

#### XML-like delimiters: the modern pattern

On 2026 models (Claude in particular), the use of **XML-like delimiters** emerges as the preferred pattern for visually separating prompt sections. It reduces ambiguity, especially in long conversations where the model has to recognize which part of the message is instruction and which is, for example, code to analyze.

```
<context>
WordPress project, custom plugin, PHP 8.1.
Base theme: Astra. Block editor: Gutenberg.
</context>

<task>
Generate custom CSS for the theme's primary buttons (class
.wp-block-button__link) with a modern hover effect: slight scale,
fluid transition, subtle shadow.
</task>

<constraints>
- No !important
- Responsive (mobile-first)
- Use CSS variables for colors
- Comments in English
</constraints>

<output_format>
CSS code only, ready for Appearance → Customize → Additional CSS.
No textual explanation.
</output_format>
```

The tags have no semantic meaning to the model (it's not real XML), but they act as **clear separators**. The model recognizes them as delimiters and treats each section as a coherent block. For complex prompts, it's one of the most reliable patterns.

### 6.4 The fundamental techniques

There's no universal technique. Each technique responds to a certain type of problem. The five that follow cover most practical use cases for those working with code.

#### 6.4.1 Chain of Thought (CoT) — step-by-step reasoning

The idea: explicitly ask the model to **reason in phases before answering**, instead of producing the conclusion directly. The magic formulas are simple: *"think step by step"*, *"reason in steps before proposing the solution"*, *"first analyze, then propose"*.

It works because it forces the explication of logical steps. The model doesn't "jump to the answer" on intuition, but breaks the problem down into sub-problems and addresses them one at a time.

**Commented example**: diagnosing site slowness.

```
A WordPress + WooCommerce site has become slow in recent
weeks (TTFB > 3s on product pages).

Before proposing solutions, reason in phases:

1. List the most probable causes of TTFB worsening
   on WP/WooCommerce in production.
2. For each cause, indicate how to verify it (free tool,
   SQL query, log to check).
3. Sort the causes by probability + ease of verification.
4. ONLY AFTER completing the three steps above, propose
   an intervention plan in 5 ordered steps.

Don't jump to generic advice like "use a caching plugin".
I want the diagnostic analysis first.
```

What makes this prompt work: the last line (*"don't jump to generic advice"*) blocks the most common response pattern. The 4-phase numbering forces the model not to take shortcuts.

> On Claude 4.x there's also **extended thinking** as a product capability: the model "thinks" before answering, showing the reasoning in a separate block. On Claude Code, activatable with `Alt+T` (see chapter 4.7). It's the "native" version of CoT, to be preferred when available.

::: note

**Worth it when** — diagnosis, debugging, architectural decisions, any multi-phase task where the risk is the "pre-packaged answer" that skips intermediate steps. On Claude 4.x it's almost always better to activate native **extended thinking** (`Alt+T`) instead of reconstructing CoT in words.

**It's filler when** — well-defined linear tasks ("rename this function", "write a test for X"). On 2026 models, step-by-step reasoning is already implicit: adding *"think step by step"* to a simple request doubles the tokens without improving the output.

:::

#### 6.4.2 Few-Shot Prompting — teaching by examples

The idea: instead of describing how you want the output, **show it with two or more examples**. The model recognizes the pattern, applies it to the new input.

It's the most effective technique for **voice consistency** (maintaining a uniform style across recurring content) and for **reproducing structured formats** that are hard to describe in words.

**Commented example**: generating FAQ in colloquial style.

```
I have to write FAQs for a site of products for early infancy.
Tone: confidential, never patronizing, some emojis but
sparingly. Synthetic answer, max 3 lines.

I'll give you two examples of the tone I want:

❓ When can I start weaning?
   Italian pediatric guidelines talk about 6 completed months,
   but every baby has their own timing 🌱. Always talk to your
   pediatrician before starting.

❓ Can I wash baby bottles in the dishwasher?
   Yes, if the temperature exceeds 60 °C. But remember to
   sterilize them separately once a week — the dishwasher
   isn't enough to eliminate everything.

Now write me 5 FAQs in the same tone on these topics:
1. Pacifier sterilization
2. Food allergies in the first 12 months
3. When to switch from breast milk to follow-on milk
4. Safe sleeping position
5. Mandatory vaccinations 2026
```

What makes this prompt work: the two examples are **complete and canonical**. They show format (emoji + question + 2-3 lines), tone (confidential but responsible), and a specific implicit rule (always defer to the pediatrician when in doubt).

::: note

**Worth it when** — voice consistency, microcopy, product cards, FAQs, classifications with your labels, structured formats hard to describe in words. 2-3 well-chosen canonical examples are enough.

**It's filler when** — technical tasks where the spec is crystal clear in words. Inserting 2 examples of "how to write a JUnit test" wastes context: a sentence on the tech stack is enough. **Anti-pattern**: 8-10 examples "for safety" — the model over-specializes and loses generality.

:::

#### 6.4.3 Panel of Experts (Round table)

This is the technique that, in my opinion, is most worth learning in depth. **It doesn't only serve to "get an answer"**: it serves to *learn*, *explore*, *put your own ideas into question*. It's particularly valuable when you have to make a decision and don't want to settle for a single answer, but want to *hear different perspectives* — especially those that might not come to your mind.

**The idea**: you simulate a **discussion among virtual specialists**, each with their own viewpoint. You ask the model to interpret each one with their own perspective and to explicitly point out conflicts. The value isn't in the final synthesis, but in the **explication of trade-offs** that each decision implies.

The most powerful use cases:

- **Choosing a stack** for a new project (e.g. *"PHP+MySQL or Node+PostgreSQL?"* depends on who's looking at it)
- **Evaluating an architecture** before starting to code it
- **Stress-testing an idea** that seems good — you want to know where it breaks before discovering it in production
- **Asking for an opinion** before a decision with consequences (big refactor, DB migration, choice of library that will enter many files)
- **Understanding a topic** you know little about, listening to different voices instead of a single, potentially partial answer

**Prompt-template for software development** (canonical, reusable):

```
You're in a session dedicated exclusively to analyzing,
suggesting, and possibly creating code snippets.
Behave as if we're having a debate at a
round table with the following virtual experts:

– Full-stack computer engineer
– Programmer expert in PHP
– Programmer expert in JavaScript, Node and React
– Database Administrator and Data Engineer
– UX Designer
– Project Manager

For every question I want a response from each expert with
their own opinion. If there are discordant observations,
point them out to me. Every code proposal must be explained
and commented step by step.
```

What makes this prompt work:

- **Variety of angles**: full-stack sees the whole, PHP/JS see the technical stack, DBA sees persistence, UX sees the end user, PM sees timing and priorities. Covering angles you would individually miss is the point.
- **Explicit request for conflicts** (*"if there are discordant observations, point them out to me"*). Without this line the model tends to synthesize toward fictitious consensus. With the line, dissent becomes explicit and is the most useful part.
- **Step-by-step explanation of code** requires that every proposal be argued, not just presented. It helps unmask proposals that "look right" but aren't.

**Applied example**: you have a small internal application (task tracker for an 8-person team). You have to decide whether to write it as a custom PHP+MySQL app, or as a Next.js + PostgreSQL app, or use a no-code tool. Launched the prompt template above and then:

```
Question: for an internal task tracker (team of 8 people, ~500
tasks/month, dashboard with filters and a REST API for integration
with Slack), evaluate three options:
1. Custom PHP+MySQL app
2. Custom Next.js + PostgreSQL app
3. No-code tool (Airtable, Notion, ClickUp)

I want pros/cons from each of you, and a final recommendation
with the main trade-offs explicitly stated.
```

What you'll typically get: the full-stack will look at the "total 3-year maintenance cost", PHP/JS will compare on development experience, the DBA will raise the migrations point, UX will say no-code already has an excellent UI you'll never recreate well, the PM will say *"with 8 people it's not worth writing anything, get Notion"*. The value is in having heard **also** the PM's voice, which alone you would never have inserted into the reasoning.

::: note

**Worth it when** — architectural or stack decision with real trade-offs across dimensions you can't weigh alone (full-stack vs. UX vs. PM vs. DBA). The value is in the **explication of dissent**, not the final synthesis.

**It's filler when** — questions with a single technical answer (*"what's the complexity of a quicksort?"*). Staging a debate on settled questions doesn't add perspective, it lengthens the answer.

:::

#### 6.4.4 Context Engineering — the new frontier

"Pure" prompt engineering has a limit: no matter how well you formulate the request, the model only knows what you've given it. If you're asking it to review an architecture without showing it the code, or to write a product description without showing it brand guidelines and existing cards, you're asking the impossible.

**Context engineering** is the discipline of *what you make available to the model before the question*: relevant files, pre-existing examples, documentation, screenshots. The more the context is **clean, structured, and relevant**, the less you have to rely on "magic" prompts — and the more the structured prompts we discuss here pay off.

For **web chat** this means uploading PDFs, attaching images, using Projects to persist briefs and reference files.

For **Claude Code CLI** context engineering translates into three mechanisms you've already seen or will see:

- **`CLAUDE.md`** (see section 7) — persistent project context: stack, conventions, rules. Loaded at every session.
- **Auto Memory** (see section 7) — dynamic learnings written by the model itself, persistent across sessions.
- **Subagent as delegation strategy** (see section 12) — when the context to load is large, you delegate to a subagent that digests it and returns only the summary.

An important thing: **more context isn't automatically better**. [Chroma's research on context rot](https://www.elastic.co/search-labs/blog/context-engineering-vs-prompt-engineering) shows that beyond certain thresholds the model degrades. The rule is "**better little and well-ordered than a lot and chaotic**". It's the same principle that governs [section 8](#context-management) of this guide on context management: treat it as a scarce resource, not as a dump.

::: note

**Worth it when** — always relevant if the model has to produce output coherent with material it doesn't know: real codebase, brand guidelines, DB schemas, past decisions. It's the highest-leverage discipline of 2026 and is almost always more effective than an elaborate prompt.

**It's filler when** — loading everything-everything: [context rot](#what-context-is-and-why-it-matters) degrades performance beyond certain thresholds. It's not filler in the sense of verbosity, but it becomes **context-noise**. The rule is "little and orderly": files pertinent to the task, not the whole `vendor/` or the whole email archive.

:::

#### 6.4.5 Meta-prompting (the prompt for the prompt)

The idea is almost counterintuitive: **ask the model to write the prompt you should give it**. It's useful when a task is new or complex, and you don't know where to start.

**Operational pattern**:

```
In the role of Expert Prompt Engineer, you have to help me build
an effective prompt for another session.

Goal of the future session: [describe the task in a rough way]

Proceed like this:
1. Analyze my request. Identify ambiguities and missing
   information.
2. Ask me 3-5 clarifying questions. Wait for my answers.
3. After my answers, write me the final complete prompt,
   structured with context/task/constraints/output format.

Start with the questions.
```

What makes this pattern work: the model doesn't give you the prompt right away (impossible, info is missing), but **forces the explication of ambiguities** that you alone wouldn't have noticed. The questions it asks are often those that, if not asked of you, would have led to a wrong result.

::: note

**Worth it when** — new or vague task where you don't know what you're asking: complex prompts to formalize for reuse (e.g., to be promoted in `CLAUDE.md` or in custom slash commands), unknown domain, marketing brief to translate into a technical spec. The 3-5 clarifying questions are worth the round.

**It's filler when** — task you already know how to formulate well. Asking the model to "write you the prompt" on a trivial refactor is a waltz to arrive at a formulation you would have written in 30 seconds.

:::

#### Summary table: which technique for which problem

| Technique | Problem it solves | Hint "this is the right one" |
|---|---|---|
| **4+1 Anatomy** | Vague, generic, unusable output | You just need to be more specific |
| **XML-like delimiters** | Long prompt where the model confuses sections | You have 3+ semantic blocks in the prompt |
| **Chain of Thought** | Answers that skip intermediate steps | Complex, multi-phase decision |
| **Few-Shot** | Output that doesn't respect a precise style | You have 2+ examples of the desired pattern |
| **Panel of Experts** | Important decision with unclear trade-offs | You want to hear different angles, not a synthesis |
| **Context Engineering** | The model doesn't know your context | You have reference material to load |
| **Meta-prompting** | You don't know well where to start | New, vague task to formalize |

In summary: in 2026 the truly high-yield levers are **explicit instructions**, **curated context**, and **examples when the format requires them**. The most "performative" techniques (verbal CoT to excess, panel on closed questions, meta-prompting on trivial tasks) are leftovers from old models and today often worsen the prompt's signature — more input tokens, more risk of confusing the model, no advantage on the output.

### 6.5 Claude Code specifics compared to chat

Prompt engineering was born from chat and evolved there. In Claude Code CLI there are three substantial differences to keep in mind:

- **Tool use**: the prompt doesn't just describe the output — it can activate actions. *"Find all functions that use `mysql_query`"* in chat produces a suggestion; in CLI it produces an actual reading of all files and a real list, because Claude executes Grep. The prompt should be calibrated knowing that every request can translate into actions on your filesystem.
- **Plan Mode** (see section 5) is a variant of prompt engineering applied: it explicitly separates the planning phase (read-only) from execution. For non-trivial tasks it's the safest way to formulate risky requests.
- **`CLAUDE.md` and custom commands**: prompts that work well shouldn't be written every time. You **promote** them to permanent instructions in `CLAUDE.md` (see section 7) or to custom slash commands in `.claude/commands/` (see section 15.6). See also 6.8 below.

### 6.6 Before/after examples

Three practical cases that show the difference between a vague prompt and a structured one. All on realistic development tasks.

**Case 1 — Refactoring**

Before:

```
Refactor this function to make it more readable
```

After:

```
Context: TypeScript code from a Node app, function that handles
auth login. Project style: PSR-style but for TS, max 60 lines
per function, no nested ternary, early returns preferred.

Task: refactor the `authenticateUser` function below.

Constraints:
- Maintain exactly the same public signature and the same
  behavior (tests must continue to pass).
- Break the function into 2-3 private helper functions if needed.
- Replace nested if with early returns.
- No new external libraries.

Output format: 1) TypeScript block with new code,
2) brief bullet summary of what you changed and why.
```

**Case 2 — Test generation**

Before:

```
Write the tests for this function
```

After:

```
Context: Vitest, TypeScript email validation module (see
function below).

Task: write a Vitest test suite for `validateEmail`.

Constraints:
- Coverage: all return paths of the function
- Edge case tests: empty email, too long (>254), invalid
  format (no @, multiple @s, no TLD), numeric TLD
- No snapshot tests
- Use `describe` to group by scenario, `it` for cases

Output format: TS code block only, no explanation.
```

**Case 3 — Structured output for pipelines**

Before:

```
Analyze this function and tell me if it has security problems
```

After:

```
Context: pre-commit code review, output will be parsed by a
Python script to insert findings into a report.

Task: analyze the PHP function below for security problems
(SQL injection, XSS, missing nonce, capability check, hardcoded
secrets).

Constraints:
- Only real problems, no overly speculative "potential" ones
- For each finding: severity (critical/high/medium/low), line,
  explanation, suggested fix

Output format: JSON ONLY, no text before or after, schema:

{
  "findings": [
    {
      "severity": "critical" | "high" | "medium" | "low",
      "line": <number>,
      "type": "<sql_injection | xss | missing_nonce | ...>",
      "description": "<string>",
      "suggested_fix": "<string>"
    }
  ],
  "summary": {
    "critical": <number>,
    "high": <number>,
    "medium": <number>,
    "low": <number>
  }
}
```

The principle is always the same: reduce the degrees of freedom the model can make mistakes on.

### 6.7 Common anti-patterns

Mistakes you'll see (and make) recurrently:

- **Hope Coding** — *"Write me a product description"*, *"fix this bug"*, *"refactor this function"*. No context, no constraints, no format. It's the founding antipattern: it produces random results.
- **Multiple tasks in one prompt** — *"Refactor the function, write the tests, update the documentation, and commit"*. The model chooses what to do and what to skip, and the quality of each individual task collapses. One task at a time.
- **Relying on the role as a shortcut** — *"Act as a senior engineer"* doesn't replace a well-made brief. The role, where useful, completes the prompt; it doesn't replace it.
- **Context too long or chaotic** — loading 50 files "for safety", pasting 200 lines of irrelevant logs, describing entire projects when a synopsis would suffice. See section 8 (Context management): the model degrades with excessive context.
- **Ambiguity in constraints** — *"not too long"*, *"in adequate tone"*. "Adequate" to what? "Long" compared to what? Quantified, not qualitative constraints: "max 100 lines", "confidential tone like in the examples below".
- **Not documenting prompts that work** — you rewrite the same complex prompt every time. Methodological mistake: see 6.9.

### 6.8 Promoting a prompt: when it goes in CLAUDE.md or in a custom command

Once a prompt works, you have three possible destinations:

- **Daily** — you rewrite it on the fly when needed. Fine for occasional tasks.
- **`CLAUDE.md`** (see section 7) — persistent project instructions. Loaded at every session, you don't have to repeat them anymore. Perfect for rules that always apply in that project: code conventions, build commands, prohibitions.
- **Custom slash commands** in `.claude/commands/` (see section 15.6) — recurring workflows you want to recall with a single command. Perfect for things you do often but not in *every* prompt.

**Promotion threshold**, practical rule: **if you find you've rewritten the same instruction for the third time, it goes somewhere**. Project rules in `CLAUDE.md`, personal workflows in custom commands.

### 6.9 Prompt library: archiving and versioning

Prompts that work are **assets**, not single-use text. Treating them as such means archiving them with some minimum discipline.

Minimum pattern that works:

- A `prompts/` folder (or a single Markdown file, or Notion, or whatever you prefer) with a file per pattern: `code-review-php.md`, `refactor-typescript.md`, `panel-of-experts-software.md`, etc.
- For each prompt: a brief description of the use case, the actual prompt, any notes on known limits.
- **Versioning**: when you refine a prompt, keep the previous version with a suffix (`-v1.md`, `-v2.md`) and a brief changelog of what changed and why.
- **Feedback loop**: when a prompt fails, note the case that broke it. Often it's an edge case that will help you refine it.

For Claude Code CLI, the most recurring prompts can be **promoted to custom slash commands** (see 15.6) — they effectively become part of your tool, invocable with a single `/`.

---


---

> ← [5. Plan Mode](05-plan-mode.md) | [Index](README.md) | [7. Persistent memory](07-memory.md) →
