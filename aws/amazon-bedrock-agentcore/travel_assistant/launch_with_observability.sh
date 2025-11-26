#!/bin/bash
# Launch script with full observability configuration
# Make sure to replace placeholder values with your actual credentials

agentcore launch \
  --env OTEL_EXPORTER_OTLP_ENDPOINT="https://your-deployment-id.ingest.your-region.cloud.elastic.co:443" \
  --env OTEL_EXPORTER_OTLP_HEADERS="Authorization=ApiKey your-elastic-api-key" \
  --env OTEL_EXPORTER_OTLP_PROTOCOL="http/protobuf" \
  --env OTEL_METRICS_EXPORTER="otlp" \
  --env OTEL_TRACES_EXPORTER="otlp" \
  --env OTEL_LOGS_EXPORTER="otlp" \
  --env OTEL_RESOURCE_ATTRIBUTES="service.name=travel_assistant_quickstart,service.version=1.0.0,deployment.environment=production" \
  --env AGENT_OBSERVABILITY_ENABLED="true" \
  --env DISABLE_ADOT_OBSERVABILITY="true" \
  --env TAVILY_API_KEY="your-tavily-api-key"

