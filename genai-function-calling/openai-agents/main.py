import asyncio
import os
import sys

from httpx import AsyncClient
from agents import (
    Agent,
    ModelSettings,
    OpenAIProvider,
    RunConfig,
    Runner,
    function_tool,
    Tool,
)
from agents.tracing import set_tracing_disabled
from openai import AsyncAzureOpenAI

from main_mcp import run_main as mcp_main

# Disable the default tracer as it sends to the OpenAI "/traces/ingest"
# endpoint, which we aren't using and doesn't exist on alternative backends
# like Ollama.
set_tracing_disabled(True)


async def get_latest_elasticsearch_version(major_version: int = 0) -> str:
    """Returns the latest GA version of Elasticsearch in "X.Y.Z" format.

    Args:
        major_version: Major version to filter by (e.g. 7, 8). Defaults to latest
    """
    async with AsyncClient() as client:
        response = await client.get("https://artifacts.elastic.co/releases/stack.json")
    response.raise_for_status()
    releases = response.json()["releases"]

    # Fetch releases and filter out non-release versions (e.g., -rc1) or
    # those not matching major_version. In any case, remove " GA" suffix.
    versions = []
    for r in releases:
        v = r["version"].removesuffix(" GA")
        if "-" in r["version"]:
            continue
        if major_version and int(v.split(".")[0]) != major_version:
            continue
        versions.append(v)

    if not versions:
        raise ValueError("No valid versions found")

    # "8.9.1" > "8.10.0", so coerce to a numeric tuple: (8,9,1) < (8,10,0)
    return max(versions, key=lambda v: tuple(map(int, v.split("."))))


async def run_agent(tools: list[Tool]):
    model_name = os.getenv("CHAT_MODEL", "gpt-4o-mini")
    openai_client = AsyncAzureOpenAI() if os.getenv("AZURE_OPENAI_API_KEY") else None
    model = OpenAIProvider(openai_client=openai_client, use_responses=False).get_model(model_name)
    agent = Agent(
        name="version_assistant",
        model=model,
        model_settings=ModelSettings(temperature=0),
        tools=tools,
    )

    result = await Runner.run(
        starting_agent=agent,
        input="What is the latest version of Elasticsearch 8?",
        run_config=RunConfig(workflow_name="GetLatestElasticsearchVersion"),
    )
    print(result.final_output)


async def main():
    """Run tools with the agent directly unless in MCP mode"""

    fns = [get_latest_elasticsearch_version]
    if any(arg.startswith("--mcp") for arg in sys.argv):
        await mcp_main(fns, run_agent)  # start an MCP server and use its tools
    else:  # run the tools directly
        await run_agent([function_tool(strict_mode=False)(fn) for fn in fns])


if __name__ == "__main__":
    asyncio.run(main())
