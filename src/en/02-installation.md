# Practical Guide to Claude Code CLI

> **Version 4.23 — May 2026** — verified on Claude Code v2.1.123
> Licensed under [Creative Commons BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

> ← [1. What is Claude Code](01-what-is-claude-code.md) | [Index](README.md) | [3. The first end-to-end project](03-first-project.md) →

---

## 2. Installation and setup

### 2.1 Compatible plans

Claude Code is **not included in the free plan**. You need one of the following:

| Plan | Cost (indicative) | Suited for |
|-------|-------------------|--------------|
| **Claude Pro** | $20/month | Moderate individual use, freelance developers |
| **Claude Max 5x** | $100/month | Intensive use, extended access to Opus |
| **Claude Max 20x** | $200/month | Near-autonomous workflow, multi-agent sessions |
| **Teams / Enterprise** | Custom | Organizations with compliance needs |
| **API (Anthropic Console)** | Pay-per-token | CI/CD, automations, sporadic use |

> **Note**: API pay-per-token pricing depends on the model. Sonnet 4.6 is priced at $3 per million input tokens and $15 per million output tokens (indicative figures, always verify on the Anthropic website).

### 2.2 System requirements

- **macOS**: 13.0 (Ventura) or higher
- **Linux**: Ubuntu 20.04+, Debian 10+, or equivalent distributions
- **Windows**: Windows 10 (1809+) or Windows 11, native with Git for Windows or via WSL2 (recommended)
- **RAM**: minimum 4 GB, 8 GB recommended for extensive codebases
- **Shell**: Bash, Zsh, PowerShell or CMD
- **Internet connection**: always required (the model runs on Anthropic servers)

In 2025 Anthropic introduced the **native installer** as the recommended method, replacing the npm installation (which remains supported but deprecated). The native installer has three advantages:

1. No Node.js dependency
2. Automatic background auto-update
3. None of the typical permission issues of `npm install -g`

The sections below cover installation on each platform.

### 2.3 Installation on macOS and Linux

Open the terminal and run:

```bash
# Download and execute the official installation script
curl -fsSL https://claude.ai/install.sh | bash
```

**What this command does, step by step:**

1. `curl` downloads the script from Anthropic's URL
2. `-fsSL` is four flags combined:
   - `-f` makes curl fail on HTTP errors (avoids executing error pages)
   - `-s` silent mode (no progress bar)
   - `-S` still shows errors if something goes wrong
   - `-L` follows HTTP redirects
3. The pipe `|` passes the downloaded script directly to `bash` for execution
4. The script downloads the right binary for your platform, places it in `~/.local/bin`, and configures auto-update

> **Security note**: executing scripts downloaded from the internet via pipe is a practice that should be evaluated. If you work in enterprise contexts, download the script first, inspect it, and then execute it separately.

### 2.4 Installation on Windows

Open **PowerShell** (not CMD) and run:

```powershell
# Download and execute the official PowerShell script
irm https://claude.ai/install.ps1 | iex
```

**How it works:**

- `irm` is the alias for `Invoke-RestMethod`: downloads the URL content
- `iex` is the alias for `Invoke-Expression`: executes the downloaded content as a PowerShell script

> **If you see the error** `'irm' is not recognized`, you're in CMD instead of PowerShell. The PowerShell prompt shows `PS C:\>`, while CMD shows only `C:\>`.

**Native installation on Windows requires Git for Windows**. Install it first if you don't have it.

### 2.5 Installation via WSL2 (recommended for Windows)

For Unix-like projects, WSL2 offers a cleaner and more compatible environment:

```powershell
# Install WSL2 (requires reboot)
wsl --install
```

After reboot, open Ubuntu (installed by default) and use the Linux command:

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

### 2.6 Alternative installation via npm (deprecated but supported)

If you have specific reasons to use npm (example: version pinning, environments where npm is the standard):

```bash
# Requires Node.js 18 or higher
npm install -g @anthropic-ai/claude-code
```

> **Don't use `sudo`**. If you get permission errors, the correct solution is to use `nvm` (Node Version Manager), which installs Node in your home directory, avoiding the problem at the root.

### 2.7 Verifying the installation

After installation, verify everything works:

```bash
# Check the installed version
claude --version

# Complete diagnostics: auth, PATH, MCP, file permissions
claude doctor
```

The `claude doctor` command is your best friend when something doesn't work: it runs a series of checks and tells you exactly what to fix.

### 2.8 Authentication

On first launch, `claude` opens the browser for OAuth:

```bash
cd ~/my-project
claude
```

Login with your Anthropic account (the one with the Pro/Max plan). The session is saved and persists across terminal restarts.

**For headless environments** (CI/CD, servers), use the API key:

```bash
# Add to ~/.zshrc, ~/.bashrc or ~/.profile
export ANTHROPIC_API_KEY="sk-ant-api03-..."
```

---


---

> ← [1. What is Claude Code](01-what-is-claude-code.md) | [Index](README.md) | [3. The first end-to-end project](03-first-project.md) →
