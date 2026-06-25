# Changelog

All notable changes to AI Creator are documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [0.7.1] — 2026-06-26

Open Source Polish release. No functional changes.

### Added
- `LICENSE` — MIT
- `CHANGELOG.md` — full release history
- `CONTRIBUTING.md` — contributor guide
- `SECURITY.md` — vulnerability reporting policy
- `CODE_OF_CONDUCT.md` — community standards
- `.github/ISSUE_TEMPLATE/bug_report.md` — bug report template
- `.github/ISSUE_TEMPLATE/feature_request.md` — feature request template
- `.github/PULL_REQUEST_TEMPLATE.md` — PR checklist template
- `.github/dependabot.yml` — automated dependency updates (pip + Actions)
- `.editorconfig` — consistent editor settings across environments

### Changed
- `README.md` — license badge, Table of Contents, Quick Start section,
  Contributing and License sections, updated Project Structure
- `docs/README_RU.md` — Contributing and License sections added
- `docs/REVIEW_NOTES.md` — v0.7.1 section added

---

## [0.7] — 2026-06-26

Production hardening release. VPS-ready.

### Added
- `docs/DEPLOYMENT.md` — full Ubuntu VPS deployment guide (Docker install,
  .env setup, first launch, logs, update, backup, troubleshooting)
- `pytest.ini` — `addopts = --basetemp=pytest_tmp` (fixes Windows temp dir)
- `HEALTHCHECK` in `Dockerfile` — verifies Python environment every 60 s

### Changed
- `Dockerfile` — non-root user (`botuser`), `pip upgrade`, optimized layer order
- `docker-compose.yml` — named volume for `generated_projects/` (solves
  non-root write permissions), `json-file` log rotation (10 MB × 3 files)
- `requirements.txt` — all 29 runtime deps pinned to exact versions
- `requirements-dev.txt` — all dev deps pinned
- `.gitignore` — added `pytest_tmp/` and `*.pyc`
- `CLAUDE.md` — updated test count (129 → 151) and module count (12 → 13)
- `README.md` / `README_RU.md` — status v0.7, updated Limitations and Roadmap,
  link to `docs/DEPLOYMENT.md`
- `docs/REVIEW_NOTES.md` — v0.7 section added

---

## [0.6] — 2026-06-24 / 2026-06-25

Domain-aware generation and interactive interview release.

### Added
- Interactive interview flow — bot asks up to 5 domain-specific questions in chat
- `domain_packs.py` — Domain Pack system with 7 packs (Zabbix, Jira, Logistics,
  Document Automation, Knowledge Assistant, Trading, Generic)
- `assistant_architect.py` — assistant architecture design layer
- `agent_blueprint.py` — Agent Blueprint builder (full product specification)
- Trading Assistant domain pack — TradingView webhook, prop firm risk tracking,
  RR/winrate statistics, economic calendar reminders
- `path_safety.py` — single source of path traversal protection
- `GenerationCooldown` in `runtime_guards.py`
- Full pipeline timeout (`GENERATION_PIPELINE_TIMEOUT_SECONDS`, default 180 s)
- Gitleaks GitHub Actions secret scanning workflow
- `CLAUDE.md` — developer guide with security rules
- `docs/README_RU.md` — Russian documentation
- `docs/REVIEW_NOTES.md` — version history and known limitations

### Changed
- `ai_generator.py` — domain context, assistant architecture, and agent blueprint
  included in generation prompt
- Test count: 151 passing (up from 87 in v0.5)

---

## [0.5-rc1] — 2026-06-24

Interactive idea analysis and interview release candidate.

### Added
- `idea_analyzer.py` — free-form idea → structured project context (rule-based)
- `interview_builder.py` — domain-specific clarifying question generator
- Per-user generation lock (`GenerationLock`)
- Per-user generation cooldown
- Stricter user-flow state guards

### Changed
- `ai_generator.py` — idea analysis and interview questions passed into prompt
- `bot.py` — interview flow integrated into FSM

---

## [0.4] — 2026-06-23

Security hardening and Docker release.

### Added
- Access control via `ALLOWED_TELEGRAM_IDS`
- `Dockerfile` and `docker-compose.yml`
- GitHub Actions CI (`tests.yml`: py_compile + pytest)
- AI output validation: file count limit, file size limit, path sanitisation

### Changed
- Safer project folder naming (`make_safe_filename`)
- Guarded file writes in `project_builder.py`
- `requirements.txt` and `requirements-dev.txt`

---

## [0.1] — 2026-06-22

Initial release.

### Added
- Async Telegram bot using `aiogram 3`
- Survey FSM (project type, goal, experience, language, hosting)
- Claude and OpenAI provider support (`ai_generator.py`)
- Template fallback for unavailable or failed AI
- `project_builder.py` — project file assembly
- `zip_utils.py` — ZIP archive creation and delivery
- `templates.py` — built-in fallback projects
- Basic unit test suite
