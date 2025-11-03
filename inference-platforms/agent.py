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
# ruff: noqa: E402
from opentelemetry.instrumentation import auto_instrumentation

# This must precede any other imports you want to instrument!
auto_instrumentation.initialize()

import argparse
import asyncio
import os
from datetime import datetime, timedelta

from agents import (
    Agent,
    HostedMCPTool,
    OpenAIProvider,
    RunConfig,
    Runner,
    Tool,
)
from agents.mcp import MCPServerStreamableHttp, MCPUtil
from openai.types.responses.tool_param import Mcp


async def run_agent(tools: list[Tool], model_name: str, use_responses: bool):
    model = OpenAIProvider(use_responses=use_responses).get_model(model_name)
    agent = Agent(
        name="flight-search-agent",
        model=model,
        tools=tools,
    )

    next_week = (datetime.now() + timedelta(weeks=1)).strftime("%Y-%m-%d")
    result = await Runner.run(
        starting_agent=agent,
        input=f"Give me the best flight from New York to Kota Kinabalu on {next_week}",
        run_config=RunConfig(workflow_name="flight search"),
    )
    print(result.final_output)


async def main():
    parser = argparse.ArgumentParser(description="MCP-enabled flight search agent")
    parser.add_argument("--use-responses-api", action="store_true", help="Use Responses API instead of Agents")
    args = parser.parse_args()

    model_name = os.getenv("AGENT_MODEL", "gpt-5-nano")
    mcp_url = os.getenv("MCP_URL", "https://mcp.kiwi.com")
    mcp_headers = dict(h.split("=", 1) for h in os.getenv("MCP_HEADERS", "").split(",") if h)

    if args.use_responses_api:
        # Server-side MCP via Responses API
        tools = [
            HostedMCPTool(
                tool_config=Mcp(
                    type="mcp",
                    server_url=mcp_url,
                    server_label="kiwi-flights",
                    headers=mcp_headers,
                    require_approval="never",
                )
            )
        ]
        await run_agent(tools, model_name, use_responses=True)
        return

    # Client-side MCP orchestration
    async with MCPServerStreamableHttp(
        {"url": mcp_url, "headers": mcp_headers, "timeout": 30.0},
        client_session_timeout_seconds=60.0,
    ) as server:
        tools = await server.list_tools()
        util = MCPUtil()
        tools = [util.to_function_tool(tool, server, False) for tool in tools]
        await run_agent(tools, model_name, use_responses=False)


if __name__ == "__main__":
    asyncio.run(main())
