# archgw

This shows how to use the Arch Gateway as an OpenAI [LLM router][docs], using
its [`tracing` configuration][config] for OpenTelemetry.

Arch Gateway does not serve OpenAI requests. Rather, it configures an Envoy
proxy according to its configuration. Envoy handles requests, collects
telemetry and forwards them to Ollama via the OpenAI API.

## Setup

Start ollama and the otel collector via this repository's [README](../../README.md).

## Run Arch Gateway

Arch Gateway is a python command that internally runs Docker. Hence, you need a
working Docker configuration. Run `archgw` using `uv run` from [uv][uv] to ensure
Python is available:

```bash
uv run --with archgw -- archgw up arch_config.yaml
```

When finished, clean up like this:

```bash
uv run --with archgw -- archgw down
```

## Start Prometheus Scraping

### Elastic Stack

If your OpenTelemetry backend is Elasticsearch, you can pump Prometheus metrics
coming from Arch Gateway to Elasticsearch like this:

```bash
docker compose -f docker-compose-elastic.yml run --rm prometheus-pump
```

### otel-tui

If you are using [otel-tui][otel-tui] to visualize OpenTelemetry data, you can
add Arch Gateway's Prometheus endpoint to it when starting, like this:

```bash
otel-tui --prom-target http://localhost:19901/stats?format=prometheus
```

## Call Arch Gateway with python

Once Arch Gateway is running, use [uv][uv] to make an OpenAI request via
[chat.py](../chat.py):

```bash
uv run --exact -q --env-file env.local ../chat.py
```

## Notes

OpenTelemetry signals are a function of native [Envoy support][envoy-otel]
and anything added in Arch Gateway's [wasm filter][archgw-wasm].

* `archgw` invokes `envoy` in a Docker container, which is why this has no
  instructions to run from Docker (to avoid nested docker).
* Traces come from Envoy, whose configuration is written by `archgw`. At the
  moment, this hard-codes aspects including default ports.
* Until [this][openai-responses] resolves, don't use `--use-responses-api`.

The chat prompt was designed to be idempotent, but the results are not. You may
see something besides 'South Atlantic Ocean.'.
Just run it again until we find a way to make the results idempotent.

---
[docs]: https://github.com/katanemo/archgw?tab=readme-ov-file#use-arch-gateway-as-llm-router
[config]: https://docs.archgw.com/guides/observability/tracing.html
[envoy-otel]: https://www.envoyproxy.io/docs/envoy/latest/api-v3/config/trace/v3/opentelemetry.proto#extension-envoy-tracers-opentelemetry
[archgw-wasm]: https://github.com/katanemo/archgw/blob/main/arch/README.md
[uv]: https://docs.astral.sh/uv/getting-started/installation/
[openai-responses]: https://github.com/katanemo/archgw/issues/476
[otel-tui]: https://github.com/ymtdzzz/otel-tui
