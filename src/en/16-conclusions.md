# Practical Guide to Claude Code CLI

> **Version 4.30 — May 2026** — verified on Claude Code v2.1.123
> Licensed under [Creative Commons BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

> ← [15. Advanced workflows](15-advanced-workflows.md) | [Index](README.md) | [Appendix A — Glossary](appendix-a-glossary.md) →

---

## 16. Conclusions: why CLI and not just chat

After tackling installation, commands, Plan Mode, CLAUDE.md, Skills, and everything else, a legitimate question remains worth making explicit: *why use Claude Code CLI when I can simply paste code into a browser chat?*

Chat remains a perfectly valid tool, and indeed in some scenarios it's the most effective choice. But three differences make the CLI a qualitatively different tool, not just a variant of the channel.

### 16.1 Persistent context: stop introducing yourself every time

In traditional chat, every new session starts from zero. The model knows nothing about your project: naming conventions, stack, hard rules, build commands. Every time you have to re-explain, or hope Claude guesses from the code you paste.

With CLI, **`CLAUDE.md` is a permanent contract**. It's automatically read at every session, it's hierarchical (global user, monorepo, project), and you can regenerate it with `/init` every time the project evolves. The `--continue` and `--resume` commands let you resume conversations interrupted days before in the same context state.

This changes the way you think about your development environment: instead of mentally reconfiguring AI at every opening, you configure once and work. The same logic as `.editorconfig`, `.eslintrc`, `.gitignore` files that consolidate project rules once for all.

### 16.2 Agentic autonomy: it executes, not just suggests

In chat, Claude produces text. You're the human bridge: you copy the code into the editor, save, open the terminal, run the test, read the error, return to chat, paste the error, wait for the correction, copy the correction, paste into the editor, and so on. Every step is an interruption of the flow.

In CLI, Claude **is** the terminal. It reads files, executes commands, sees errors, makes commits, opens PRs, queries databases via MCP, navigates folders, runs tests. The "write → test → fix" cycle becomes a continuous conversation without leaving the tool:

```
You:     "The auth/login.test.js test fails. Figure out why and fix it."

Claude:  [reads the test]
         [reads the code under test]
         [runs npm test -- auth/login.test.js]
         [analyzes the output]
         [identifies the bug]
         [modifies the code]
         [re-runs the test]
         [all green]
         "Fixed. The problem was in token expiry handling.
          I modified validateToken() at lines 34-38."
```

This autonomy has a flip side — that's why there are entire chapters on security and Plan Mode — but when well managed it multiplies productivity in a non-linear way. You don't do something faster: you do things you simply wouldn't do in chat because the cost of manual orchestration is too high.

### 16.3 Integration into the real workflow

Professional development isn't just writing code: it's git, test suite, linting, CI/CD, code review, dependencies, environments. Chat lives **alongside** this workflow; CLI lives **inside** it.

**Native git.** Claude Code makes commits, opens branches, resolves merge conflicts, writes Conventional Commits commit messages, manages stash. You don't explain the diff to it: it reads it directly from `git diff`.

**Test and lint in loop.** The CLI runs the test suite, reads linter errors, retries until it passes. There's no copy-paste between windows, no "wait while I send you the output".

**Headless CI/CD.** The `-p` flag turns Claude into a pipeline tool:

```bash
claude -p "Review the changes in this PR and flag any security issues" \
       --output-format json > review.json
```

Insert this step in a GitHub Actions workflow and you have automatic AI code review on every push. Try doing the same with a browser chat.

### 16.4 When chat remains the right choice

For honesty: there are cases when opening chat.anthropic.com is the better move:

- **Conceptual brainstorming** without specific code — "What patterns can I use to implement a feature flag system?"
- **Learning a new framework** — you need pedagogy, not execution
- **Abstract architectural questions** — "Is it worth introducing CQRS in this context?"
- **Review of single snippets** from code you don't have locally
- **Discussions with Claude on non-coding topics** — writing, document analysis, planning

Practical rule: if the answer is **"code to integrate into my project"**, use the CLI. If the answer is **"an idea, a principle, an explanation"**, chat is enough.

### 16.5 In summary

Claude Code CLI isn't "Claude-in-chat with a different interface". It's an agentic tool that transforms a linguistic assistant into an **operational junior colleague**: it can do things, not just suggest them. For those who develop professionally, the difference is the same as between having a consultant who sends emails and having an intern at the next desk. Both useful, different contexts.

My advice, if you're starting out: install Claude Code, try a small and non-critical project, write a decent `CLAUDE.md`, always use Plan Mode for non-trivial tasks, and after a week evaluate. The curve is steep the first two days, then it flattens out.

---


---

> ← [15. Advanced workflows](15-advanced-workflows.md) | [Index](README.md) | [Appendix A — Glossary](appendix-a-glossary.md) →
