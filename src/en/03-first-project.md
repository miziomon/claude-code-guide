# Practical Guide to Claude Code CLI

> **Version 4.30 — May 2026** — verified on Claude Code v2.1.123
> Licensed under [Creative Commons BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

> ← [2. Installation and setup](02-installation.md) | [Index](README.md) | [4. Essential commands and shortcuts](04-commands.md) →

---

## 3. The first end-to-end project

Let's see a complete flow starting from zero. Suppose we have a WordPress plugin to analyze.

### 3.1 Step 1: Position yourself in the project directory

```bash
cd ~/mavida/wp-access-control-block
```

> Claude Code **always** uses the current directory as the working context. Don't launch `claude` from the home directory if you want to work on a specific project.

### 3.2 Step 2: Initialize the project

```bash
claude
```

Once inside the interactive session, run:

```
/init
```

This command analyzes the project structure and automatically generates a `CLAUDE.md` file in the root. The file contains:

- Project overview (detected technology stack)
- Main architecture
- Detected build/test commands (from `package.json`, `composer.json`, etc.)
- Code conventions

### 3.3 Step 3: Review and customize CLAUDE.md

The auto-generated file is a starting point. Open it and enrich it with project-specific information (see [section 7](#persistent-memory-claude.md-and-auto-memory) for detailed examples).

### 3.4 Step 4: First request

Return to the Claude session and write your first prompt:

```
Analyze the plugin structure and explain to me:
1. How the code is organized (namespaces, patterns)
2. How the Gutenberg block is registered
3. Where access controls are managed
Don't modify anything, just explore and report.
```

Claude will read the relevant files, produce an analysis, and stop waiting for further instructions.

### 3.5 Step 5: Exit the session

```
/exit
```

Or `Ctrl+D`.

### 3.6 Step 6: Resume where you left off

When you return to the project:

```bash
cd ~/mavida/wp-access-control-block
claude --continue
```

The `--continue` flag loads the most recent session in this directory. Alternatively, `claude --resume` shows a list of past sessions to choose from.

---


---

> ← [2. Installation and setup](02-installation.md) | [Index](README.md) | [4. Essential commands and shortcuts](04-commands.md) →
