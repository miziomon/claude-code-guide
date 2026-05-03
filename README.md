# Claude Code — Practical Guide

> **Version 4.23 — May 2026** · Verified on Claude Code v2.1.123
> Licensed under [Creative Commons BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

A hands-on, honest guide to **Claude Code CLI** — covering everything from first installation to advanced agentic workflows, written by a developer who uses the tool daily and with the tool itself.

Read online: **[English](src/en/README.md)** · **[Italiano](src/it/README.md)**

---

## Why this guide exists

There is no shortage of content about Claude Code. What is harder to find is content that goes past the trailer. Most video tutorials show what the tool *can do* in the abstract; most social-media "guides" sit behind a funnel of comments, DMs, and newsletter subscriptions.

At some point the obvious thought arrived: *I use every day a tool that exists precisely to produce complex work in short timeframes — why not use it to write the guide I would have liked to read and didn't find?*

The result is what you are reading now. Everything here is verified against Anthropic's official documentation — no invented flags, no fantasy features fished from unchecked Reddit threads. No email to leave, no newsletter to subscribe to. Just a guide released under a Creative Commons license: download it, read it, pass it to colleagues.

---

## Who it's for

- Web developers (PHP, JavaScript, Python) comfortable with the terminal and Git
- Professionals who want to integrate AI into their daily workflow **consciously**, not just experimentally
- Technical teams evaluating agentic AI tools for their development processes
- Anyone who has tried Claude Code and wants to move from "it sometimes works" to "I know what I'm doing"

---

## Contents

Both language editions share the same 16-chapter structure plus appendices.

| # | Chapter | What you'll learn |
|---|---------|-------------------|
| — | [Foreword](src/en/00-foreword.md) | An honest assessment by the model this book is about |
| — | [Preface](src/en/00-preface.md) | Why this guide exists, who it's for, how it was written |
| 1 | [What is Claude Code](src/en/01-what-is-claude-code.md) | Architecture, the agentic loop, and how it differs from IDE assistants |
| 2 | [Installation and setup](src/en/02-installation.md) | First run, authentication, IDE integrations, global config |
| 3 | [The first end-to-end project](src/en/03-first-project.md) | A real project from scratch — the full workflow in practice |
| 4 | [Essential commands and shortcuts](src/en/04-commands.md) | The commands and keyboard shortcuts you'll use every day |
| 5 | [Plan Mode](src/en/05-plan-mode.md) | How to make Claude think before it writes — and why that matters |
| 6 | [Prompt engineering](src/en/06-prompt-engineering.md) | Writing effective prompts for agentic tools: context, examples, constraints |
| 7 | [Persistent memory](src/en/07-memory.md) | CLAUDE.md, Auto Memory, and how to give Claude a stable project context |
| 8 | [Context management](src/en/08-context.md) | Keeping the context window clean and costs under control |
| 9 | [Security and permissions](src/en/09-security.md) | The permission model, safe operation, and what can go wrong |
| 10 | [Skills](src/en/10-skills.md) | The extension mechanism — installing, writing, and composing Skills |
| 11 | [MCP](src/en/11-mcp.md) | Integrating external services via the Model Context Protocol |
| 12 | [Subagents](src/en/12-subagents.md) | Orchestrating specialized parallel work with the Agent tool |
| 13 | [Hooks](src/en/13-hooks.md) | Automating Claude Code's lifecycle with pre/post-tool shell hooks |
| 14 | [Plugins](src/en/14-plugins.md) | Packaging and distributing Skills and hooks as reusable plugins |
| 15 | [Advanced workflows](src/en/15-advanced-workflows.md) | Patterns, tips, and hard-won lessons from real projects |
| 16 | [Conclusions](src/en/16-conclusions.md) | When the CLI beats the chat — and when it doesn't |
| A | [Glossary](src/en/appendix-a-glossary.md) | Key terms and definitions |
| B | [Sources](src/en/appendix-b-sources.md) | Official Anthropic documentation and verified references |

> The first six chapters cover the basics. Chapters 7–14 cover the mechanisms that separate casual use from professional use. The rest is context, judgment, and reflection.

---

## Repository structure

```
claude-code-guide/
├── src/
│   ├── en/                    ← English guide, split by chapter
│   │   ├── README.md          ← Navigable index (EN)
│   │   ├── 00-foreword.md
│   │   ├── 01-what-is-claude-code.md
│   │   └── … (21 files total)
│   ├── it/                    ← Italian guide, split by chapter
│   │   ├── README.md          ← Indice navigabile (IT)
│   │   └── … (21 files total)
│   ├── claude-code-guide-en.md  ← Full source (single file, EN)
│   ├── claude-code-guide-it.md  ← Full source (single file, IT)
│   └── assets/
├── output/
│   ├── Claude_Code_Guide_17x24.pdf
│   └── Guida_Claude_Code_17x24.pdf
├── CHANGELOG.md
└── LICENSE
```

---

## About the author

**Maurizio Pelizzone** is a senior web developer with 20+ years of experience in PHP and a daily user of Claude Code since its early releases. He runs **[Mavida](https://maurizio.mavida.com)**, where he teaches structured AI-assisted development workflows — what he calls *vibe coding*: development guided by deliberate prompts rather than manual line-by-line writing.

This guide is meta-circular: it was written *using* Claude Code. The source is a single Markdown file processed through a Pandoc + WeasyPrint pipeline into the PDFs you find in `output/`. Each chapter was drafted and refined in Claude Code sessions, with the model maintaining coherence across sections, checking cross-references, and updating the changelog at every release. The human part — the original idea, editorial cuts, voice, final decisions — remains entirely the author's.

---

## Pre-built PDFs

Ready-to-read PDFs in 17×24 cm book format are available in [output/](output/).

---

## License

Released under **[Creative Commons BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)** (attribution — share alike).
Share it, adapt it, pass it to colleagues — as long as you credit the source and keep the same license.

---

## Feedback & Errata

This is a living document. Claude Code evolves fast, and errors are possible.
If you find a typo, a broken example, or an outdated procedure — **open an issue** or write to [maurizio@mavida.com](mailto:maurizio@mavida.com).
Every report is welcome and credited in the release notes.
