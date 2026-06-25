FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN python -m pip install --no-cache-dir --upgrade pip

COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY . .

RUN useradd --no-create-home --shell /bin/false botuser \
    && mkdir -p generated_projects \
    && chown -R botuser:botuser /app

USER botuser

HEALTHCHECK --interval=60s --timeout=10s --start-period=30s --retries=3 \
    CMD python -c "import aiogram, anthropic, openai"

CMD ["python", "bot.py"]
