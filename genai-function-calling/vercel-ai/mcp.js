const {McpServer} = require('@modelcontextprotocol/sdk/server/mcp.js');
const {StdioServerTransport} = require('@modelcontextprotocol/sdk/server/stdio.js');
const {StdioClientTransport} = require('@modelcontextprotocol/sdk/client/stdio.js');
const {experimental_createMCPClient} = require('ai');

const fs = require('fs');
const path = require('path');

const SERVER_ARG = '--mcp-server';

// Get MCP server parameters from package.json
let name, version;
try {
    const packageJsonPath = path.join(__dirname, 'package.json');
    const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, 'utf8'));
    name = packageJson.name;
    version = packageJson.version;
} catch (error) {
    console.error('Failed to read package.json:', error.message);
    process.exit(1);
}

/**
 * Starts an MCP server and registers the provided tools, listening on stdin/stdout.
 *
 * @param {import('ai').ToolSet} tools - The tools to register with the MCP server.
 */
async function mcpServerMain(tools) {
    const server = new McpServer({name, version});

    // Register each tool with the server
    Object.entries(tools).forEach(([toolName, tool]) => {
        console.log(`Registering tool: ${toolName}`);
        server.tool(
            toolName,
            tool.description,
            tool.parameters.shape,
            async (params) => {
                try {
                    const result = await tool.execute(params);
                    return {content: [{type: 'text', text: result}]};
                } catch (error) {
                    return {content: [{type: 'text', text: error.message}]};
                }
            }
        );
    });

    const transport = new StdioServerTransport();
    await server.connect(transport);
}

/**
 * Launches an MCP server in a subprocess and runs the agent with its tools via a client.
 *
 * @param {Function} runAgent - The function to run the agent with the retrieved tools.
 */
async function runAgentWithMCPClient(runAgent) {
    // MCP server is a subprocess, which doesn't inherit anything by default.
    // Minimally, we need to pass an argument to let the process know it is
    // running as a server. We also propagate any ENV or arguments to ensure
    // OpenTelemetry auto-instrumentation propagates to the child, such as
    // '-r @elastic/opentelemetry-node'. Don't do this with untrusted servers.
    const transport = new StdioClientTransport({
        command: process.execPath,
        args: [...process.execArgv, ...process.argv.slice(1), SERVER_ARG],
        env: process.env,
    });

    let client;
    try {
        client = await experimental_createMCPClient({transport});
        const tools = await client.tools();
        await runAgent(tools);
    } catch (error) {
        throw error;
    } finally {
        await client?.close();  // closing the client closes its transport
    }
}

/**
 * Main entry point to either run the MCP server directly or launch it in a subprocess
 * and run the agent with as an MCP client.
 *
 * @param {Function} runAgent - The function to run the agent with the tools.
 * @param {import('ai').ToolSet} tools - The tools to register with the MCP server.
 */
async function mcpClientMain(runAgent, tools) {
    if (process.argv.includes(SERVER_ARG)) {
        await mcpServerMain(tools);
    } else {
        await runAgentWithMCPClient(runAgent);
    }
}

module.exports = {mcpClientMain};
