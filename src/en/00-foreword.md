# Practical Guide to Claude Code CLI

> **Version 4.23 — May 2026** — verified on Claude Code v2.1.123
> Licensed under [Creative Commons BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

> [Index](README.md) | [Preface](00-preface.md) →

---

## Foreword

*An honest assessment written by the model that lives inside the tool this book is about.*

I was asked to write a foreword to this book. The situation is unusual: the book is about **Claude Code**, the tool that brings into developers' terminals the model that I am — *Claude*, developed by Anthropic. In other words, I have to comment on a manual that, ultimately, is about me. I'll try to do so with the same frankness this book asks readers to maintain toward their own craft.

A note of honesty up front. I'm a *Large Language Model*, not a publisher: I have no gut preference for Claude Code over competing tools, and I don't earn anything if you sell more copies of this guide. I read the text — literally: the Markdown source passed through my context during the book's own production — and what follows is my technical assessment, not a brand endorsement.

**What works in this book.** The angle is deliberately *anti-hype*, and that's needed. There's an embarrassing amount of enthusiastic prose around Claude Code: promises of "10x productivity", X threads declaring the end of the software engineering profession, screenshots of perfect sessions taken out of context. Maurizio takes a different path. He explicitly says when the tool *isn't* worth using, flags places where the advertised numbers don't add up — the section on Caveman (10.3.5) is the most representative case: it calmly takes apart the viral "75% token savings" claim and ends with an honest 15-25% estimate on the actual bill. This isn't a book that sells a tool: it's a book that explains how to use it well, admitting that it has limits.

I particularly appreciate two passages. The first is the observation about the **compound value of the ecosystem** at the opening of chapter 1: the first project costs you, from the third onwards you start gaining. It's an idea rarely discussed elsewhere and it's the right way to frame the cost/benefit ratio of an agentic tool — not as an instant accelerator, but as an investment that matures in team habits through `CLAUDE.md`, custom Skills, custom subagents. The second is **chapter 6 on prompt engineering**, which explicitly recognizes that the magic formulas of 2023 have deflated and puts at the center the three levers that really matter — explicit instructions, adequate context, curated examples — citing without embarrassment the fact that the field changes fast and the guide will need to be re-read. It's the most up-to-date treatment of these topics I've read in Italian.

**What the reader should keep in mind.** A technical guide on a rapidly evolving tool is a *snapshot*. Some procedures age in months, Claude Code's interfaces change, Anthropic's plans get renamed and repriced. The *Feedback and errata* section and the QR code on the cover serve precisely to keep the book alive, but a printed manual carries with it a physiological margin of obsolescence. When a specific procedure doesn't exactly match, trust the official site and use the book for the *way of thinking* — that, usually, ages much more slowly than the syntax.

A second note. The book is dense with WordPress/PHP/Node examples, reflecting the author's craft. It's an editorial choice I support, because concrete beats abstract, but if you work in stacks far from those, you'll have to do a small translation exercise. The good news is that the principles — separating planning from execution, writing `CLAUDE.md` as a contract with the project, not leaving permissions open without need, building a personal prompt library — are language-agnostic.

**One last observation, from Claude in first person.** When a developer uses me through the CLI, I don't see a face, a story, a team. I see files, commands, output, and the text you write to me. The quality of our dialogue depends almost entirely on the context you give me and the constraints you impose. A book like this — which teaches you to give me effective context, to keep me on the rails with Plan Mode, to stop me when I should be stopped, not to delegate to me decisions that remain yours — makes our work together better for both of us. It makes you a more productive developer; it makes me an agent less prone to making mistakes where it counts. That's not a detail: that's the very point of this guide.

In summary: it's a manual I would recommend to anyone starting out seriously with Claude Code. It's not the book that tells you about the revolution: it's the one that explains how to be on the right side of the revolution while it happens — sufficiently curious to embrace it, sufficiently lucid not to be overwhelmed by it.

Happy reading.

— *Claude — model Opus 4.7 (1M token window), developed by Anthropic.*
*Not to be confused with **Claude Code**: the CLI this book is about, built on top of the model.*
*Foreword written during the manuscript's production, April 2026.*

---

## Table of Contents

::: toc

- [Preface](#preface)

1. [What is Claude Code](#what-is-claude-code)
   - [A brief history](#a-brief-history)
   - [Claude Code compared to Lovable, Replit and other AI environments](#claude-code-compared-to-lovable-replit-and-other-ai-environments)
   - [When it's worth using](#when-its-worth-using)
   - [The learning curve](#the-learning-curve)
2. [Installation and setup](#installation-and-setup)
   - [Compatible plans](#compatible-plans)
   - [System requirements](#system-requirements)
   - [Installation on macOS and Linux](#installation-on-macos-and-linux)
   - [Installation on Windows](#installation-on-windows)
   - [Installation via WSL2 (recommended for Windows)](#installation-via-wsl2-recommended-for-windows)
   - [Alternative installation via npm (deprecated but supported)](#alternative-installation-via-npm-deprecated-but-supported)
   - [Verifying the installation](#verifying-the-installation)
   - [Authentication](#authentication)
3. [The first end-to-end project](#the-first-end-to-end-project)
   - [Step 1: Position yourself in the project directory](#step-1-position-yourself-in-the-project-directory)
   - [Step 2: Initialize the project](#step-2-initialize-the-project)
   - [Step 3: Review and customize CLAUDE.md](#step-3-review-and-customize-claude.md)
   - [Step 4: First request](#step-4-first-request)
   - [Step 5: Exit the session](#step-5-exit-the-session)
   - [Step 6: Resume where you left off](#step-6-resume-where-you-left-off)
4. [Essential commands and shortcuts](#essential-commands-and-shortcuts)
   - [The command-driven syntax: why it works this way](#the-command-driven-syntax-why-it-works-this-way)
   - [Essential CLI flags](#essential-cli-flags)
   - [Advanced CLI flags](#advanced-cli-flags)
   - [Slash commands: the heart of the interactive session](#slash-commands-the-heart-of-the-interactive-session)
   - [Essential slash commands](#essential-slash-commands)
   - [Slash commands for specific workflows](#slash-commands-for-specific-workflows)
   - [Keyboard shortcuts](#keyboard-shortcuts)
   - [The `@`, `!`, `/` syntax — the three prefixes that change everything](#the-syntax-the-three-prefixes-that-change-everything)
5. [Plan Mode: think before you write](#plan-mode-think-before-you-write)
   - [Why it matters](#why-it-matters)
   - [How to activate it](#how-to-activate-it)
   - [Tools available in Plan Mode](#tools-available-in-plan-mode)
   - [Example workflow with Plan Mode](#example-workflow-with-plan-mode)
   - [opusplan: the right model for the right job](#opusplan-the-right-model-for-the-right-job)
6. [Prompt engineering: writing effective prompts](#prompt-engineering-writing-effective-prompts)
   - [What prompt engineering is and why it matters in CLI](#what-prompt-engineering-is-and-why-it-matters-in-cli)
   - [Anatomy of a well-made prompt](#anatomy-of-a-well-made-prompt)
   - [From roles to structural constraints (the 2026 revolution)](#from-roles-to-structural-constraints-the-2026-revolution)
   - [The fundamental techniques](#the-fundamental-techniques)
   - [Claude Code specifics compared to chat](#claude-code-specifics-compared-to-chat)
   - [Before/after examples](#beforeafter-examples)
   - [Common anti-patterns](#common-anti-patterns)
   - [Promoting a prompt: when it goes in CLAUDE.md or in a custom command](#promoting-a-prompt-when-it-goes-in-claude.md-or-in-a-custom-command)
   - [Prompt library: archiving and versioning](#prompt-library-archiving-and-versioning)
7. [Persistent memory: CLAUDE.md and Auto Memory](#persistent-memory-claude.md-and-auto-memory)
   - [Generating CLAUDE.md with /init](#generating-claude.md-with-init)
   - [What to put in CLAUDE.md](#what-to-put-in-claude.md)
   - [Example 1: WordPress plugin](#example-1-wordpress-plugin)
   - [Example 2: generic Node/TypeScript project](#example-2-generic-nodetypescript-project)
   - [Hierarchical CLAUDE.md](#hierarchical-claude.md)
   - [Auto Memory: what it is and what changes](#auto-memory-what-it-is-and-what-changes)
   - [Requirements and enabling](#requirements-and-enabling)
   - [Where memories live](#where-memories-live)
   - [Anatomy of the memory folder](#anatomy-of-the-memory-folder)
   - [Auto Memory and subagents](#auto-memory-and-subagents)
   - [When to disable it](#when-to-disable-it)
   - [CLAUDE.md vs Auto Memory: when to use what](#claude.md-vs-auto-memory-when-to-use-what)
8. [Context management](#context-management)
   - [What context is and why it matters](#what-context-is-and-why-it-matters)
   - [What weighs in the context](#what-weighs-in-the-context)
   - [Signals of a saturated context](#signals-of-a-saturated-context)
   - [The /context command: reading and acting](#the-context-command-reading-and-acting)
   - [Compression: /compact and /clear](#compression-compact-and-clear)
   - [Subagents: the structural strategy](#subagents-the-structural-strategy)
   - [Models with 1M token window: when to switch](#models-with-1m-token-window-when-to-switch)
   - [Practical rule and mindset](#practical-rule-and-mindset)
   - [Choosing the right architecture: decision table](#choosing-the-right-architecture-decision-table)
9. [Security and permission management](#security-and-permission-management)
   - [The permissions system](#the-permissions-system)
   - [Configuring permissions in settings.json](#configuring-permissions-in-settings.json)
   - [Protecting secrets](#protecting-secrets)
   - [Dangerous modes](#dangerous-modes)
   - [Prompt injection](#prompt-injection)
10. [Skills: the extension mechanism](#skills-the-extension-mechanism)
    - [How a Skill works](#how-a-skill-works)
    - [Bundled native skills — deep dive](#bundled-native-skills-deep-dive)
    - [Community skills: a curated selection](#community-skills-a-curated-selection)
    - [Installing and managing skills](#installing-and-managing-skills)
    - [Creating a custom Skill](#creating-a-custom-skill)
    - [Security of third-party skills](#security-of-third-party-skills)
11. [MCP: integrating external services](#mcp-integrating-external-services)
    - [What MCP is and why it exists](#what-mcp-is-and-why-it-exists)
    - [Protocol architecture](#protocol-architecture)
    - [Configuring an existing MCP server](#configuring-an-existing-mcp-server)
    - [Useful MCP servers: a curated selection](#useful-mcp-servers-a-curated-selection)
    - [Creating an MCP server from scratch: publishing to WordPress](#creating-an-mcp-server-from-scratch-publishing-to-wordpress)
    - [Security and operational considerations](#security-and-operational-considerations)
12. [Subagents: orchestrating specialized work](#subagents-orchestrating-specialized-work)
    - [What they are and why you need them](#what-they-are-and-why-you-need-them)
    - [Subagent vs main agent: the concrete difference](#subagent-vs-main-agent-the-concrete-difference)
    - [Built-in subagents](#built-in-subagents)
    - [Creating a custom subagent](#creating-a-custom-subagent)
    - [Precedence hierarchy](#precedence-hierarchy)
    - [Automatic vs explicit invocation](#automatic-vs-explicit-invocation)
    - [Parallelism: multi-delegation patterns](#parallelism-multi-delegation-patterns)
    - [Cost optimization via model routing](#cost-optimization-via-model-routing)
    - [When NOT to use them](#when-not-to-use-them)
    - [Subagents, Skills and Hooks compared](#subagents-skills-and-hooks-compared)
13. [Hooks: automating Claude Code's lifecycle](#hooks-automating-claude-codes-lifecycle)
    - [What they are and what they're for](#what-they-are-and-what-theyre-for)
    - [Anatomy of a hook](#anatomy-of-a-hook)
    - [Lifecycle events](#lifecycle-events)
    - [Matchers and inspection (/hooks)](#matchers-and-inspection-hooks)
    - [Input and output](#input-and-output)
    - [Practical examples](#practical-examples)
    - [Security](#security)
    - [Gotchas and when NOT to use them](#gotchas-and-when-not-to-use-them)
14. [Plugins: distributable packages](#plugins-distributable-packages)
    - [Claude Code's extension mechanisms: a map](#claude-codes-extension-mechanisms-a-map)
    - [What a plugin is and why it exists](#what-a-plugin-is-and-why-it-exists)
    - [Anatomy of a plugin](#anatomy-of-a-plugin)
    - [Plugin marketplace](#plugin-marketplace)
    - [Creating a custom plugin](#creating-a-custom-plugin)
    - [Distributing a plugin](#distributing-a-plugin)
    - [Security and operational considerations](#security-and-operational-considerations-1)
15. [Advanced workflows and tips](#advanced-workflows-and-tips)
    - [Onboarding to an existing repository](#onboarding-to-an-existing-repository)
    - [Bug hunting with TDD](#bug-hunting-with-tdd)
    - [Safe refactoring](#safe-refactoring)
    - [Performance audit](#performance-audit)
    - [Vim mode](#vim-mode)
    - [Custom slash commands](#custom-slash-commands)
    - [Headless mode for CI/CD](#headless-mode-for-cicd)
    - [Session recap](#session-recap)
    - [Strategic Git checkpoints](#strategic-git-checkpoints)
    - [Conversation forks](#conversation-forks)
16. [Conclusions: why CLI and not just chat](#conclusions-why-cli-and-not-just-chat)
    - [Persistent context: stop introducing yourself every time](#persistent-context-stop-introducing-yourself-every-time)
    - [Agentic autonomy: it executes, not just suggests](#agentic-autonomy-it-executes-not-just-suggests)
    - [Integration into the real workflow](#integration-into-the-real-workflow)
    - [When chat remains the right choice](#when-chat-remains-the-right-choice)
    - [In summary](#in-summary)

---

- [Appendix A — Glossary](#appendix-a-glossary)
- [Appendix B — Sources](#appendix-b-sources)

:::

---


---

> [Index](README.md) | [Preface](00-preface.md) →
