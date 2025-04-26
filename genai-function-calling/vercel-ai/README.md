# Function Calling with Vercel AI (Node.js)

[index.js](index.js) implements the [example application flow][flow] using
[Vercel AI (Node.js)][vercel-ai].

[package.json](package.json) starts the application with Elastic Distribution
of OpenTelemetry (EDOT) Node.js, by requiring `@elastic/opentelemetry-node`

## Configure

Copy [env.example](env.example) to `.env` and update its `OPENAI_API_KEY`.

An OTLP compatible endpoint should be listening for traces, metrics and logs on
`http://localhost:4318`. If not, update `OTEL_EXPORTER_OTLP_ENDPOINT` as well.

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


## Run with Model Context Protocol (MCP)

[mcp.js](mcp.js) includes code needed to decouple tool discovery and invocation
via the [Model Context Protocol (MCP) flow][flow-mcp]. To run using MCP, append
`-- --mcp` flag to `npm start` or `docker compose run` command.

For example, to run with Docker:
```bash
docker compose run --build --rm genai-function-calling -- --mcp
```

Or to run with npm:
```bash
npm run start -- --mcp
```

## Notes

The LLM should generate something like "The latest stable version of
Elasticsearch is 8.18.0," unless it hallucinates. Run it again, if you see
something else.

Vercel AI's OpenTelemetry instrumentation only produces traces (not logs or
metrics).

This uses [OpenInference][openinference] to propagate trace identifiers when
using MCP.

---
[flow]: ../README.md#example-application-flow
[vercel-ai]: https://github.com/vercel/ai
[flow-mcp]: ../README.md#model-context-protocol-flow
[openinference]: https://github.com/Arize-ai/openinference/tree/main/js/packages/openinference-instrumentation-mcp
