# open-responses

This shows how to use the Masaic OpenResponses as an [OpenAI Responses adapter][docs],
using its [OpenTelemetry configuration][config].

OpenAI Responses API requests are adapted and forwarded to Ollama as chat
completions.

## Prerequisites

Start Ollama and your OpenTelemetry Collector via this repository's [README](../README.md).

## Run OpenResponses

```bash
docker compose up --pull always --force-recreate --remove-orphans
```

Clean up when finished, like this:

```bash
docker compose down
```

## Call OpenResponses with python

Once OpenResponses is running, use [uv][uv] to make an OpenAI request via
[chat.py](../chat.py):

```bash
# Set the OpenAI base URL to the OpenResponses proxy, not Ollama
OPENAI_BASE_URL=http://localhost:8080/v1 uv run --exact -q --env-file env.local ../chat.py
```

Or, for the OpenAI Responses API
```bash
OPENAI_BASE_URL=http://localhost:8080/v1 uv run --exact -q --env-file env.local ../chat.py --use-responses-api
```

## Notes

OpenResponses is a Spring Boot application, so signals collected are adapted to
OpenTelemetry via a Micrometer bridge.

---
[doc]: https://openresponses.masaic.ai/openresponses/compatibility
[config]: https://openresponses.masaic.ai/openresponses/observability#setting-up-the-opentelemetry-collector
[uv]: https://docs.astral.sh/uv/getting-started/installation/
