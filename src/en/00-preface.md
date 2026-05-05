# Practical Guide to Claude Code CLI

> **Version 4.30 — May 2026** — verified on Claude Code v2.1.123
> Licensed under [Creative Commons BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

> ← [Foreword](00-foreword.md) | [Index](README.md) | [1. What is Claude Code](01-what-is-claude-code.md) →

---

## Preface

*A guide for those who want to start using Claude Code professionally.*

This guide is a practical introduction to **Claude Code**, the agentic CLI from Anthropic that brings the Claude model directly into the terminal as an operational collaborator capable of reading code, executing commands, modifying files, and managing complete workflows.

The document is intended for **developers who want to start using Claude Code professionally**, without relying on word of mouth or fragmented tutorials. You'll find here the complete journey from installation to advanced workflows, with concrete examples drawn from WordPress/PHP scenarios and generic Node/TypeScript projects.

### Why this guide

In recent months I've come across plenty of content on Claude Code, and at some point I recognized two recurring categories.

The first are the **video tutorials** that explain what the tool is and stop there. Useful for the first ten minutes, then you realize you've watched a trailer: you've seen what Claude Code can do in the abstract, but you don't yet know how to actually use it on your own project.

The second are the **email-exchange guides**: the social media post *"I've prepared the definitive guide, leave me a comment and I'll send it"*, the classic funnel comment → DM → landing page → form → newsletter (with attached spam). Sometimes the PDF at the end of the funnel is even well done, but the price you pay in attention and privacy is disproportionate to the value.

At some point I stopped and thought something fairly obvious:

> *I'm using every day a tool that exists precisely to produce complex work in short timeframes.*
> *Why don't I use it to write the well-made guide I would have liked to read and didn't find?*

What you have in front of you is the result. Everything verified against Anthropic's official documentation — zero invented flags, zero fantasy skills fished from unchecked Reddit threads. No DM to write, no email to leave, no newsletter to subscribe to receive it. It's a PDF released under a **Creative Commons BY-SA 4.0** license: download it, read it, print it, pass it to colleagues if you find it useful.

Precisely because it's an open and living document, reader feedback is part of the process: you'll find contacts for errata and suggestions in the [Feedback and errata](#feedback-and-errata) section below, or you can scan the QR code on the cover to reach the official guide page.

### Who it's for

- Web developers (PHP, JavaScript, Python) familiar with the terminal and Git
- Professionals who want to integrate AI into their daily workflow consciously
- Technical teams evaluating the adoption of agentic AI tools in development processes
- Participants in Mavida workshops on *vibe coding* (development guided by structured prompts rather than manual code writing) and AI-assisted development

### What you'll find

The first six chapters cover the basics: what Claude Code does, how to install it, how to structure your first project, essential commands, Plan Mode, and prompt engineering principles. Chapters 7-14 dive into the mechanisms that make the difference between casual and professional use: persistent memory with `CLAUDE.md`, context management, security, Skills, plugins, MCP, subagents, and hooks. The final chapters present practical workflows, advanced tips, and an honest reflection on when the CLI surpasses the chat and when it's better to stay in the browser.

### What you won't find

This isn't an exhaustive reference: for that there's the official documentation (linked in Appendix B). The goal is to put the reader in a position to work productively in one or two days, knowing where to dig deeper when needed. You also won't find hype about AI's capabilities: the tone is technical, honest about limits, and attentive to real risks (security, prompt injection, hidden token costs).

### How to read it

If you're a beginner, read in sequence at least up to chapter 7 (CLAUDE.md). If you've already installed Claude Code and are looking for specific best practices, use the index as a thematic reference. At the end you'll find a glossary of recurring terms (Appendix A) and the official sources for verifications and deeper dives (Appendix B).

### How this guide was written

This guide is meta-circular: it was written using Claude Code itself. The source is a single Markdown file (`claude-code-guide-it.md`); a Python build pipeline converts it to two PDF formats — A4 for office printing, 17×24 cm for the book version — through **Pandoc** and **WeasyPrint**, in a single command `python scripts/build_pdf.py`.

Each chapter was discussed, written, and refined in Claude Code sessions, with the model re-reading the entire document to maintain coherence between chapters, checking cross-references, and updating `CHANGELOG.md` at every release. When an editorial choice required discussion — a title, the position of a section, the tone of a passage — I used Plan Mode to align before touching the file. Versioning followed a SemVer-like semantic (minor increments for new chapters or sections, patches for editorial fixes), tracked carefully in the repository's `CHANGELOG.md`.

The human part remains entirely: the original idea, editorial cuts, voice, final review, decisions on tone. What Claude Code took away is the mechanical fatigue of keeping a document in evolution synchronized across multiple dimensions — content, structure, cross-references, build — leaving me more time for what counts, which is writing well. It's exactly the kind of workflow this guide describes in the rest of the pages.

### Feedback and errata

This guide is a living document: despite care in verification, errors, inaccuracies, or omissions are always possible — and Claude Code itself evolves rapidly. **If you find a typo, an example that doesn't work, an outdated procedure, or a topic that deserves deeper treatment, report it.** Reports will be collected and integrated into future versions, with acknowledgment to contributors in release notes.

You can send feedback by writing to **[maurizio@mavida.com](mailto:maurizio@mavida.com)** indicating, where possible, the chapter and section of reference. The official guide page — with any updates, errata, and subsequent versions — is reachable at **[maurizio.mavida.com/guida-claude-code](https://maurizio.mavida.com/guida-claude-code/)** or via the QR code on the cover. Any report — even a minimal one — is welcome and contributes to improving the work for those who read the guide after you.

---


---

> ← [Foreword](00-foreword.md) | [Index](README.md) | [1. What is Claude Code](01-what-is-claude-code.md) →
