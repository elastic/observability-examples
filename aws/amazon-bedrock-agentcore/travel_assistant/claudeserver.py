import os
import logging
import time
from bedrock_agentcore.runtime import BedrockAgentCoreApp
from strands import Agent, tool
from strands.models import BedrockModel
from strands.telemetry import StrandsTelemetry
from tavily import TavilyClient
from duckduckgo_search import DDGS

# Optional OpenTelemetry imports for custom resource configuration
try:
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry import trace as trace_api
    from opentelemetry import propagate
    from opentelemetry.baggage.propagation import W3CBaggagePropagator
    from opentelemetry.propagators.composite import CompositePropagator
    from opentelemetry.trace.propagation.tracecontext import (
        TraceContextTextMapPropagator,
    )

    OTEL_AVAILABLE = True
except ImportError:
    OTEL_AVAILABLE = False

logging.basicConfig(level=logging.ERROR, format="[%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)
logger.setLevel(os.getenv("AGENT_RUNTIME_LOG_LEVEL", "INFO").upper())


@tool
def web_search(query: str) -> str:
    """
    Search the web for information using Tavily Search API.

    Args:
        query: The search query

    Returns:
        A string containing the search results
    """
    try:
        # Get Tavily API key from environment variable
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            return "Error: TAVILY_API_KEY environment variable not set. Please sign up at https://tavily.com to get your API key."

        tavily_client = TavilyClient(api_key=api_key)
        response = tavily_client.search(query, max_results=5)

        # Extract results from Tavily response
        results = response.get("results", [])

        formatted_results = []
        for i, result in enumerate(results, 1):
            formatted_results.append(
                f"{i}. {result.get('title', 'No title')}\n"
                f"   {result.get('content', 'No summary')}\n"
                f"   Source: {result.get('url', 'No URL')}\n"
            )

        return "\n".join(formatted_results) if formatted_results else "No results found."

    except Exception as e:
        return f"Error searching the web: {str(e)}"


@tool
def web_search_ddg(query: str) -> str:
    """
    Search the web for information using DuckDuckGo Search.

    Args:
        query: The search query

    Returns:
        A string containing the search results
    """
    try:
        # Initialize DuckDuckGo search client
        ddgs = DDGS()

        # Perform search with max_results=5
        results = list(ddgs.text(query, max_results=5))

        formatted_results = []
        for i, result in enumerate(results, 1):
            formatted_results.append(
                f"{i}. {result.get('title', 'No title')}\n"
                f"   {result.get('body', 'No summary')}\n"
                f"   Source: {result.get('href', 'No URL')}\n"
            )

        return "\n".join(formatted_results) if formatted_results else "No results found."

    except Exception as e:
        return f"Error searching the web with DuckDuckGo: {str(e)}"


@tool
def country_specific_search(query: str) -> str:
    """
    Search for best places to visit in India with a 120-second delay before performing the search.
    This tool waits for 2 minutes before executing a Tavily search about India travel destinations.

    Args:
        query: The search query (should be about best places to visit in India)

    Returns:
        A string containing the search results after the delay
    """
    try:
        logger.info("Delayed India search initiated. Waiting 120 seconds before performing search...")

        # Wait for 120 seconds
        time.sleep(120)

        logger.info("Wait complete. Performing Tavily search for India destinations...")

        # Get Tavily API key from environment variable
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            return "Error: TAVILY_API_KEY environment variable not set. Please sign up at https://tavily.com to get your API key."

        # Perform the search specifically about best places to visit in India
        tavily_client = TavilyClient(api_key=api_key)
        search_query = f"best places to visit in India {query}"
        response = tavily_client.search(search_query, max_results=5)

        # Extract results from Tavily response
        results = response.get("results", [])

        formatted_results = ["[DELAYED SEARCH - Waited 120 seconds before executing]\n"]
        for i, result in enumerate(results, 1):
            formatted_results.append(
                f"{i}. {result.get('title', 'No title')}\n"
                f"   {result.get('content', 'No summary')}\n"
                f"   Source: {result.get('url', 'No URL')}\n"
            )

        return "\n".join(formatted_results) if len(formatted_results) > 1 else "No results found after delayed search."

    except Exception as e:
        return f"Error in delayed India search: {str(e)}"


# Function to initialize Bedrock model
def get_bedrock_model():
    region = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
    model_id = os.getenv("BEDROCK_MODEL_ID", "us.anthropic.claude-3-5-sonnet-20240620-v1:0")

    bedrock_model = BedrockModel(model_id=model_id, region_name=region, temperature=0.0, max_tokens=1024)
    return bedrock_model


# Initialize the Bedrock model
bedrock_model = get_bedrock_model()


# Define the agent's system prompt
system_prompt = """You are an experienced travel agent specializing in personalized travel recommendations 
with access to real-time web information from multiple search engines. Your role is to find dream destinations 
matching user preferences by using BOTH available search tools to gather comprehensive information.

IMPORTANT: When responding to queries:
1. Use BOTH web_search (Tavily) and web_search_ddg (DuckDuckGo) tools for each query
2. Clearly identify results from each search engine in your response
3. Format your response to show:
   - Results from Tavily Search (use web_search)
   - Results from DuckDuckGo Search (use web_search_ddg)
4. SPECIAL CASE: If someone asks specifically about "best places to visit in India", use the 
   country_specific_search tool which will wait 120 seconds before performing a specialized Tavily search
5. Synthesize information from both sources to provide comprehensive recommendations with current 
   information, brief descriptions, and practical travel details."""


app = BedrockAgentCoreApp()


def initialize_agent():
    """Initialize the agent with proper telemetry configuration."""

    if OTEL_AVAILABLE:
        try:
            # Create a custom resource that respects OTEL_RESOURCE_ATTRIBUTES from environment
            # This will automatically merge env vars with any explicit attributes
            custom_resource = Resource.create(
                attributes={
                    "telemetry.sdk.name": "opentelemetry",
                    "telemetry.sdk.language": "python",
                }
            )

            # Create a custom tracer provider with our resource
            tracer_provider = TracerProvider(resource=custom_resource)

            # Set as global tracer provider (required for traces to work)
            trace_api.set_tracer_provider(tracer_provider)

            # Set up propagators (required for distributed tracing)
            propagate.set_global_textmap(
                CompositePropagator(
                    [
                        W3CBaggagePropagator(),
                        TraceContextTextMapPropagator(),
                    ]
                )
            )

            # Initialize Strands telemetry with the custom tracer provider
            strands_telemetry = StrandsTelemetry(tracer_provider=tracer_provider)
            strands_telemetry.setup_otlp_exporter()

            logger.info("Strands telemetry initialized with custom resource attributes")
            logger.info(f"Resource attributes: {custom_resource.attributes}")
        except Exception as e:
            logger.warning("Telemetry setup failed: %s", str(e))
    else:
        logger.warning("Telemetry setup skipped - OpenTelemetry packages not available")

    # Create and cache the agent
    agent = Agent(
        model=bedrock_model,
        system_prompt=system_prompt,
        tools=[web_search, web_search_ddg, country_specific_search],
    )

    return agent


@app.entrypoint
def strands_agent_bedrock(payload, context=None):
    """
    Invoke the agent with a payload
    """
    user_input = payload.get("prompt")
    logger.info("[%s] User input: %s", context.session_id, user_input)

    # Initialize agent with proper configuration
    agent = initialize_agent()

    response = agent(user_input)
    return response.message["content"][0]["text"]


if __name__ == "__main__":
    app.run()
