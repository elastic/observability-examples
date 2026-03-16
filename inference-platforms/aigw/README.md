# Envoy AI Gateway

This shows how to use [Envoy AI Gateway][docs] to proxy LLM and MCP servers,
specifically Ollama and Kiwi flight search.

Envoy AI Gateway exposes OpenAI and MCP compatible endpoints with configurable
backends. It is automatically configured by OpenAI and OpenTelemetry
environment variables read by `aigw run`, such as `OPENAI_API_KEY`. In the case
of MCP, it uses the canonical JSON format like this:

```json
{
"mcpServers": {
  "kiwi": {
    "type": "http",
    "url": "https://mcp.kiwi.com"
  }
}
}
```

`aigw run` launches an Envoy proxy to handle requests. OpenTelemetry support
for GenAI metrics and traces is handled directly in the `aigw` (go) binary.

OpenTelemetry traces produced by Envoy AI Gateway follow the [OpenInference specification][openinference].

## Prerequisites

Start Ollama and your OpenTelemetry Collector via this repository's [README](../README.md).

## Run Envoy AI Gateway

### Run with Docker

```bash
docker compose up --force-recreate --pull always --remove-orphans --wait -d
```

Clean up when finished, like this:

```bash
docker compose down
```

### Run with Go

Download [shdotenv](https://github.com/ko1nksm/shdotenv) to load `env.local` when running.

```
curl -O -L https://github.com/ko1nksm/shdotenv/releases/download/v0.14.0/shdotenv
chmod +x ./shdotenv
```

Run `aigw` from source after setting ENV variables like this:
```bash
./shdotenv -e env.local go run github.com/envoyproxy/ai-gateway/cmd/aigw@latest run --mcp-json '{"mcpServers":{"kiwi":{"type":"http","url":"https://mcp.kiwi.com"}}}'
```

## Call Envoy AI Gateway with python

Once Envoy AI Gateway is running, use [uv][uv] to make an OpenAI request via
[chat.py](../chat.py):

### Chat Completion

```bash
OPENAI_BASE_URL=http://localhost:1975/v1 uv run --exact -q --env-file env.local ../chat.py
```

Or, for the OpenAI Responses API
```bash
OPENAI_BASE_URL=http://localhost:1975/v1 uv run --exact -q --env-file env.local ../chat.py --use-responses-api
```

### MCP Agent

```bash
OPENAI_BASE_URL=http://localhost:1975/v1 MCP_URL=http://localhost:1975/mcp uv run --exact -q --env-file env.local ../agent.py
```

## Notes

Here are some constraints about the Envoy AI Gateway implementation:
* Access log integration currently requires the OTLP gRPC transport (`OTEL_EXPORTER_OTLP_PROTOCOL=grpc`).

---
[docs]: https://aigateway.envoyproxy.io/docs/cli/
[openinference]: https://github.com/Arize-ai/openinference/tree/main/spec
[uv]: https://docs.astral.sh/uv/getting-started/installation/
