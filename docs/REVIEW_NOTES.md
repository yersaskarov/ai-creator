# AI Creator Review Notes

## v0.6 status (current)

AI Creator v0.6 is a released prototype with 151 passing tests, security hardening, and a Trading Assistant domain pack.

Changes since v0.5:

- Interactive interview flow implemented (users are asked clarifying questions in chat).
- Domain Pack system introduced (`domain_packs.py`): 7 packs covering Zabbix, Jira, Logistics, Document Automation, Knowledge Assistant, Trading, and Generic.
- Assistant Architect layer added (`assistant_architect.py`).
- Agent Blueprint layer added (`agent_blueprint.py`): generates a full product specification from domain context, idea analysis, and interview answers.
- Trading Assistant domain pack added with 9 interview questions, TradingView webhook support, prop firm risk tracking, and trading-specific security notes.
- `path_safety.py` introduced as the single source of path traversal protection; duplicate implementations removed from `ai_generator.py` and `project_builder.py`.
- `GenerationCooldown` added to `runtime_guards.py`: per-user cooldown between generation requests (env: `GENERATION_COOLDOWN_SECONDS`, default 60 s).
- Full pipeline timeout added in `bot.py` via `asyncio.wait_for` (env: `GENERATION_PIPELINE_TIMEOUT_SECONDS`, default 180 s).
- Gitleaks GitHub Actions workflow added for secret scanning on every push and pull request.
- `CLAUDE.md` added with security rules, architecture map, and safe commit workflow.
- Russian documentation added in `docs/README_RU.md`.
- `README.md` is the main English GitHub entry point; `docs/README_RU.md` is the Russian version.
- Test count: 151 passing (was 87 in v0.5 notes, 129 in v0.6 RC).

## v0.5 status (archived)

AI Creator was a v0.5 release candidate (now superseded by v0.6). It is a working Telegram bot MVP that collects project requirements, generates a starter project through an AI provider when configured, falls back to built-in templates when AI generation is unavailable or unsafe, and returns the result as a ZIP archive.

The repository includes the v0.4 hardening patch, v0.5 idea analysis and interview-question generation, access control, a per-user generation lock, and stricter user-flow guards. The latest local verification passed with 87 tests.

## v0.5 RC status

- `idea_analyzer.py` analyzes free-form project descriptions into structured project context.
- `interview_builder.py` builds clarifying questions from the idea analysis.
- `bot.py` enriches generation data with `idea_analysis` and `interview_questions` when `custom_idea` is present.
- `ai_generator.py` includes idea analysis and interview questions in the generation prompt.
- Access control can be enabled with `ALLOWED_TELEGRAM_IDS`.
- A per-user generation lock prevents overlapping generation jobs from the same user.
- Stricter user-flow guards reduce accidental out-of-order actions.
- Interview questions are currently used as an internal checklist for the AI generation prompt.
- A full Telegram interview flow is not implemented yet; users are not asked these follow-up questions in chat.
- Generated README/project architecture should reflect the checklist, but the bot does not yet collect explicit answers to those questions.
- Controlled pilot usage is possible with a small allowlisted group and manual operational supervision.

## What is already implemented

- Telegram FSM questionnaire with `aiogram`.
- Claude and OpenAI provider support through `ai_generator.py`.
- Template fallback when AI generation is disabled, times out, fails, or returns invalid output.
- AI-generated file validation for JSON format, path traversal, file count, and file size.
- Project file assembly helpers in `project_builder.py`.
- ZIP archive creation utility in `zip_utils.py`.
- Rule-based idea analysis in `idea_analyzer.py`.
- Clarifying question generation in `interview_builder.py`.
- Structured prompt enrichment with idea analysis and interview questions.
- Access control through `ALLOWED_TELEGRAM_IDS`.
- Per-user generation lock.
- Stricter user-flow guards.
- Safer project folder naming and guarded file writes.
- Dockerfile and Docker Compose deployment config.
- GitHub Actions for compile checks and tests.
- Unit tests for AI parsing, prompt sanitization, project building, ZIP creation, fallback behavior, and cleanup behavior.

## Known limitations

- FSM state is in memory, so active conversations are lost on process restart.
- Full Telegram interview flow is not implemented yet.
- Interview questions are used as a generation checklist, not asked to the user yet.
- There is no rate limiting or quota system yet.
- Generated projects are starter scaffolds, not audited production systems.
- The bot does not persist generation history.
- There is no structured logging or metrics pipeline yet.
- Docker Compose runs a single bot container only; no Redis, database, or monitoring service is included.

## Production gaps

- Redis FSM.
- Rate limiting / quotas.
- Monitoring / healthcheck.
- Queue / worker.
- Non-root Docker user.

## Security notes

- `.env` is ignored by Git and Docker build context.
- AI-generated paths are normalized and checked before being accepted.
- `project_builder.write_files()` rejects unsafe paths as defense in depth.
- ZIP creation now validates that the archive root is the direct parent of the project directory.
- OpenAI and Anthropic SDK clients have an explicit provider timeout.
- User text included in AI prompts is normalized to collapse multiline prompt-injection style input.
- File count and file size limits reduce risk from oversized AI responses.
- The bot can enforce an allowlist through `ALLOWED_TELEGRAM_IDS`; empty allowlists still permit open access.
- Prompt injection cannot be fully solved by sanitization; generated code should be reviewed before execution.

## v0.5 roadmap

- Add Redis or another persistent FSM storage.
- Add rate limits and daily generation quotas.
- Move long-running generation into a background queue.
- Add structured logs with request IDs and generation mode fields.
- Add metrics and basic operational dashboards.
- Add container healthcheck or external uptime check.
- Add production deployment notes for systemd, backups, and log rotation.
- Add tests around concurrent generation behavior.

## What is intentionally not implemented yet

- Redis, queue workers, rate limiting, and monitoring are intentionally deferred.
- A database is not included because the current prototype does not persist user projects or history.
- Healthcheck is not included because the current bot has no HTTP service endpoint.
- Generated-code sandboxing is not implemented; AI Creator creates ZIP starter projects, it does not execute them.
- Full prompt-injection prevention is not claimed. The hardening patch only reduces obvious multiline instruction injection in prompt fields.
- Multi-container production infrastructure is intentionally out of scope for the current prototype.
