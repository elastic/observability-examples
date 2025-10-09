# Function Calling with Spring AI

[Main.java](src/main/java/example/Main.java) implements the
[example application flow][flow] using [Spring AI][spring-ai].

[Dockerfile](Dockerfile) starts the application with Elastic Distribution
of OpenTelemetry (EDOT) Java, via `-javaagent:/elastic-otel-javaagent.jar`.

Notably, this shows how to bridge Micrometer to OpenTelemetry in the use case
of Spring AI.

## Configure

Copy [env.example](env.example) to `.env` and update its `OPENAI_API_KEY`.

An OTLP compatible endpoint should be listening for traces, metrics and logs on
`http://localhost:4318`. If not, update `OTEL_EXPORTER_OTLP_ENDPOINT` as well.

## Run with Docker

```bash
docker compose run --build --rm genai-function-calling
```

## Run with Maven

Download shdotenv to load `.env` file when running.

```
curl -O -L https://github.com/ko1nksm/shdotenv/releases/download/v0.14.0/shdotenv
chmod +x ./shdotenv
```

Run maven after setting ENV variables like this:
```bash
./shdotenv ./mvnw -q clean package exec:exec
```

## Run with Model Context Protocol (MCP)

[Mcp.java](src/main/java/example/Mcp.java) includes code needed to decouple
tool invocation via the [Model Context Protocol (MCP) flow][flow-mcp]. To run
using MCP, adjust arguments to `docker compose run` or `./shdotenv ./mvnw`.

For example, to run with Docker:
```bash
docker compose run --build --rm genai-function-calling --mcp
```

Or to run with Maven:
```bash
./shdotenv ./mvnw -q clean package exec:exec -Dtools=mcp
```

## Notes

The LLM should generate something like "The latest stable version of
Elasticsearch is 9.1.5", unless it hallucinates. Just run it again, if you
see something else.

Spring AI uses Micrometer which bridges to OpenTelemetry, but needs a few
tweaks.

Customization of data included in traces, is defined in
[application.yml](src/main/resources/application.yml), notably to see chat
completion details, you need to add this:
```yml
spring:
  ai:
    chat:
      observations:
        log-prompt: true
        log-completion: true
        include-error-logging: true
logging:
  level:
    org:
      springframework:
        ai:
          chat:
            observation: INFO
            client:
              observation: INFO
```

To delegate OpenTelemetry to EDOT, [Main.java](src/main/java/example/Main.java)
defines this bean:
```java
@Bean
OpenTelemetry openTelemetry() {
    return GlobalOpenTelemetry.get();
}
```

Finally, to route Micrometer metrics to OpenTelemetry, you need this ENV:
```
OTEL_INSTRUMENTATION_MICROMETER_ENABLED=true
```

---
[flow]: ../README.md#example-application-flow
[spring-ai]: https://github.com/spring-projects/spring-ai/
[flow-mcp]: ../README.md#model-context-protocol-flow
