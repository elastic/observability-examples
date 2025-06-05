# Llama Stack

This shows how to use [Llama Stack][docs] to proxy Ollama, accessible via an
OpenAI compatible API.

This uses the [`otel` telemetry sink][otel-sink] to export OpenTelemetry traces
and metrics from signals recorded with Llama Stack's observability SDK.

## Prerequisites

Start Ollama and your OpenTelemetry Collector via this repository's [README](../README.md).

## Run Llama Stack

```bash
docker compose up --pull always --force-recreate --remove-orphans
```

Clean up when finished, like this:

```bash
docker compose down
```

## Call Llama Stack with python

Once Llama Stack is running, use [uv][uv] to make an OpenAI request via
[chat.py](../chat.py):

```bash
uv run --exact -q --env-file env.local ../chat.py
```

Or, for the OpenAI Responses API
```bash
uv run --exact -q --env-file env.local ../chat.py --use-responses-api
```

## Notes

Here are some constraints about the LlamaStack implementation:
* Only supports llama models (so not Qwen)
* Bridges its tracing and metrics APIs to `otel_trace` and `otel_metric` sinks.
* Until [this issue][docker] resolves, running docker on Apple Silicon
  requires emulation.
* Llama Stack doesn't yet have ENV variable support for the OTLP exporter.
  Hence, we use Docker's localhost:host-gateway to direct localhost traffic
  back to the host. See https://github.com/meta-llama/llama-stack/issues/783

---
[docs]: https://llama-stack.readthedocs.io/en/latest/index.html
[otel-sink]: https://llama-stack.readthedocs.io/en/latest/building_applications/telemetry.html#configuration
[uv]: https://docs.astral.sh/uv/getting-started/installation/
[docker]: https://github.com/meta-llama/llama-stack/issues/406
