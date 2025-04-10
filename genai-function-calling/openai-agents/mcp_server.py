from agents.mcp import MCPServerStdio
from mcp.server.fastmcp import FastMCP
import os
import signal
import sys


SERVER_ARG = "--mcp-server"


def handler(signum, frame):
    sys.exit(0)


async def mcp_server_main(tools):
    mcp_server = FastMCP(log_level="WARNING")
    for tool in tools:
        mcp_server.add_tool(tool)
    # Mysteriously, cleanup such as from opentelemetry-instrument does not run on exit
    # without registering an effectively no-op termination handler.
    signal.signal(signal.SIGTERM, handler)
    await mcp_server.run_stdio_async()


async def run_agent_with_mcp_client(run_agent):
    env = os.environ.copy()
    # Make sure PYTHONPATH is set to the same as what started this
    # process. Notably, opentelemetry-instrument removes itself from the value
    # in os.environ and we'd like to restore it if it was used.
    env["PYTHONPATH"] = os.pathsep.join(sys.path)
    async with MCPServerStdio(
        {
            "command": sys.executable,
            "args": sys.argv + [SERVER_ARG],
            "env": env,
        }
    ) as mcp_client:
        await run_agent(mcp_servers=[mcp_client])


async def mcp_client_main(run_agent, tools, is_server):
    if is_server:
        await mcp_server_main(tools)
    else:
        await run_agent_with_mcp_client(run_agent)
