# AgC - Agentic Compute

This shows how to use the AgC as an [OpenAI Responses adapter][docs],
using its [OpenTelemetry configuration][config].

AgC API requests are adapted and forwarded to Ollama as chat
completions.

## Prerequisites

Start Ollama and your OpenTelemetry Collector via this repository's [README](../README.md).

## Run AgC

```bash
docker compose up --pull always --force-recreate --remove-orphans
```

Clean up when finished, like this:

```bash
docker compose down
```

## Call AgC with python

Once AgC is running, use [uv][uv] to make an OpenAI request via
[chat.py](../chat.py):

```bash
# Set the OpenAI base URL to the AgC proxy, not Ollama
OPENAI_BASE_URL=http://localhost:6644/v1 uv run --exact -q --env-file env.local ../chat.py
```

Or, for the AgC Responses API
```bash
OPENAI_BASE_URL=http://localhost:6644/v1 uv run --exact -q --env-file env.local ../chat.py --use-responses-api
```

## Notes

AgC comes up with a platform service: open-responses (a Spring Boot application), so signals collected are adapted to
OpenTelemetry via a Otel-SDK.

---
[doc]: https://github.com/masaic-ai-platform/AgC
[config]: https://github.com/masaic-ai-platform/AgC/blob/main/platform/README.md#setting-up-the-opentelemetry-collector
[uv]: https://docs.astral.sh/uv/getting-started/installation/
