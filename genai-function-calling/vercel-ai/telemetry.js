const { MCPInstrumentation } = require("@arizeai/openinference-instrumentation-mcp");

const mcpInstrumentation = new MCPInstrumentation();
// MCP must be manually instrumented as it doesn't have a traditional module structure
mcpInstrumentation.manuallyInstrument({
    clientStdioModule: require("@modelcontextprotocol/sdk/client/stdio.js"),
    serverStdioModule: require("@modelcontextprotocol/sdk/server/stdio.js"),
});
