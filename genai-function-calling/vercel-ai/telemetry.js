const { NodeSDK } = require("@opentelemetry/sdk-node");
const { getNodeAutoInstrumentations } = require('@opentelemetry/auto-instrumentations-node');
const { OTLPTraceExporter } = require("@opentelemetry/exporter-trace-otlp-proto");
const { MCPInstrumentation } = require("@arizeai/openinference-instrumentation-mcp");
const MCPClientModule = require("@modelcontextprotocol/sdk/client/index.js");
const MCPServerModule = require("@modelcontextprotocol/sdk/server/index.js");

const mcpInstrumentation = new MCPInstrumentation();
// MCP must be manually instrumented as it doesn't have a traditional module structure
mcpInstrumentation.manuallyInstrument({
    clientModule: MCPClientModule,
    serverModule: MCPServerModule,
});

const sdk = new NodeSDK({
    traceExporter: new OTLPTraceExporter(),
    instrumentations: [getNodeAutoInstrumentations()],
});

sdk.start();

process.on("SIGTERM", async () => {
    try {
        await sdk.shutdown();
    } catch (err) {
        console.warn("warning: error shutting down OTel SDK", err);
    }
    process.exit();
});

process.once("beforeExit", async () => {
    // Flush recent telemetry data if about to shutdown.
    try {
        await sdk.shutdown();
    } catch (err) {
        console.warn("warning: error shutting down OTel SDK", err);
    }
});
