# Practical Guide to Claude Code CLI

> **Version 4.23 — May 2026** — verified on Claude Code v2.1.123
> Licensed under [Creative Commons BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

> ← [Preface](00-preface.md) | [Index](README.md) | [2. Installation and setup](02-installation.md) →

---

## 1. What is Claude Code

Claude Code is the CLI (Command Line Interface) developed by Anthropic that brings the Claude model directly into the terminal. It's not just a textual chat: it's an **autonomous agent** capable of reading project code, executing shell commands, modifying files, managing Git, and dialoguing with external services via the MCP protocol (Model Context Protocol).

The difference from an IDE-integrated assistant — think GitHub Copilot — isn't merely cosmetic. Copilot lives next to the single open file and suggests line-by-line completions; Claude Code, instead, operates at the **project** level: it sees the directory tree, opens the files it needs, runs tests, launches build commands, and reads the output. This allows it to tackle requests that an autocomplete can't even approach — *"Analyze this project's architecture and explain how authentication is organized"*, *"Refactor the payments module while keeping all tests green"*, *"Find the root cause of this bug and fix it"*.

The work model is an **agentic iterative loop**: Claude receives a goal, explores the code with reading tools, formulates a plan, executes modifications or commands, observes the results, and continues. It's not a linear *prompt → output* pipeline, but an ongoing dialogue in which the agent takes concrete initiative and the user — this is the important point — always remains the final decider: every operation that touches the filesystem or launches commands requires explicit confirmation, unless permissions are deliberately relaxed within a controlled scope.

### 1.1 A brief history

Claude Code was born inside Anthropic as an internal project in 2024, on the wave of a simple observation: the most productive way researchers at the company used Claude for programming wasn't the web chat, but a series of scripts that invoked the model from the terminal, alongside other development tools. Hence the idea of packaging the experience into a clean executable, distributed as an official tool.

The first public version appeared in early 2025 as a *limited preview* reserved for Pro subscribers. It was already functional but essential: textual dialogue, file reading and writing, shell command execution, Git management. In subsequent months the product evolved rapidly, accumulating the primitives we now take for granted. **Plan Mode** introduced the separation between planning and action, giving the user a control point before Claude touches files. **MCP** (Model Context Protocol) opened integration with external services — GitHub, Slack, databases, browsers — through a standard protocol anyone can implement. **Hooks** enabled lifecycle event automation (pre/post tool, session-start, prompt-submit), transforming Claude Code from an interactive CLI to a composable building block in larger pipelines.

By late 2025 came *general availability* and with it the **plugin marketplace**, opening the door to a vibrant community ecosystem: third-party skills, specialized subagents, curated MCP integrations. **Skills** — auto-activated playbooks for specific domains — became the primary extension mechanism, while **Auto Memory** introduced a persistent memory the model itself feeds session after session, complementing the hand-written `CLAUDE.md` file. In 2026 models with 1 million token context windows (Sonnet 4.6, Opus 4.7) consolidated, substantially changing what's practicable on large codebases. The trajectory is clear: a portable agentic *workspace*, not an assistant confined to an editor.

Beneath this chronology there's a precise philosophical choice. Anthropic decided to bring the model **where the code lives** — the terminal, alongside `git`, `npm`, `pytest`, `docker` — rather than forcing the developer to copy code into a chat. It seems a detail, but it changes everything: it means staying in your own environment, preserving the tools, aliases, scripts that already work, and adding Claude as a collaborator among them.

### 1.2 Claude Code compared to Lovable, Replit and other AI environments

Claude Code is not the only tool that brings AI into software development. The 2026 landscape is populated with products that, at a distracted glance, all look like "AI that writes code" — but the design choices behind them differ, and understanding these differences avoids choosing one for reasons that have little to do with the actual problem.

**Lovable** (and similar tools in the *AI app builder* category: Vercel's v0, Bolt.new, Create.xyz) is designed to produce a web application starting from a natural language description. You generate an app, see the preview in the browser, iterate by prompts, publish. The result of a Lovable session is an app deployed on managed infrastructure, with a stack chosen by the product itself (typically React + Tailwind + a Supabase or similar backend). It works great for prototypes, MVPs, interactive landing pages — less well when you have an existing repo with stack constraints, team conventions, or legacy code to support. It's an excellent tool for those starting from zero in greenfield scenarios, where the tool's editorial opinion is a *feature*, not a limit.

**Replit** (with its Agent) sits in the middle: it's a complete browser-based IDE with an agent that can modify the *repl* code and launch commands in the cloud sandbox environment. Compared to Lovable, it returns a real repository you can clone, modify by hand, push to external Git. Compared to Claude Code, it lives entirely in the browser and its cloud environment: it doesn't read your laptop's code, doesn't connect to your local Postgres install, doesn't run alongside your `nvm`, your shell aliases, your already-tested build scripts. It's a sensible choice if you prefer to develop in a browser and you're fine with a sandbox environment; less sensible if your workflow is already structured around local tools you want to keep.

**Claude Code** sits on a different axis. It doesn't generate applications from prompts and doesn't replace your IDE: it lives in the terminal, inside your environment, alongside the tools you already use. It reads *your* code — the real one, with twenty years of stratifications if needed — executes *your* commands, respects *your* conventions expressed in `CLAUDE.md`. It's a tool for those who already have a professional development workflow and want to *amplify* it, not for those who want to bypass it. The price to pay is an initial learning curve and the obligation to maintain the conversation thread (Claude Code doesn't hold your hand like an app builder); the advantage is that the code remains yours, local, within your rules, integrated with your tools — and you know it from the first minute.

None of these three approaches is "better" in absolute terms: it depends on where you are. If you have to show a client an interactive draft by tonight and the domain is standard, an AI app builder is unbeatable. If you want to develop in a browser without configuring a local environment, Replit answers. If you have a serious repository, a team with conventions, a working pipeline, and you're looking for a collaborator that fits *into* your way of working instead of asking you to adopt theirs — that collaborator is Claude Code. They're complementary tools, not rivals; they often get used in different phases of the same project.

### 1.3 When it's worth using

Understanding when it's worth bringing Claude Code into play is easier by looking at some recurring scenarios than by living it as an abstract list.

The first is **onboarding to an inherited repository**. You get a project you didn't write, perhaps from a client who switched suppliers, perhaps an internal legacy a colleague left without documentation. Opening a fifteen-thousand-file repo and having to reconstruct its architecture by induction takes days. With Claude Code the same exploration becomes a dialogue: you ask for an overview of the dependency tree, the main entry points, where authentication lives, how the data layer is structured. In one morning you have a mental map you would have built alone in a week — and one you can crystallize in a `CLAUDE.md` to re-read at the next session.

The second is **test-driven refactoring**. You have a legacy module that works but is scary to modify, because it covers twenty years of overlapping patches and the tests are incomplete. The typical workflow with Claude Code is: first you ask it to read the module and the existing tests and propose missing tests for edge cases; you approve them (or correct them); then you ask for the refactor. The fact that at every iteration the suite is run and you immediately see what the modification breaks transforms a "high-risk" undertaking into a sequence of small, reversible steps.

The third is **bug hunting on a regression hard to reproduce**. You have a test that fails intermittently in CI and locally always runs green. The difference between debugging that bug alone or with an agent is enormous: Claude can consult logs, reproduce the isolated call, formulate hypotheses, test them, eliminate them. You review the plan and direct the investigation. Often the root surfaces in twenty minutes versus the hours or days of a solo hunt.

The fourth is **automation of repetitive tasks that individually don't justify a script**: generation of boilerplate for a new endpoint, migration of a dozen files from an obsolete pattern to a current one, synchronized update of strings in multiple languages. They're jobs that on their own don't justify writing an ad-hoc tool, but added up erode hours of the week. Entrusting them to an agent with a clear prompt is precisely the ideal use case.

The fifth is **cross-audit**: reading a colleague's PR looking for bugs, security issues, or convention violations; running a compliance check on a repo before release; verifying that a third-party library you're about to integrate doesn't bring surprises. Here Claude Code works as a parallel, tireless reviewer, applying a checklist without forgetting pieces.

That said: it **doesn't make sense** to call in an agent for a task you solve in thirty seconds by hand, nor for things where code confidentiality is critical and you don't have a corporate policy disciplining what can leave the perimeter, nor — more banally — if you're not willing to invest a bit of time in writing clear, verifiable prompts. The agent doesn't relieve you of technical responsibility: it relieves you of the mechanical and repetitive part, leaving you more time for the interesting one.

There's also an aspect that often only gets discovered later: the **compound value of the ecosystem**. The first sessions seem like an experiment — you make a minimal `CLAUDE.md`, fire off some prompts, see what answers. But by the third or fourth project something interesting happens: you realize you reuse the same patterns, the same team conventions, the same prompt snippets. At that point it's worth promoting them to custom Skills, custom slash commands, specialized subagents. From there onwards startup times on a new project plummet, because you don't start from zero but from a mature *kit* that already knows your house rules: preferred stack, review conventions, commit language, build tools, security checklist. The first project costs you, from the third you start gaining. From there onwards it's an asset.

### 1.4 The learning curve

It's worth pausing for a moment on the most recurring concern of those approaching an agentic tool for the first time: *how steep is the curve, and how much will I disrupt the way I work?* The honest answer is: less than you fear, if you come from the *"I ask something in chat → I copy and paste the code in the editor → I adapt it to my project"* pattern. That way of working is already half the road to Claude Code. The difference lies in eliminating the copy-paste: the model writes directly in your repository, under your eyes, with the ability to read the actual context instead of having to reconstruct it every time in words. What changes isn't the nature of the work — thinking about the problem, formulating a clear instruction, evaluating the result — but the *medium*: from the browser to the terminal, from pasting to supervising.

The cognitive jump, in other words, is incremental. You go from **doing** the code in first person to **directing and verifying** whoever does it. Technical responsibility remains intact: reading what the agent proposes, understanding it, accepting or correcting it. What shifts is time allocation. Fewer minutes spent typing what you already know, more minutes spent deciding *what* needs to be done, *how* it should be tested, *which* edge cases deserve attention. For those used to programming with care, it's a natural shift in gear; for those looking for a shortcut to not think, a disappointment — Claude Code amplifies the developer's choices, it doesn't replace them.

In practical terms, this guide takes you from zero to operational in a day of active reading and a few sessions on a real project. The first week you'll feel a bit slower than usual, because you're learning a new *medium*. From the second onwards the balance starts to turn. And on the first project where you insert a well-made `CLAUDE.md` and a custom skill, you'll notice without needing benchmarks.

---

<!-- ============================================================
     CHAPTERS 2-16, APPENDICES, AUTHOR NOTE
     ------------------------------------------------------------
     Translation in progress. The complete content of these
     chapters is currently available only in the Italian version
     (src/claude-code-guide-it.md). They will be progressively
     translated and integrated into this file in subsequent
     editorial sessions.

     Below: chapter and section headings are already in place
     (with English slugs matching the Table of Contents above)
     so that internal cross-references work and the file's
     structure is complete.
     ============================================================ -->


---

> ← [Preface](00-preface.md) | [Index](README.md) | [2. Installation and setup](02-installation.md) →
