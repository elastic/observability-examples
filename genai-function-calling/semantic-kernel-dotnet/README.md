# Function Calling with Semantic Kernel .NET

[Program.cs](Program.cs) implements the [example application flow][flow] using
[Semantic Kernel][semantic-kernel] for .NET.

[Dockerfile](Dockerfile) starts the application with Elastic Distribution
of OpenTelemetry (EDOT) .NET, by prepending its command with `instrument.sh`.

## Configure

Copy [env.example](env.example) to `.env` and update its `OPENAI_API_KEY`.

An OTLP compatible endpoint should be listening for traces, metrics and logs on
`http://localhost:4318`. If not, update `OTEL_EXPORTER_OTLP_ENDPOINT` as well.

## Run with Docker

```bash
docker compose run --build --rm genai-function-calling
```

## Notes

The LLM should generate something like "The latest stable version of
Elasticsearch is 8.18.0", unless it hallucinates. Just run it again, if you
see something else.

Semantic Kernel .NET's OpenTelemetry instrumentation uses the following custom
ENV variables, and only produces traces (not logs or metrics).
```
SEMANTICKERNEL_EXPERIMENTAL_GENAI_ENABLE_OTEL_DIAGNOSTICS=true
SEMANTICKERNEL_EXPERIMENTAL_GENAI_ENABLE_OTEL_DIAGNOSTICS_SENSITIVE=true
OTEL_DOTNET_AUTO_TRACES_ADDITIONAL_SOURCES="Microsoft.SemanticKernel*"
```

---
[flow]: ../README.md#example-application-flow
[semantic-kernel]: https://github.com/microsoft/semantic-kernel/tree/main/dotnet
