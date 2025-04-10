import asyncio
import contextlib
import httpx
from mcp.server.fastmcp import FastMCP
import uvicorn

server: uvicorn.Server
server_task: asyncio.Task


@contextlib.asynccontextmanager
async def mcp_server(tools):
    mcp_server = FastMCP(log_level="WARNING")
    for tool in tools:
        mcp_server.add_tool(tool)
    # Manually setup uvicorn to allow shutting it down
    config = uvicorn.Config(
        mcp_server.sse_app(),
        host="localhost",
        port=8000,
        log_level="critical",  # To suppress an SSE background task cancellation ERROR
        timeout_graceful_shutdown=1,
    )
    server = uvicorn.Server(config)
    server_task = asyncio.create_task(server.serve())
    # Wait for the server to start
    async with httpx.AsyncClient() as client:
        while True:
            try:
                await client.get("http://localhost:8000/")
                break
            except httpx.ConnectError:
                pass
    try:
        yield
    finally:
        server.should_exit = True
        await server_task
