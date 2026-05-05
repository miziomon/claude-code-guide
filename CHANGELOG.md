# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

---

## [4.30.0] — 2026-05-05

### Added

- New working example: `src/examples/wordpress-publisher-mcp/` — a complete Python MCP server publishing to WordPress via the REST API, accompanying chapter 11.5
- Documentation of the `examples/` folder in the root README with example table

### Changed

- Bump guide version from 4.23 to 4.30 across all sources, split chapter files, and READMEs
- Re-split English and Italian chapter files from updated sources
- Rename chapter 9: "Security and permission management" → "Security, permissions, and guardrails" (EN) / "Sicurezza e gestione dei permessi" → "Sicurezza, permessi e guardrail" (IT)
- New PDF builds: `output/claude-code-guide-{en,it}-{17x24,a4}-v4.30.pdf`

---

## [4.23.2] — 2026-05-03

### Changed

- Expand root `README.md`: add chapter table with descriptions, repository structure diagram, expanded About section, and Why this guide section drawn from the Preface

---

## [4.23.1] — 2026-05-03

### Added

- Split both English and Italian guides into per-chapter Markdown files under `src/en/` and `src/it/`
- Navigable index (`README.md`) for each language with a full table of contents
- Navigation header on every chapter file (← prev | Index | next →)
- `README.md` at repository root with project overview and links to both language versions
- `CHANGELOG.md` (this file)
- `.gitignore` for OS and editor artefacts
- `LICENSE` (MIT, added by GitHub at repo creation)

---

## [4.23.0] — 2026-05-03

### Added

- Initial repository setup
- Full guide source in English: `src/claude-code-guide-en.md`
- Full guide source in Italian: `src/claude-code-guide-it.md`
- Pre-built PDFs (17×24 cm format): `output/Claude_Code_Guide_17x24.pdf`, `output/Guida_Claude_Code_17x24.pdf`
- Cover and logo assets: `src/assets/`

---

[Unreleased]: https://github.com/miziomon/claude-code-guide/compare/v4.30.0...HEAD
[4.30.0]: https://github.com/miziomon/claude-code-guide/compare/v4.23.2...v4.30.0
[4.23.2]: https://github.com/miziomon/claude-code-guide/compare/v4.23.1...v4.23.2
[4.23.1]: https://github.com/miziomon/claude-code-guide/compare/v4.23.0...v4.23.1
[4.23.0]: https://github.com/miziomon/claude-code-guide/releases/tag/v4.23.0
