const OTEL_EXPORTER_OTLP_HEADERS = process.env.OTEL_EXPORTER_OTLP_HEADERS;
// error if secret token is not set
if (!OTEL_EXPORTER_OTLP_HEADERS) {
  throw new Error("OTEL_EXPORTER_OTLP_HEADERS environment variable is not set");
}

const OTEL_EXPORTER_OTLP_ENDPOINT = process.env.OTEL_EXPORTER_OTLP_ENDPOINT;
// error if server url is not set
if (!OTEL_EXPORTER_OTLP_ENDPOINT) {
  throw new Error("OTEL_EXPORTER_OTLP_ENDPOINT environment variable is not set");
}

// Parse the environment variable string into an object
const envAttributes = process.env.OTEL_RESOURCE_ATTRIBUTES || '';
const attributes = envAttributes.split(',').reduce((acc, curr) => {
  const [key, value] = curr.split('=');
  if (key && value) {
    acc[key.trim()] = value.trim();
  }
  return acc;
}, {});


const { SemanticResourceAttributes } = require('@opentelemetry/semantic-conventions');
const { NodeSDK } = require('@opentelemetry/sdk-node');
// Import OpenTelemetry instrumentations
// NOTE: they are part of @opentelemetry/auto-instrumentations
const { HttpInstrumentation } = require('@opentelemetry/instrumentation-http');
const { ExpressInstrumentation } = require('@opentelemetry/instrumentation-express');

// Start the SDK
const sdk = new NodeSDK({
  resource: {
    attributes: {
      [SemanticResourceAttributes.SERVICE_NAME]: attributes['service.name'] || 'node-server-otel-manual',
      [SemanticResourceAttributes.SERVICE_VERSION]: attributes['service.version'] || '1.0.0',
      [SemanticResourceAttributes.DEPLOYMENT_ENVIRONMENT]: attributes['deployment.environment'] || 'production',
    }
  },
  instrumentations: [
    new HttpInstrumentation(),
    new ExpressInstrumentation(),
  ],
});

// Gracefull shudown
process.on('SIGTERM', async () => {
  try {
    await sdk.shutdown();
  } catch (err) {
    console.warn('warning: error shutting down OTel SDK', err);
  }
  process.exit();
});

process.once('beforeExit', async () => {
  // Flush recent telemetry data if about the shutdown.
  try {
    await sdk.shutdown();
  } catch (err) {
    console.warn('warning: error shutting down OTel SDK', err);
  }
});

sdk.start();



// Add OpenTelemetry packages
// const opentelemetry = require("@opentelemetry/api");
// const { NodeTracerProvider } = require('@opentelemetry/sdk-trace-node');
// const { BatchSpanProcessor } = require("@opentelemetry/sdk-trace-base");
// const { OTLPTraceExporter } = require('@opentelemetry/exporter-trace-otlp-grpc');
// const { Resource } = require('@opentelemetry/resources');
// const { SemanticResourceAttributes } = require('@opentelemetry/semantic-conventions');

// const { registerInstrumentations } = require('@opentelemetry/instrumentation');