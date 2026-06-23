# AI Creator v0.4 Review Notes

## Current status

AI Creator v0.4 is a working Telegram bot MVP that collects project requirements, generates a starter project through an AI provider when configured, falls back to built-in templates when AI generation is unavailable or unsafe, and returns the result as a ZIP archive.

The repository currently includes the v0.4 hardening patch. The latest local verification passed with 40 tests.

## What is already implemented

- Telegram FSM questionnaire with `aiogram`.
- Claude and OpenAI provider support through `ai_generator.py`.
- Template fallback when AI generation is disabled, times out, fails, or returns invalid output.
- AI-generated file validation for JSON format, path traversal, file count, and file size.
- Project file assembly helpers in `project_builder.py`.
- ZIP archive creation utility in `zip_utils.py`.
- Safer project folder naming and guarded file writes.
- Dockerfile and Docker Compose deployment config.
- GitHub Actions for compile checks and tests.
- Unit tests for AI parsing, prompt sanitization, project building, ZIP creation, fallback behavior, and cleanup behavior.

## Known limitations

- FSM state is in memory, so active conversations are lost on process restart.
- There is no per-user concurrency lock yet; a user can start overlapping generations.
- There is no rate limiting or quota system yet.
- Generated projects are starter scaffolds, not audited production systems.
- The bot does not persist generation history.
- There is no structured logging or metrics pipeline yet.
- Docker Compose runs a single bot container only; no Redis, database, or monitoring service is included.

## Security notes

- `.env` is ignored by Git and Docker build context.
- AI-generated paths are normalized and checked before being accepted.
- `project_builder.write_files()` rejects unsafe paths as defense in depth.
- ZIP creation now validates that the archive root is the direct parent of the project directory.
- OpenAI and Anthropic SDK clients have an explicit provider timeout.
- User text included in AI prompts is normalized to collapse multiline prompt-injection style input.
- File count and file size limits reduce risk from oversized AI responses.
- The bot still relies on Telegram-side identity and does not implement app-level authorization.
- Prompt injection cannot be fully solved by sanitization; generated code should be reviewed before execution.

## v0.5 roadmap

- Add Redis or another persistent FSM storage.
- Add per-user generation lock to prevent concurrent jobs.
- Add rate limits and daily generation quotas.
- Move long-running generation into a background queue.
- Add structured logs with request IDs and generation mode fields.
- Add metrics and basic operational dashboards.
- Add container healthcheck or external uptime check.
- Add production deployment notes for systemd, backups, and log rotation.
- Add tests around concurrent generation behavior.

## What is intentionally not implemented yet

- Redis, queue workers, and monitoring are intentionally deferred to v0.5.
- A database is not included because v0.4 does not persist user projects or history.
- Healthcheck is not included because the current bot has no HTTP service endpoint.
- Generated-code sandboxing is not implemented; AI Creator creates ZIP starter projects, it does not execute them.
- Full prompt-injection prevention is not claimed. v0.4 only reduces obvious multiline instruction injection in prompt fields.
- Multi-container production infrastructure is intentionally out of scope for the v0.4 MVP.
