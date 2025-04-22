import { MCPInstrumentation } from "@arizeai/openinference-instrumentation-mcp";
import * as MCPClientModule from "@modelcontextprotocol/sdk/client/index.js";
import * as MCPServerModule from "@modelcontextprotocol/sdk/server/index.js";

const mcpInstrumentation = new MCPInstrumentation();
// MCP must be manually instrumented as it doesn't have a traditional module structure
mcpInstrumentation.manuallyInstrument({
    clientModule: MCPClientModule,
    serverModule: MCPServerModule,
});
