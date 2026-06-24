# CLAUDE.md — AI Creator

## SECURITY: NEVER DO THIS

- Never print `.env` contents (no `cat .env`, `Get-Content .env`, `type .env`)
- Never commit `.env` — it is in `.gitignore` and must stay there
- Never hardcode tokens, API keys, or passwords in source files
- Never add secrets to test fixtures or example data

## Project Overview

AI Creator is an async Telegram bot (aiogram 3) that runs a survey → domain detection →
agent blueprint → AI generation pipeline and delivers a ZIP project archive to the user.

```
bot.py                     ← entry point, FSM handlers, generation orchestration
ai_generator.py            ← Claude / OpenAI integration, prompt building, JSON parsing
path_safety.py             ← shared path sanitisation (clean_relative_path)
project_builder.py         ← safe file writing, template assembly
runtime_guards.py          ← access control, GenerationLock, GenerationCooldown
domain_packs.py            ← domain knowledge database (7 domains)
agent_blueprint.py         ← product specification builder
assistant_architect.py     ← architecture design layer
idea_analyzer.py           ← idea → project type detection
interview_builder.py       ← domain-specific clarifying questions
templates.py               ← built-in fallback project templates
zip_utils.py               ← ZIP archive creation
```

## Running the bot

```bash
python bot.py
```

Requires `TELEGRAM_BOT_TOKEN` in `.env`. Use `.env.example` as the template — never
copy real keys into it.

## Checking syntax

```bash
python -m py_compile bot.py ai_generator.py templates.py project_builder.py \
  zip_utils.py idea_analyzer.py interview_builder.py runtime_guards.py \
  domain_packs.py assistant_architect.py agent_blueprint.py path_safety.py
```

## Running tests

```bash
pytest
```

Current baseline: **129 tests passing** (12 test modules under `tests/`).
Always run after any code change. Do not mark a task done if tests are red.

## Safe commit workflow

1. `git status` — verify no `.env` in staged files
2. `git diff --staged` — review before commit
3. `git ls-files .env` — must return empty; if not, stop and investigate
4. Only then commit

## Key environment variables

| Variable | Default | Purpose |
|---|---|---|
| `TELEGRAM_BOT_TOKEN` | — | Required; bot token from BotFather |
| `AI_CREATOR_PROVIDER` | — | `anthropic` or `openai` |
| `ANTHROPIC_API_KEY` | — | Anthropic secret key |
| `OPENAI_API_KEY` | — | OpenAI secret key |
| `ALLOWED_TELEGRAM_IDS` | (empty = all) | Comma-separated Telegram user IDs |
| `AI_GENERATION_TIMEOUT_SECONDS` | 120 | Timeout for AI provider call |
| `GENERATION_COOLDOWN_SECONDS` | 60 | Per-user cooldown between generations |
| `GENERATION_PIPELINE_TIMEOUT_SECONDS` | 180 | Hard timeout for the full pipeline |

## Architecture invariants

- `path_safety.clean_relative_path` is the single source of path validation logic.
  Both `ai_generator` and `project_builder` import from it.
- `GenerationLock` prevents concurrent generation for the same user.
- `GenerationCooldown` prevents spam by adding a per-user wait after each generation.
- All user text fields are sanitised (newlines collapsed) before they enter prompts.
- Generated files are always cleaned up in `finally` blocks — no temp files leak.
