# LiteLLM

This shows how to use the LiteLLM Proxy Server as an [OpenAI gateway][docs],
using its [`otel` logging callback][config] for OpenTelemetry.

Requests to the proxy are logged and forwarded to Ollama via the OpenAI API.
The `otel` logging callback use the OpenTelemetry Python SDK to export traces.

## Prerequisites

Start Ollama and your OpenTelemetry Collector via this repository's [README](../README.md).

## Run LiteLLM

```bash
docker compose up --build --force-recreate --remove-orphans
```

Clean up when finished, like this:

```bash
docker compose down
```

## Call LiteLLM with python

Once LiteLLM is running, use [uv][uv] to make an OpenAI request via
[chat.py](../chat.py):

```bash
# Set the OpenAI base URL to the LiteLLM proxy, not Ollama
OPENAI_BASE_URL=http://localhost:4000/v1 uv run --exact -q --env-file env.local ../chat.py
```

## Notes

* LiteLLM uses its callbacks, not `opentelemetry-instrument`, to instrument
  calls. This prevents propagation from working.
* LiteLLM uses [custom env][env] to configure OTLP and the tracer. This means
  `opentelemetry-instrument` can't configure it.
* LiteLLM makes spurious HTTP requests to its [pricing endpoint][endpoint],
  which shows up as an extra trace when in use.
* `--use-responses-api` only works when what you are proxying supports it. In
  other words, it doesn't work with Ollama unless Ollama adds responses API.

---
[docs]: https://docs.litellm.ai/docs/simple_proxy
[config]: https://github.com/BerriAI/litellm/blob/main/litellm/integrations/opentelemetry.py
[uv]: https://docs.astral.sh/uv/getting-started/installation/
[sdk]: https://github.com/BerriAI/litellm/blob/main/litellm/main.py
[env]: https://github.com/BerriAI/litellm/issues/9901
[endpoint]: https://raw.githubusercontent.com/BerriAI/litellm/main/model_prices_and_context_window.json