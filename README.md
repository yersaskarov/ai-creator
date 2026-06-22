# AI Creator

AI Creator is a Telegram bot that asks a short product questionnaire and generates a starter project as a zip archive. It can work in a safe template mode, and it can optionally use an AI provider when the required environment variables are configured.

## Features

- Telegram questionnaire built with aiogram 3.
- Project generation for several starter categories: Telegram bot, AI agent, SaaS service, iOS backend, or a custom idea.
- Template fallback when AI generation is not configured or fails.
- Optional OpenAI or Anthropic generation through the existing provider layer.
- Zip archive delivery directly in Telegram.
- Generated `.env.example`, README, dependency files, and starter source files for the output project.

## Installation

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

On macOS or Linux, activate the virtual environment with:

```bash
source venv/bin/activate
```

## Configuration

Copy `.env.example` to `.env` and fill in the values you need:

```bash
TELEGRAM_BOT_TOKEN=
AI_CREATOR_PROVIDER=
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4.1-mini
ANTHROPIC_API_KEY=
ANTHROPIC_MODEL=claude-sonnet-4-6
```

Environment variables:

- `TELEGRAM_BOT_TOKEN`: required Telegram bot token from BotFather.
- `AI_CREATOR_PROVIDER`: optional AI provider. Supported values are `openai` and `anthropic`.
- `OPENAI_API_KEY`: required only when `AI_CREATOR_PROVIDER=openai`.
- `OPENAI_MODEL`: optional OpenAI model override.
- `ANTHROPIC_API_KEY`: required only when `AI_CREATOR_PROVIDER=anthropic`.
- `ANTHROPIC_MODEL`: optional Anthropic model override.

If no AI provider is configured, AI Creator uses built-in templates.

## Running

```bash
python bot.py
```

Then open the bot in Telegram and send `/start`.

## Security

Never commit `.env`. It may contain real Telegram, OpenAI, or Anthropic tokens. This repository includes `.env.example` only as a safe template with empty secret values.

Generated projects, virtual environments, Python caches, and zip archives are ignored by Git.

## Roadmap

- Add persistent FSM storage for production deployments.
- Add tests for template generation, JSON parsing, and zip creation.
- Add file count and archive size limits for AI-generated projects.
- Improve AI output validation with stricter schemas.
- Add deployment instructions for Render, VPS, or Docker.

## Project Status

Early portfolio/MVP stage. The bot is usable as a starter generator, but production use still needs persistent state, stronger validation, tests, monitoring, and deployment hardening.
