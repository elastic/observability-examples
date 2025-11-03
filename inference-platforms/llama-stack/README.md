# Llama Stack

This shows how to use [Llama Stack][docs] to proxy Ollama via an OpenAI
compatible API.

**Note**: Telemetry is currently broken in v0.3.1, but not on main.

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

* Uses the `starter` distribution with its built-in `remote::openai` provider,
  pointing to Ollama via `OPENAI_BASE_URL` environment variable.
* Models require `provider_id/` prefix (e.g., `openai/qwen3:0.6b`) as of
  [PR #3822][prefix-pr].
* Until [this issue][docker] resolves, running docker on Apple Silicon
  requires emulation.

---
[docs]: https://llama-stack.readthedocs.io/en/latest/index.html
[otel-sink]: https://llama-stack.readthedocs.io/en/latest/building_applications/telemetry.html#configuration
[uv]: https://docs.astral.sh/uv/getting-started/installation/
[prefix-pr]: https://github.com/meta-llama/llama-stack/pull/3822
[docker]: https://github.com/llamastack/llama-stack/issues/406
