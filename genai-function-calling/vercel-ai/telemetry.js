// Import and initialize MCPInstrumentation before importing the MCP modules.
const { MCPInstrumentation } = require("@arizeai/openinference-instrumentation-mcp");
const mcpInstrumentation = new MCPInstrumentation();

// Then, manually instrument MCP, as it doesn't have a traditional module structure.
mcpInstrumentation.manuallyInstrument({
    clientModule: require("@modelcontextprotocol/sdk/client/index.js"),
    serverModule: require("@modelcontextprotocol/sdk/server/index.js"),
});