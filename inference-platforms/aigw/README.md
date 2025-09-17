# Envoy AI Gateway

This shows how to use [Envoy AI Gateway][docs] to proxy Ollama, accessible via an
OpenAI compatible API.

Envoy AI Gateway [YAML configuration](ai-gateway-local.yaml) is processed and run
by `aigw`, which launches an Envoy proxy to handle requests. OpenTelemetry support
for GenAI metrics and traces is handled directly in the `aigw` (go) binary.

OpenTelemetry traces produced by Envoy AI Gateway follow the [OpenInference specification][openinference].

## Prerequisites

Start Ollama and your OpenTelemetry Collector via this repository's [README](../README.md).

## Run Envoy AI Gateway

```bash
docker compose pull
docker compose up --force-recreate --remove-orphans
```

Clean up when finished, like this:

```bash
docker compose down
```

## Call Envoy AI Gateway with python

Once Envoy AI Gateway is running, use [uv][uv] to make an OpenAI request via
[chat.py](../chat.py):

```bash
uv run --exact -q --env-file env.local ../chat.py
```

## Notes

Here are some constraints about the Envoy AI Gateway implementation:
* Until [this][openai-responses] resolves, don't use `--use-responses-api`.

---
[docs]: https://aigateway.envoyproxy.io/docs/cli/
[openinference]: https://github.com/Arize-ai/openinference/tree/main/spec
[uv]: https://docs.astral.sh/uv/getting-started/installation/
[openai-responses]: https://github.com/envoyproxy/ai-gateway/issues/980
