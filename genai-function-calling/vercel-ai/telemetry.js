// First, import and initialize the instrumentation
const { MCPInstrumentation } = require("@arizeai/openinference-instrumentation-mcp");
const mcpInstrumentation = new MCPInstrumentation();

// Then, import the MCP modules after instrumentation is set up
const MCPClientModule = require("@modelcontextprotocol/sdk/client/index.js");
const MCPServerModule = require("@modelcontextprotocol/sdk/server/index.js");

// Finally, manually instrument the modules
mcpInstrumentation.manuallyInstrument({
    clientModule: MCPClientModule,
    serverModule: MCPServerModule,
});
