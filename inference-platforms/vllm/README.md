# vLLM

This shows how to export OpenTelemetry traces from [vLLM][vllm] requests to
its OpenAI compatible endpoint.

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

Or, for the OpenAI Responses API
```bash
uv run --exact -q --env-file env.local ../chat.py --use-responses-api
```

## Notes

* This does not yet support metrics, and there is no GitHub issue on it.
* This does not yet support logs, and there is no GitHub issue on it.

---
[vllm]: https://docs.vllm.ai/en/latest/features/opentelemetry.html
[uv]: https://docs.astral.sh/uv/getting-started/installation/
