# Practical Guide to Claude Code CLI

> **Version 4.23 — May 2026** — verified on Claude Code v2.1.123
> Licensed under [Creative Commons BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

> ← [16. Conclusions](16-conclusions.md) | [Index](README.md) | [Appendix B — Sources](appendix-b-sources.md) →

---

## Appendix A — Glossary

Recurring terms in the guide and in the Claude Code ecosystem, useful as a quick reference.

::: glossary

**Agent (agentic)** — AI system capable of executing actions in the real world (commands, file modifications, API calls), not just producing text. Claude Code is an agent unlike classic chat.

**Agent Teams** — Experimental Claude Code feature (requires the environment variable `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`) that allows multiple independent instances of Claude to run in true simultaneous parallelism, coordinated via shared task list and message mailbox. Not to be confused with multi-delegation to subagents in foreground, which is sequential instead.

**Auto Memory** — Persistent memory that Claude Code feeds autonomously during sessions (introduced in v2.1.59). Unlike `CLAUDE.md`, written by the user, Auto Memory is written by the model: it accumulates learnings, patterns, and recurring corrections of the project. It lives in `~/.claude/projects/<project>/memory/` and is organized into an index (`MEMORY.md`) plus topic files loaded on-demand.

**Chain of Thought (CoT)** — Prompt engineering technique that explicitly asks the model to "reason step by step" before answering, instead of producing the conclusion directly. Forces explication of logical steps and improves accuracy on complex tasks (debugging, architectural decisions, multi-phase problems).

**CLAUDE.md** — Markdown file in the project root that contains persistent context: stack, conventions, commands, rules. Automatically read at every session.

**CLI (Command Line Interface)** — Command-line interface. The `claude` tool is used from the terminal instead of from the browser.

**Context engineering** — Discipline complementary to prompt engineering: instead of focusing on how to formulate the request, it concerns *what information to make available to the model before* asking it. For Claude Code CLI it materializes in `CLAUDE.md`, Auto Memory, and delegation via subagent. Guiding principle: "better little well-ordered context than much chaotic context".

**Few-shot prompting** — Technique that teaches the desired style or format by providing two or more examples before the actual request. Particularly effective for voice consistency (FAQs, microcopy) and reproduction of structured formats hard to describe in words.

**Headless mode** — Non-interactive execution via `-p` flag. Claude receives a prompt, produces output, exits. Used for CI/CD and automations.

**Hook** — Script (bash, HTTP, prompt, agent or MCP tool) configured in `settings.json` that intercepts Claude Code lifecycle events: `PreToolUse`, `PostToolUse`, `SessionStart`, `UserPromptSubmit`, and others. Used to validate, log, inject context, or block operations. Different from Subagent (executes delegated work) and from Skill (enriches the main agent's context): a Hook acts **around** the main agent without being part of it. For complete treatment see section 13.

**Hope Coding** — Prompt engineering antipattern: launching generic requests to AI "hoping" it guesses what we wanted, without specifying context, constraints, or output format. Produces random results and contrasts with *conscious Vibe coding* (see Vibe coding entry) based on structured prompts.

**JSON-RPC** — Textual communication protocol (based on JSON) for remote procedure calls. It's the base layer on which MCP packages all its messages between client and server. Defines request, response, and notification with a standardized format.

**MCP (Model Context Protocol)** — Open protocol, open-sourced by Anthropic in November 2024, that standardizes the way an AI application (host) connects to external data sources and tools. Client-server model based on JSON-RPC 2.0; transport via stdio (local) or HTTP+SSE (remote). Three primitives: tools, resources, prompts. See chapter 11 for complete treatment.

**MCP server** — Process that implements the MCP protocol and exposes one or more functionalities (tool, resource, prompt) to a compatible AI host. Can be written in any language for which an SDK exists (Python, TypeScript, Java, C#, Rust, Kotlin, Swift). Typically local (stdio) for personal integrations, hosted (HTTP+SSE) for team integrations.

**MCP tool** — One of the three primitives of an MCP server: callable function exposed by a server. It has a name, AI-readable textual description, JSON schema of arguments. When the model decides to call it, the host sends a `tools/call` JSON-RPC request to the server. It's the most used primitive in custom MCP servers.

**MEMORY.md** — Index file of a project's Auto Memory, located in `~/.claude/projects/<project>/memory/`. Loaded at every session (limit ~200 lines, ~25 KB), it lists and describes the topic files of the folder, which are then loaded on-demand when their content is relevant.

**Meta-prompting** — Prompt engineering technique that consists of asking the AI itself to write the prompt to use in a subsequent session. Pattern: the model, in the role of "Expert Prompt Engineer", analyzes raw specs, asks clarifying questions, produces a final structured prompt. Useful for new or complex tasks worthy of formalization.

**Native installer** — Official installation method introduced by Anthropic in 2025: a `curl` or `PowerShell` command without Node.js dependencies, with auto-update.

**OAuth** — Authentication protocol used at first launch of `claude`. Opens the browser, you log in with your Anthropic account, the session persists.

**Panel of Experts (Round table)** — Prompt engineering technique that simulates a discussion among virtual experts, each with their own viewpoint and area of expertise. Particularly precious for exploring an idea, putting one's beliefs into question, choosing a stack, or stress-testing an architecture: the value isn't in the final synthesis but in the explication of trade-offs each decision implies. See section 6.4.3 for the complete prompt template.

**Plan Mode** — Read-only mode activated via `/plan` or by cycling with `Shift+Tab` (which scrolls between `default → acceptEdits → plan → ...`). Claude analyzes and proposes a plan but doesn't modify anything until you approve.

**Plugin** — Package distributed via marketplace that extends Claude Code with slash commands, agents, and skills. Managed with `claude plugin install`.

**Prompt engineering** — Discipline of formulating effective requests for an LLM. Articulated in four fundamental ingredients (context, task, constraints, output format) plus an optional one (role). On top 2026 models, "role prompting" is downsized in favor of structural constraints and the use of XML-like delimiters (`<context>`, `<task>`, `<constraints>`, `<output_format>`). See section 6 for complete treatment.

**Prompt injection** — Attack in which malicious instructions are injected into files, comments, or responses from external services to manipulate AI behavior.

**REPL (Read-Eval-Print Loop)** — Interactive read-execute-print cycle. Claude Code's interactive session is a REPL.

**Session** — Ongoing conversation with Claude Code, persistent across restarts. Each session has its own context and history.

**Skill** — Specialized module (folder with `SKILL.md`) that Claude automatically activates when the skill description matches the task context. Not invoked with slash commands.

**Slash command** — Command starting with `/` inside an interactive session (e.g., `/init`, `/compact`, `/plan`). Different from launch flags that start with `--`.

**Subagent** — Isolated Claude instance created by the `Task` tool to execute searches or specialized tasks without "polluting" the main session context.

**Token** — Unit of text measurement for an LLM (approximately 4 characters in English, slightly less in Italian). API costs are calculated in input and output tokens. Claude Code uses tokens every time it reads a file, receives a prompt, or produces a response.

**Vibe coding** — Term that became popular in 2024-2025 to describe AI-assisted development style: instead of writing code manually, you write a structured prompt describing what it should do, and the AI generates the implementation.

**WSL2 (Windows Subsystem for Linux)** — Linux environment integrated in Windows 10/11. Recommended for using Claude Code on Windows avoiding many compatibility issues.

:::

---


---

> ← [16. Conclusions](16-conclusions.md) | [Index](README.md) | [Appendix B — Sources](appendix-b-sources.md) →
