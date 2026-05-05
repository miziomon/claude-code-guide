# Practical Guide to Claude Code CLI

> **Version 4.30 — May 2026** — verified on Claude Code v2.1.123
> Licensed under [Creative Commons BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

> ← [4. Essential commands and shortcuts](04-commands.md) | [Index](README.md) | [6. Prompt engineering](06-prompt-engineering.md) →

---

## 5. Plan Mode: think before you write

**Plan Mode** is probably the most important feature to master for safe use of Claude Code. It's a **read-only** mode in which Claude analyzes the project and proposes a plan, but **does not touch any file** until you explicitly approve.

### 5.1 Why it matters

Without Plan Mode, Claude tends to be extremely fast at executing. You ask for a "small fix" and find yourself with 12 files modified in 15 seconds. Plan Mode reverses this flow: think first, then execute.

### 5.2 How to activate it

`Shift+Tab` **cycles** through permission modes (`default → acceptEdits → plan → custom modes → default`). To activate Plan Mode starting from `default` mode, press it twice: the first goes to `acceptEdits`, the second to `plan`. The current state is shown in the prompt bar. Alternatively, regardless of the current mode, you can use the explicit command **`/plan`** to enter directly.

> **Windows note**: from v2.1.3 of Claude Code on Windows there's a known bug on the `Shift+Tab` binding. As an alternative, use the `/plan` command.

### 5.3 Tools available in Plan Mode

Claude can only use reading and search tools:

- `Read`, `Glob`, `Grep`: code reading and search
- `WebFetch`, `WebSearch`: online search
- `Task`: delegate research to subagents
- `TodoRead/TodoWrite`: task management

Modification tools are **blocked**:

- `Edit`, `MultiEdit`, `Write`: file editing
- `Bash`: command execution
- All MCP tools that modify state

### 5.4 Example workflow with Plan Mode

```
[Shift+Tab, Shift+Tab — Plan Mode activated]

Prompt: "I need to migrate the logging system from error_log() to Monolog.
Analyze all occurrences and propose an incremental migration plan."

Claude responds with:
- List of the 23 files involved
- Migration strategy in 4 phases
- Risks and points of attention
- Complexity estimate for each phase

[Review the plan]
[If ok: Shift+Tab to exit and approve]
[Claude executes the plan]
```

### 5.5 opusplan: the right model for the right job

Plan Mode delivers its best when the model has high reasoning capabilities for analyzing a complex problem. Once the plan is approved, however, execution is often more mechanical work: applying repetitive edits, writing code following a pattern already defined, launching commands. The same power isn't needed for the two phases — and that's exactly the idea behind **`opusplan`**.

`opusplan` is a model alias that uses **Opus during Plan Mode** and **automatically switches to Sonnet for execution**. You activate it like this:

```bash
# During a session
/model opusplan

# At launch
claude --model opusplan

# In settings.json (persistent)
{ "model": "opusplan" }
```

From that moment Claude uses Opus when you enter `/plan`, then returns to Sonnet as soon as you approve the plan and move to action.

::: warning

**Watch out — the 200K trap in plan-mode.** Even if you activate `opusplan`, the planning phase runs with the standard **200K token** context window, not with the 1M context. The automatic upgrade to 1M described in section [8.7](#models-with-1m-token-window-when-to-switch) applies to the `opus` alias but **does not extend to `opusplan`** ([official source](https://code.claude.com/docs/en/model-config#opusplan-model-setting)).

This is the most expensive operational error in the chapter: those who work on a large codebase assume they're planning with 1M and end up with a plan based on a partial reading of the project, with no warning shown on screen.

**What to do if planning truly requires 1M of context:**

- Use directly `claude --model opus[1m]` (or `/model opus[1m]` in session). Plan-mode will use 1M, but execution will also run on Opus at 1M — so you pay Opus for everything, not just planning.
- Alternatively, keep `opusplan` as default and switch to `opus[1m]` only when the task justifies it (cross-module audit, refactor that crosses dozens of files). For daily use, `opusplan` is still the right choice.

:::

#### Why it makes sense (token economy)

Opus costs **significantly more than Sonnet** per token, both in input and output. In a typical session, planning consumes 20-40% of tokens and execution the remaining 60-80% (file reading, code writing, tool output). Letting Opus do the heavy thinking only where it really matters — planning — and delegating execution to Sonnet significantly reduces the overall bill without losing quality where it counts.

The amount of savings depends on the planning/execution mix of your session: Anthropic's documentation doesn't publish official percentages, but in practice you get an appreciable cost reduction when sessions are balanced between the two phases. To measure real consumption in real time, see the [`/context` command in section 8](#context-management).

#### The principle: not always Opus is needed

There's a widespread tendency to use "always the best model", presuming that Opus produces better output in every scenario. It's not so: Opus is the best model **for complex reasoning**, not for every task. For a variable rename, applying an already-decided pattern, a regex-driven mechanical refactor, Sonnet is perfectly adequate and much faster at generating the output.

> Calling Opus for a repetitive edit is like running the full end-to-end test suite to verify the change of a constant: you pay time and tokens for a guarantee you don't need.

The "right model for the right thing" principle is an asset, not a limitation: it helps you build economically sustainable sessions without sacrificing quality in the phases that require it.

#### When NOT to use it

`opusplan` isn't always the right choice:

- **Simple, well-circumscribed tasks**: an isolated bug fix, a modification to a single file. Sonnet alone is more than sufficient, and activating opusplan would make you use Opus uselessly if you enter Plan Mode by reflex.
- **Sessions where you never enter Plan Mode**: opusplan only makes sense if you use `/plan`. If you always work in direct mode, you would only use Sonnet even with opusplan active — better to set `sonnet` directly.
- **Plans with Opus already included (e.g. Max)**: if you're on a plan where Opus is included with no extra marginal costs, the "savings" don't materialize on the bill. It still remains useful for discipline (Opus only where needed), but the economic driver fades.

#### Availability

`opusplan` is today a stable built-in alias, listed in the [official table of model aliases](https://code.claude.com/docs/en/model-config#model-aliases) alongside `default`, `sonnet`, `opus`, `haiku`, `sonnet[1m]`, and `opus[1m]`. If you don't find it, update Claude Code: `claude --version` and then `claude update`.

---


---

> ← [4. Essential commands and shortcuts](04-commands.md) | [Index](README.md) | [6. Prompt engineering](06-prompt-engineering.md) →
