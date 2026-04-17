# plano

This shows how to use [Plano][docs] as an OpenAI [LLM router][config], using
its `tracing` configuration for OpenTelemetry.

Plano defaults to native mode, downloading pre-compiled Envoy binaries to
`~/.plano/`. Envoy handles requests, collects telemetry and forwards them to
Ollama via the OpenAI API.

## Prerequisites

Start Ollama and your OpenTelemetry Collector via this repository's [README](../README.md).

## Run Plano

Plano is a python command that runs Envoy natively (no Docker required). Run
`planoai` using `uv run` from [uv][uv]:

```bash
uv run --python 3.13 --with planoai -- planoai up plano_config.yaml
```

When finished, clean up like this:

```bash
uv run --python 3.13 --with planoai -- planoai down
```

## Call Plano with python

Once Plano is running, use [uv][uv] to make an OpenAI request via
[chat.py](../chat.py):

```bash
uv run --exact -q --env-file env.local ../chat.py
```

## Start Prometheus Scraping

### otel-tui

If you are using [otel-tui][otel-tui] to visualize OpenTelemetry data, you can
add Plano's Prometheus endpoint to it when starting, like this:

```bash
otel-tui --prom-target http://localhost:9901/stats?format=prometheus
```

### Elastic Stack

If your OpenTelemetry backend is Elasticsearch, you can pump Prometheus metrics
coming from Plano to Elasticsearch like this:

```bash
docker compose -f docker-compose-elastic.yml run --rm prometheus-pump
```

## Notes

OpenTelemetry signals are a function of native [Envoy support][envoy-otel]
and anything added in Plano's [wasm filter][plano-wasm].

* Traces come from Envoy, whose configuration is written by `planoai`. At the
  moment, this hard-codes aspects including default ports.
* Prometheus metrics show the cluster as "openai_localhost" - the
  provider_interface plus the first segment of the hostname.
* Until [this][openai-responses] resolves, don't use `--use-responses-api`.

The chat prompt was designed to be idempotent, but the results are not. You may
see something besides 'South Atlantic Ocean.'.
Just run it again until we find a way to make the results idempotent.

---
[docs]: https://docs.planoai.dev
[config]: https://docs.planoai.dev/guides/observability/tracing.html
[envoy-otel]: https://www.envoyproxy.io/docs/envoy/latest/api-v3/config/trace/v3/opentelemetry.proto#extension-envoy-tracers-opentelemetry
[plano-wasm]: https://github.com/katanemo/plano/blob/main/README.md
[uv]: https://docs.astral.sh/uv/getting-started/installation/
[openai-responses]: https://github.com/katanemo/plano/issues/476
[otel-tui]: https://github.com/ymtdzzz/otel-tui
