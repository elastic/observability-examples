import os

import httpx
from agents import (
    Agent,
    ModelSettings,
    OpenAIProvider,
    RunConfig,
    Runner,
    function_tool,
)
from agents.tracing import GLOBAL_TRACE_PROVIDER

# Shut down the global tracer as it sends to the OpenAI "/traces/ingest"
# endpoint, which we aren't using and doesn't exist on alternative backends
# like Ollama.
GLOBAL_TRACE_PROVIDER.shutdown()


@function_tool(strict_mode=False)
def get_latest_elasticsearch_version(major_version: int = 0) -> str:
    """Returns the latest GA version of Elasticsearch in "X.Y.Z" format.

    Args:
        major_version: Major version to filter by (e.g. 7, 8). Defaults to latest
    """
    response = httpx.get("https://artifacts.elastic.co/releases/stack.json")
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


def main():
    model_name = os.getenv("CHAT_MODEL", "gpt-4o-mini")
    model = OpenAIProvider(use_responses=False).get_model(model_name)
    agent = Agent(
        name="version_assistant",
        tools=[get_latest_elasticsearch_version],
        model=model,
        model_settings=ModelSettings(temperature=0),
    )

    result = Runner.run_sync(
        starting_agent=agent,
        input="What is the latest version of Elasticsearch 8?",
        run_config=RunConfig(workflow_name="GetLatestElasticsearchVersion"),
    )
    print(result.final_output)


if __name__ == "__main__":
    main()
