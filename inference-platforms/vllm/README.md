# vLLM

This shows how to use the [vLLM OpenTelemetry POC][otel-poc] to export
OpenTelemetry traces from vLLM requests to its OpenAI compatible endpoint.

## Prerequisites

Start Ollama and your OpenTelemetry Collector via this repository's [README](../README.md).

## Run vLLM

```bash
docker compose up --build --force-recreate --remove-orphans
```

Clean up when finished, like this:

```bash
docker compose down
```

## Call vLLM with python

Once vLLM is running, use [uv][uv] to make an OpenAI request via
[chat.py](../chat.py):

```bash
uv run --exact -q --env-file env.local ../chat.py
```

## Notes

* This does not yet support metrics, and there is no GitHub issue on it.
* This does not yet support logs, and there is no GitHub issue on it.
* Until [this][openai-responses] resolves, don't use `--use-responses-api`.

---
[otel-poc]: https://github.com/vllm-project/vllm/blob/main/examples/online_serving/opentelemetry/README.md
[uv]: https://docs.astral.sh/uv/getting-started/installation/
[openai-responses]: https://github.com/vllm-project/vllm/issues/14721
