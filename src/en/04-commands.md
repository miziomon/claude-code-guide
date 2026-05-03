# Practical Guide to Claude Code CLI

> **Version 4.23 — May 2026** — verified on Claude Code v2.1.123
> Licensed under [Creative Commons BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

> ← [3. The first end-to-end project](03-first-project.md) | [Index](README.md) | [5. Plan Mode](05-plan-mode.md) →

---

## 4. Essential commands and shortcuts

Claude Code is a **command-first** application: no dropdown menus, no button palettes, no preferences hidden in dialog windows. Everything is done through three types of syntax that you'll learn once and use thousands of times. This chapter explains the philosophy first, then dives into the most frequently used commands.

### 4.1 The command-driven syntax: why it works this way

Coming from a desktop application, you expect menus, icons, shortcuts with labels under buttons. Claude Code has none of that: you command it by **writing**. Three syntax families:

- **CLI flags** (passed to `claude` from the terminal): `claude --continue`, `claude -p "prompt"`, `claude --model sonnet`. They define **how a session is launched**.
- **Slash commands** (typed inside the interactive session): `/init`, `/clear`, `/plan`, `/agents`. They change state or execute actions **during** the session.
- **Keyboard shortcuts**: `Shift+Tab`, `Esc Esc`, `Alt+P`. They modify behavior and modes **on the fly**.

At first glance it can be intimidating: without a menu to "look at", how do you discover what exists? Answer: there's a picker. Type `/` alone in the session and it opens the filterable list of all available slash commands — built-in, plugin-installed, ones you've added. Type `/co` and you filter to `/compact`, `/config`, `/copy`, `/continue`, `/cost`. The same applies to `claude --help` from the terminal for flags.

The principle is the one adopted by git, vim, SQL, and almost all professional terminal tools: **efficiency over discoverability**. Learning a command costs more than clicking a button the first time; but you type the command in half a second a hundred times in a row, and over an intensive work session it makes the difference. Once you've internalized that `/clear` resets the context, you no longer go looking for a "new chat" button because two characters are faster than any click.

> **A useful mindset**. Think of the prompt as an enhanced shell. In bash you type `git status`, in Claude Code you type `/context`. The difference isn't cosmetic: the model reads your input and decides what to do, but commands starting with `/` or shortcuts with modifiers are **deterministic** — they act on the session environment, not on the agent. It's the same distinction between a shell command and a linguistic request to the model.

Three special prefixes make the experience even smoother: `@` to refer to a file or subagent (see [section 12](#subagents-orchestrating-specialized-work)), `!` to execute a shell line without model interpretation, `/` for the command picker. I'll dig into them in 4.8.

> **Evolution disclaimer.** Claude Code introduces new slash commands almost every release: from ~30 in mid-2025 to 90+ in April 2026. This guide documents the most stable and widely used commands at the time of writing. For the live and complete list: `claude --help` from the terminal, `/help` or `/` inside the session, and the [official CLI reference](https://code.claude.com/docs/en/cli-reference).

### 4.2 Essential CLI flags

These are the flags you'll use every day. Concise table, then deep dive on the most important ones:

| Flag | Short form | What it does |
|---|---|---|
| `claude` | — | Starts an interactive session |
| `claude "prompt"` | — | Starts with an initial prompt already written |
| `claude --continue` | `-c` | Resumes the most recent session in the directory |
| `claude --resume` | `-r` | Opens a picker of past sessions to choose from |
| `claude --print "prompt"` | `-p` | Non-interactive mode (headless): execute, print, exit |
| `claude --model <name>` | — | Choose model (e.g., `sonnet`, `opus`, `haiku`, `opusplan`) |
| `claude --permission-mode <mode>` | — | Start in a specific permission mode (`default`, `acceptEdits`, `plan`, `auto`, `bypassPermissions`) |
| `claude --output-format <fmt>` | — | Output format: `text`, `json`, `stream-json` (for CI/CD pipelines) |
| `claude --add-dir <path>` | — | Adds working directories accessible beyond the `cwd` |
| `claude --dangerously-skip-permissions` | — | Skip all confirmations. Only in isolated environments (see section 10) |
| `claude --version` | `-v` | Shows the installed version |
| `claude --help` | `-h` | Lists the main flags |

#### `-p` / `--print`: headless mode

The flag that opens Claude Code to the world of automation. Executes a single prompt, prints the output, and exits — no interactive session. It's the pillar of any CI/CD integration:

```bash
# Example: automatic review of a PR's changes
claude -p "Review the changes in this PR and flag any security issues" \
       --output-format json > review.json

# Pipeline: passing a file via stdin
cat changelog.md | claude -p "Summarize this changelog in 5 bullet points"
```

Combined with `--output-format json` it produces structured output parseable by subsequent pipeline steps. See also `--max-turns` and `--max-budget-usd` in 5.3 for limiting execution.

#### `-c` / `--continue` and `-r` / `--resume`

The two syntaxes for resuming a conversation. The difference is simple:

- `claude -c` opens **the last session** in this directory. Use case: you closed 10 minutes ago, you want to resume from there.
- `claude -r` opens an **interactive picker** showing all past sessions (with name, date, first prompt). Use case: you want to return to that conversation three days ago about the auth module refactor.

Both also accept an additional prompt to restart with a new request:

```bash
claude -c "Continue from the refactor point: now add the tests"
```

#### `--model` and its aliases

Three main aliases (`sonnet`, `opus`, `haiku`) plus the hybrid mode `opusplan` (see [section 5](#plan-mode-think-before-you-write)) and the full ID syntax (`claude-sonnet-4-6`, `claude-opus-4-7`, etc.). Aliases auto-update to the most recent model: writing `--model sonnet` today and tomorrow may point to different versions. For reproducibility in CI/CD, use the full ID.

### 4.3 Advanced CLI flags

A selection of specialist flags, grouped by scenario. For the live and complete list: [`claude --help`](https://code.claude.com/docs/en/cli-reference).

| Category | Main flags | When you need them |
|---|---|---|
| Bounded execution | `--max-turns N`, `--max-budget-usd X` | Limit cost or depth in headless mode |
| Structured output | `--output-format json\|stream-json`, `--json-schema <schema>`, `--include-hook-events` | Automatic parsing in pipelines, schema validation |
| Advanced sessions | `--fork-session`, `--session-id <UUID>`, `--name "<name>"`, `--no-session-persistence` | Branching, controlled ID, ephemeral sessions |
| MCP and plugins | `--mcp-config <path>`, `--strict-mcp-config`, `--plugin-dir <path>`, `--tools "Read,Edit"`, `--allowedTools`, `--disallowedTools` | Fine configuration of tools and integrations |
| Web sessions | `--remote "task"`, `--rc [name]`, `--teleport`, `--from-pr <number>` | Bring the session to claude.ai and back |
| Worktrees and teams | `--worktree <name>` (`-w`), `--tmux`, `--teammate-mode` | Parallel work on isolated branches with git worktree |
| System prompt | `--system-prompt "..."`, `--append-system-prompt "..."`, `--system-prompt-file <path>` | Customize or extend the system instructions |
| Inline subagents | `--agent <name>`, `--agents '{"name":{"prompt":"..."}}'` | Define subagents on the fly without creating files |
| Diagnostics | `--debug`, `--verbose`, `--debug-file <path>` | Troubleshooting hooks, MCP, abnormal behavior |
| Performance | `--bare`, `--exclude-dynamic-system-prompt-sections` | Fast startup for scripts, cache optimization |
| Effort/thinking | `--effort low\|medium\|high\|xhigh\|max` | Trade-off speed vs depth |

To these are added separate commands that don't use the `claude` prefix as a session argument: `claude doctor` (diagnostics), `claude install [version]`, `claude update`, `claude auth login|logout|status`, `claude agents` (subagent list), `claude plugin <subcommand>`, `claude mcp <subcommand>`, `claude setup-token` (long-lived token for CI). The logic is simple: **flags** modify the launch of a session, **subcommands** execute administrative actions without opening one.

### 4.4 Slash commands: the heart of the interactive session

Once inside the session, **slash commands** are the way to tell Claude Code "do this specific thing" without ambiguity. The important distinction is between:

- **Built-in slash commands**: part of the base product (`/init`, `/clear`, `/compact`, `/plan`, `/agents`, `/hooks`, etc.). They are the system building blocks.
- **Skills** invoked as slash commands (`/security-review`, `/simplify`, `/loop`, `/ultrareview`, etc.). They are playbooks documented in [chapter 10](#skills-the-extension-mechanism) and behave like slash commands because Anthropic chose the same syntax: you type `/`, you see everything together.
- **Custom commands** that you can define in `.claude/commands/` (see [section 15](#advanced-workflows-and-tips) "Custom slash commands") — they will appear in the same picker.
- **MCP prompts**: installed MCP servers can expose commands in the format `/mcp__<server>__<prompt>`.

All end up in the same picker when you type `/`. Filter it from the keyboard by writing the first letters.

### 4.5 Essential slash commands

Anthropic has already passed 50 built-in slash commands (plus those added by skills, plugins, and MCP), and the list grows with every release. This table is a **curated selection** of the commands you'll encounter most often in daily work: for the live and complete list, run `/help` in session or consult the [official reference](https://code.claude.com/docs/en/commands).

| Command | What it does |
|---|---|
| `/help` | Lists all available commands |
| `/init` | Generates `CLAUDE.md` by analyzing the project |
| `/plan [description]` | Enters Plan Mode (read-only) |
| `/clear` | Resets the conversation context (alias: `/reset`, `/new`) |
| `/compact [instructions]` | Compresses the conversation into a summary |
| `/context` | Shows context usage with optimization suggestions |
| `/memory` | Auto Memory and loaded `CLAUDE.md` files management |
| `/agents` | List, create, manage subagents |
| `/hooks` | Read-only browser of the active hook configuration |
| `/model [name]` | Change model during the session |
| `/effort [level]` ★ | Sets effort: `low`, `medium`, `high`, `xhigh`, `max`, `auto` |
| `/fast [on\|off]` | Enables/disables fast mode |
| `/undo` | Undo the last Claude action |
| `/rewind` | Rewind to a previous point (alias: `/checkpoint`) |
| `/branch [name]` | Create a branch of the current conversation (alias: `/fork`) |
| `/rename [name]` ★ | Rename the current session to find it again in `/resume` |
| `/resume [session]` | Resume a conversation (alias: `/continue`) |
| `/diff` | Interactive diff viewer (uncommitted changes + per-turn diff) |
| `/copy [N]` | Copy the last response to clipboard |
| `/usage` | Session cost, plan limits, statistics (alias: `/cost`, `/stats`) |
| `/btw <question>` ★ | Side question that doesn't pollute history (no tool use) |
| `/ultrareview [PR]` ★ | Multi-agent cloud review of the branch or a GitHub PR |
| `/recap` | Summary of the current session |
| `/config` | Settings panel (theme, model, output style, etc.) |
| `/exit` or `/quit` | Closes the session |

> ★ Commands introduced in recent releases (v2.1.110+ of Claude Code, spring 2026). If you don't find them, update with `claude update`.

#### `/init` — generating CLAUDE.md for a new project

See section [7 — Persistent memory](#persistent-memory-claude.md-and-auto-memory). In short: launched from the project root, it analyzes structure, config files, and dependencies and produces a draft `CLAUDE.md` to refine by hand. It's the first command to run on a new repo.

#### `/plan` and Plan Mode

See section [5 — Plan Mode](#plan-mode-think-before-you-write). Enters read-only mode: Claude analyzes, proposes a plan, but doesn't write anything until you approve. The most important feature for safe CLI use.

#### `/clear`, `/compact`, `/context` — context management

See section [8 — Context management](#context-management). In three commands:

- `/clear` resets everything, fresh session.
- `/compact` summarizes the conversation while keeping key decisions, frees tokens.
- `/context` shows how much you're consuming and tells you if it's time to act.

Concrete example:

```
[After reading 30 files and doing a heavy refactor]
/context
> Context usage: 78% (156k / 200k tokens)
>   Tool results: 112k (read files, build output)
>   Conversation: 38k

/compact keeping the decision to use Repository pattern
> [conversation compressed, context freed]
```

#### `/memory` — Auto Memory

See section [7 — Persistent memory](#persistent-memory-claude.md-and-auto-memory). Shows the `CLAUDE.md` files loaded in the current session, lets you toggle Auto Memory on/off, opens the memories folder.

#### `/agents` — subagents

See section [12 — Subagents](#subagents-orchestrating-specialized-work). Opens a tabbed interface: the "Running" tab lists active subagents, the "Library" tab shows available ones and lets you create new ones.

#### `/hooks` — hook configuration inspection

See section [13 — Hooks](#hooks-automating-claude-codes-lifecycle). Shows the active hook configuration: for each event, how many hooks are registered and from which settings file. **Read-only**: to modify hooks you have to edit `settings.json` directly.

#### `/model` and `/effort` — choosing the right model

See section [5 — Plan Mode](#plan-mode-think-before-you-write) (paragraph on `opusplan`). `/model` opens the picker and lets you switch at runtime; `/effort` adjusts the model's "effort level" (higher = more thinking time, potentially better output, higher cost). `auto` lets Claude decide.

#### `/undo`, `/rewind`, `/branch` — conversational checkpoints

Three related commands to manage "time" in the session:

- `/undo` cancels Claude's **last action** (e.g., the last file edit).
- `/rewind` rewinds to a **previous point** in the conversation and restores state (code and context). Powerful command for those who experiment — you use it when a path has proven wrong and you want to go back N steps.
- `/branch [name]` creates a **fork** of the conversation at the current point. The original conversation remains intact, you proceed in a parallel line. Use case: you have an alternative idea and want to explore it without losing the main thread. You return to the original with `/resume`.

#### `/btw` — the side question

A little-known but useful command. Ask a question that **you don't want in the session history**: Claude sees it, answers based on the current context, but the conversation doesn't get polluted. No tool use. Example:

```
/btw what's the difference between @wordpress/scripts and @wordpress/create-block?
> [Claude responds from knowledge, no files read, no edits]
```

Perfect for quick clarifications during a long task, without derailing the thread.

### 4.6 Slash commands for specific workflows

Grouped table, one row per category. All these commands are documented in detail in the [official reference](https://code.claude.com/docs/en/commands).

| Category | Commands |
|---|---|
| Cloud skills (distributed review) | `/ultrareview [PR]`, `/ultraplan <prompt>`, `/autofix-pr [prompt]` |
| Local code review | `/review [PR]`, `/security-review`, `/simplify [focus]` |
| Execution and batch | `/batch <instruction>`, `/loop [interval] [prompt]`, `/schedule [descr]` (alias `/routines`) |
| Diagnostics and troubleshooting | `/doctor`, `/debug [description]`, `/heapdump`, `/usage` |
| Export | `/export [filename]`, `/copy [N]` |
| Terminal experience | `/theme`, `/keybindings`, `/terminal-setup`, `/tui [default\|fullscreen]`, `/focus` |
| IDE/web integration | `/ide`, `/desktop` (alias `/app`), `/teleport` (alias `/tp`), `/web-setup` |
| MCP and plugins | `/mcp`, `/plugin` (alias `/plugins`), `/reload-plugins` |
| Permissions and security | `/permissions` (alias `/allowed-tools`), `/sandbox` |
| Status and statistics | `/status`, `/insights`, `/release-notes`, `/team-onboarding` |
| Auth and profile | `/login`, `/logout`, `/privacy-settings`, `/upgrade` |
| Accessibility and input | `/voice [hold\|tap\|off]` |
| Background tasks | `/tasks` (alias `/bashes`) |
| Learning skills | `/powerup`, `/feedback` (alias `/bug`) |

### 4.7 Keyboard shortcuts

Grouped by usage area.

#### Permission modes (the main cycle)

`Shift+Tab` **cycles** through permission modes: `default → acceptEdits → plan → custom modes → default`. It's not a "Plan Mode" binding: it's a mode selector. To get to Plan Mode from `default`, press it twice; to exit, press until you return to `default`. The current state is always shown in the prompt bar.

#### Model and thinking

| Shortcut | Action |
|---|---|
| `Alt+P` (`Option+P` on macOS) | Opens the model picker without canceling the prompt in progress |
| `Alt+T` | Toggle extended thinking |
| `Alt+O` | Toggle fast mode |

On macOS they require the *Option as Meta key* configuration in the terminal.

#### Session and flow

| Shortcut | Action |
|---|---|
| `Ctrl+C` | Cancel current input or interrupt generation |
| `Ctrl+D` | Exit the session |
| `Ctrl+L` | Clear the screen and redraw (the conversation remains) |
| `Esc Esc` | Rewind/summarize the conversation (rewind/summarize, see `/rewind`) |
| `Ctrl+B` | Background running tasks (tmux users: twice) |
| `Ctrl+X Ctrl+K` | Terminate all background agents (twice within 3 seconds to confirm) |

#### Transcript and history

| Shortcut | Action |
|---|---|
| `Ctrl+O` | Opens the transcript viewer (shows detailed tool use, expanded MCP calls) |
| `Ctrl+R` | Reverse search in prompt history |
| `Up/Down arrows` (or `Ctrl+P`/`Ctrl+N`) | Navigate history |

Inside the transcript viewer (`Ctrl+O`): `Ctrl+E` expands/collapses, `[` writes the entire conversation to scrollback for `Cmd+F`/copy, `v` opens in `$VISUAL`/`$EDITOR`, `q` or `Esc` closes.

#### Prompt editing (readline-style)

| Shortcut | Action |
|---|---|
| `Ctrl+A` | Beginning of line |
| `Ctrl+E` | End of line |
| `Ctrl+K` | Delete to end of line |
| `Ctrl+U` | Delete to beginning of line |
| `Ctrl+W` | Delete previous word |
| `Ctrl+Y` | Re-paste the last deleted text |
| `Alt+B` / `Alt+F` | Move cursor one word back / forward |
| `Ctrl+G` or `Ctrl+X Ctrl+E` | Open the prompt in `$EDITOR` for complex edits |

These are the same conventions as `bash`/`zsh`/Emacs. If you come from the Unix terminal, you already know them.

#### Multiline

| Method | Availability |
|---|---|
| `\` + `Enter` | All terminals (most reliable) |
| `Shift+Enter` | iTerm2, WezTerm, Ghostty, Kitty, Warp, Apple Terminal (native) |
| `Option+Enter` (macOS) | After *Option as Meta* configuration |
| `Ctrl+J` | Any terminal (readline-native syntax) |

On VS Code, Cursor, Windsurf, Alacritty, Zed you need to run `/terminal-setup` the first time.

#### Vi mode

If you come from Vim, activate it with `/config` → Editor mode → `vi`. You'll have full NORMAL/INSERT/VISUAL with motions (`hjkl`, `w`/`e`/`b`, `0`/`$`, `f{char}`) and operators (`d`, `c`, `y`, `>`/`<`). Complete documentation at [interactive-mode#vim-editor-mode](https://code.claude.com/docs/en/interactive-mode).

### 4.8 The `@`, `!`, `/` syntax — the three prefixes that change everything

Three single characters that, placed at the beginning of input or inline, activate powerful shortcuts. It's the "Claude Code" version of bash dollar-substitution or Markdown reference syntax:

#### `/` — the command picker

Typed at the start of a line, opens the filterable picker of **all** slash commands available in the session: built-in, skills, custom commands, MCP prompts. Continue typing to filter. It's the way to discover what's there without reading documentation.

```
/co
> /compact     Compress conversation...
> /config      Open settings panel...
> /context     Show context usage...
> /continue    Alias of /resume...
> /copy        Copy last response...
> /cost        Alias of /usage...
```

#### `!` — inline bash

Typed at the start of a line, executes **the line directly as a shell command**, without model interpretation. The output enters the session as a message. Equivalent to briefly stepping out of the Claude terminal to do a quick command, without losing the thread:

```
!git status --short
> M  src/guida.md
> M  scripts/style.css

!ls -la output/
> total 2.6M
> -rw-r--r-- ... Guida_Claude_Code_CLI.pdf
> -rw-r--r-- ... Guida_Claude_Code_CLI_17x24.pdf
```

Perfect for quick checks (`git status`, `ls`, `pwd`, `echo $VAR`) without having to tell Claude *"please run..."*.

#### `@` — references to files and subagents

Typed inline (in the middle of a sentence), opens a picker that autocompletes:

- **Project file and folder paths**: write `@src/` and tab to `src/guida.md`. The inserted path is read by Claude as a reference to the file.
- **Available subagents**: `@agent-wp-security-auditor` to explicitly invoke a custom subagent (see [section 12](#subagents-orchestrating-specialized-work)).

Combined example:

```
Review @src/guida.md for typos in chapters 5 and 6.
When you find a section that talks about security,
delegate to @agent-wp-security-auditor for a more thorough audit.
```

The three prefixes aren't "advanced commands": they are the **everyday way** to work fast in Claude Code once you've metabolized them.

---


---

> ← [3. The first end-to-end project](03-first-project.md) | [Index](README.md) | [5. Plan Mode](05-plan-mode.md) →
