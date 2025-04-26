import signal
from typing import Callable, Awaitable

from agents.mcp import MCPServerStdio, MCPUtil
from mcp.server.fastmcp import FastMCP
import os
import sys

from mcp.types import AnyFunction, Tool

SERVER_ARG = "--mcp-server"


def handler(signum, frame):
    sys.exit(0)


async def server_main(fns: list[AnyFunction]):
    """Runs an MCP server which publishes the tool get_latest_elasticsearch_version."""

    mcp_server = FastMCP(log_level="WARNING")
    for fn in fns:
        mcp_server.add_tool(fn)
    # Mysteriously, cleanup such as from opentelemetry-instrument does not run on exit
    # without registering an effectively no-op termination handler.
    signal.signal(signal.SIGTERM, handler)
    await mcp_server.run_stdio_async()


async def client_main(tools_callback: Callable[[list[Tool]], Awaitable[None]]):
    """Starts an MCP server subprocess and invokes tools_callback with its tools."""

    env = os.environ.copy()
    # Make sure PYTHONPATH is set to the same as what started this
    # process. Notably, opentelemetry-instrument removes itself from the value
    # in os.environ, and we'd like to restore it if it was used.
    env["PYTHONPATH"] = os.pathsep.join(sys.path)
    async with MCPServerStdio(
        {
            "command": sys.executable,
            "args": sys.argv + [SERVER_ARG],
            "env": env,
        }
    ) as server:
        tools = await server.list_tools()
        util = MCPUtil()
        tools = [util.to_function_tool(tool, server, False) for tool in tools]
        await tools_callback(tools)


async def run_main(fns: list[AnyFunction], tools_callback: Callable[[list[Tool]], Awaitable[None]]):
    if SERVER_ARG in sys.argv:
        await server_main(fns)
    else:
        await client_main(tools_callback)
