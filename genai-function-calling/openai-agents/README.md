# Function Calling with OpenAI Agents SDK (Python)

[main.py](main.py) implements the [example application flow][flow] using
[OpenAI Agents SDK (Python)][openai-agents-python].

[Dockerfile](Dockerfile) starts the application with Elastic Distribution
of OpenTelemetry (EDOT) Python, via `opentelemetry-instrument`.

Notably, this shows how to add extra instrumentation to EDOT, as the OpenAI
Agents support is via [OpenInference][openinference].

## Configure

Copy [env.example](env.example) to `.env` and update its `OPENAI_API_KEY`.

An OTLP compatible endpoint should be listening for traces, metrics and logs on
`http://localhost:4317`. If not, update `OTEL_EXPORTER_OTLP_ENDPOINT` as well.

For example, if Elastic APM server is running locally, edit `.env` like this:
```
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:8200
```

## Run with Docker

```bash
docker compose run --build --rm genai-function-calling
```

## Run with Python

First, set up a Python virtual environment like this:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install 'python-dotenv[cli]'
```

Next, install required packages:
```bash
pip install -r requirements.txt
```

Now, use EDOT to bootstrap instrumentation (this only needs to happen once):
```bash
edot-bootstrap --action=install
# TODO(EDOT): remove when > v0.6.1
pip uninstall -y elastic-opentelemetry-instrumentation-openai
pip install 'elastic-opentelemetry-instrumentation-openai @ git+https://github.com/elastic/elastic-otel-python-instrumentations.git@main#subdirectory=instrumentation/elastic-opentelemetry-instrumentation-openai'
```

Finally, run `main.py` (notice the prefix of `opentelemetry-instrument):
```bash
dotenv run --no-override -- opentelemetry-instrument python main.py
```

## Tests

Tests use [pytest-vcr][pytest-vcr] to capture HTTP traffic for offline unit
testing. Recorded responses keeps test passing considering LLMs are
non-deterministic and the Elasticsearch version list changes frequently.

Run like this:
```bash
pip install -r requirements-dev.txt
pytest
```

OpenAI responses routinely change as they add features, and some may cause
failures. To re-record, delete [cassettes/test_main.yaml][test_main.yaml], and
run pytest with dotenv, so that ENV variables are present:

```bash
rm cassettes/test_main.yaml
dotenv -f ../.env run -- pytest
```

## Notes

The LLM should generate something like "The latest stable version of
Elasticsearch is 8.17.3", unless it hallucinates. Just run it again, if you
see something else.

OpenAI Agents SDK's OpenTelemetry instrumentation is via
[OpenInference][openinference] and only produces traces (not logs or metrics).

---
[flow]: ../README.md#example-application-flow
[openai-agents-python]: https://github.com/openai/openai-agents-python
[pytest-vcr]: https://pytest-vcr.readthedocs.io/
[test_main.yaml]: cassettes/test_main.yaml
[openinference]:  https://github.com/Arize-ai/openinference/tree/main/python/instrumentation/openinference-instrumentation-openai-agents
