# run like this: uv run --exact -q --env-file .env agent.py
# /// script
# dependencies = [
#     "openai-agents",
#     "httpx",
#     "mcp",
#     "elastic-opentelemetry",
#     "openinference-instrumentation-openai-agents",
#     "opentelemetry-instrumentation-httpx",
#     "openinference-instrumentation-mcp",
# ]
# ///
from opentelemetry.instrumentation import auto_instrumentation

# This must precede any other imports you want to instrument!
auto_instrumentation.initialize()

import asyncio
import os

from agents import (
    Agent,
    OpenAIProvider,
    RunConfig,
    Runner,
    Tool,
)
from agents.mcp import MCPServerStreamableHttp, MCPUtil


async def run_agent(tools: list[Tool]):
    model_name = os.getenv("AGENT_MODEL", "gpt-5-nano")
    model = OpenAIProvider(use_responses=False).get_model(model_name)
    agent = Agent(
        name="flight-search-agent",
        model=model,
        tools=tools,
    )

    result = await Runner.run(
        starting_agent=agent,
        input="Give me the best flight from New York to Kota Kinabalu on 2025-10-10",
        run_config=RunConfig(workflow_name="flight search"),
    )
    print(result.final_output)


async def main():
    mcp_url = os.getenv("MCP_URL", "https://mcp.kiwi.com")
    async with MCPServerStreamableHttp(
        {
            "url": mcp_url,
            "timeout": 30.0,
        },
        cache_tools_list=True,
        client_session_timeout_seconds=60.0,
    ) as server:
        tools = await server.list_tools()
        util = MCPUtil()
        tools = [util.to_function_tool(tool, server, False) for tool in tools]
        await run_agent(tools)


if __name__ == "__main__":
    asyncio.run(main())
