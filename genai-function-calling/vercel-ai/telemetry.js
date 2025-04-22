import { NodeSDK } from "@opentelemetry/sdk-node";
import { getNodeAutoInstrumentations } from '@opentelemetry/auto-instrumentations-node';
import { OTLPTraceExporter} from "@opentelemetry/exporter-trace-otlp-proto";
import { MCPInstrumentation } from "@arizeai/openinference-instrumentation-mcp";
import * as MCPClientModule from "@modelcontextprotocol/sdk/client/index.js";
import * as MCPServerModule from "@modelcontextprotocol/sdk/server/index.js";

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
