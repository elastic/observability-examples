# Function Calling with Vercel AI (Node.js)

[index.js](index.js) implements the [example application flow][flow] using
[Vercel AI (Node.js)][vercel-ai].

[package.json](package.json) starts the application with Elastic Distribution
of OpenTelemetry (EDOT) Node.js, by requiring `@elastic/opentelemetry-node`

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

## Run with npm

```bash
nvm install --lts
nvm use --lts
npm install
npm start
```

## Notes

The LLM should generate something like "The latest stable version of
Elasticsearch is 8.17.4", unless it hallucinates. Just run it again, if you
see something else.

Vercel AI's OpenTelemetry instrumentation only produces traces (not logs or
metrics).

---
[flow]: ../README.md#example-application-flow
[vercel-ai]: https://github.com/vercel/ai

