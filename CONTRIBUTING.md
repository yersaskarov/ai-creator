# Contributing to AI Creator

Thank you for your interest in contributing.

---

## Development Setup

```bash
git clone https://github.com/yersaskarov/ai-creator.git
cd ai-creator
python -m venv venv
source venv/bin/activate        # macOS / Linux
# venv\Scripts\activate         # Windows

pip install -r requirements-dev.txt
cp .env.example .env
# Fill in TELEGRAM_BOT_TOKEN (required to run the bot)
```

---

## Running the Bot Locally

```bash
python bot.py
```

---

## Running Tests

```bash
python -m py_compile bot.py ai_generator.py templates.py project_builder.py \
  zip_utils.py idea_analyzer.py interview_builder.py runtime_guards.py \
  domain_packs.py assistant_architect.py agent_blueprint.py path_safety.py

pytest
```

All 151 tests must pass before opening a PR.

---

## Pull Request Guidelines

- Keep PRs focused: one concern per PR.
- Tests must be green (`pytest` passes locally).
- Do not break existing Telegram UX or pipeline behaviour.
- Do not commit `.env` — the pre-commit check in `CLAUDE.md` shows how to verify.
- Update `CHANGELOG.md` under `[Unreleased]` if your change is user-visible.

---

## Commit Style

Use a short imperative subject line (≤ 72 chars):

```
Add support for HR domain pack
Fix path traversal edge case in clean_relative_path
Update README Docker section
```

Avoid generic messages like `fix`, `update`, `changes`.

---

## Code Style

- Python 3.12, PEP 8.
- Type hints on all public functions.
- No comments explaining *what* the code does — only *why* when non-obvious.
- No dead code, no TODO stubs left in merged PRs.

---

## Security

If you find a security issue, **do not open a public issue**.
See [SECURITY.md](SECURITY.md) for the responsible disclosure process.
