# Function Calling in Generative AI Agents

Generative AI (GenAI) frameworks empower developers to build applications that
handle tasks beyond the large language models (LLMs) core knowledge.

Here are some GenAI frameworks features that contribute to choice and velocity:
* Standardized interfaces for LLMs and VectorDBs
* Tool/function support retrieving new knowledge or executing tasks
* Orchestration of common patterns, such as RAG or agent function calling loops

This directory contains examples of the GenAI agent function calling loop
pattern, applied to several frameworks in multiple languages. Notably, this
includes observability using Elastic Distributions of OpenTelemetry (EDOT) SDKs
and Kibana.

Here are the examples:

* [OpenAI Agents SDK (Python)](openai-agents)
* [Semantic Kernel .NET](semantic-kernel-dotnet)
* [Spring AI (Java)](spring-ai)
* [Vercel AI (Node.js)](vercel-ai)

## Example application flow

Regardless of programming language or GenAI framework in use, each example
performs the same process. The user asks a question that is beyond the training
date of the LLM. The application uses the framework to implement an agent
pattern to automatically call functions when it needs new information.

Here's how the question "What is the latest version of Elasticsearch 8?" ends up
being answered.

```mermaid
sequenceDiagram
    participant Agent
    participant LLM

    Note over Agent: Framework sends its tools along with the prompt
    Agent ->> LLM: user: "What is the latest version of Elasticsearch 8?"
    activate LLM
    Note over LLM: LLM determines it needs to use a tool to complete the task

    LLM ->> Agent: assistant: {"function": {"name": "get_latest_elasticsearch_version", "arguments": "{\"majorVersion\": 8}"}}
    deactivate LLM
    activate Agent
    Note over Agent: invokes get_latest_elasticsearch_version(majorVersion=8)

    Agent ->> LLM: [user, assistant, tool: "8.18.0"]
    Note over Agent: LLM is stateless, the tool result is sent back with prior messages
    deactivate Agent
    activate LLM

    LLM ->> Agent: content: "The latest version of Elasticsearch 8 is 8.18.0"
    deactivate LLM
    Note over Agent: "The latest version of Elasticsearch 8 is 8.18.0"
```

The GenAI framework not only abstracts the above loop, but also LLM plugability
and tool registration. This simplifies swapping out LLMs and also enables
flexibility in defining and testing functions.

> [!NOTE]
> LLM interactions above follow OpenAI's [Chat Completions API][openai-chat]. This is the
> most implemented LLM API. In March 2025, OpenAI announced a stateful
> [Responses API][openai-responses], which doesn't require passing prior messages in subsequent
> calls to the LLM. Once [Ollama supports this][ollama-responses], we'll update examples and
> diagrams accordingly.

## Observability with EDOT

The OpenTelemetry instrumentation approach varies per GenAI framework. Some are
[native][native] (their codebase includes OpenTelemetry code), while others
rely on external instrumentation libraries. Signals vary as well. While all
produce traces, only some produce logs or metrics.

We use Elastic Distributions of OpenTelemetry (EDOT) SDKs to enable these
features and fill in other data, such as HTTP requests underlying the LLM and
tool calls. In doing so, this implements the "zero code instrumentation"
pattern of OpenTelemetry.

Here's an example Kibana screenshot of one of the examples, looked up from a
query like:

http://localhost:5601/app/apm/traces?rangeFrom=now-15m&rangeTo=now

![Kibana screenshot](./kibana-trace.png)

## Prerequisites

Docker or Podman is required. You'll also need an OpenAI API compatible
inference platform and an OpenTelemetry collector.

First of all, you need to be in a directory that contains this repository. If
you haven't yet, you get one like this:
```bash
curl -L https://github.com/elastic/observability-examples/archive/refs/heads/main.tar.gz | tar -xz
cd observability-examples-main/genai-function-calling/
```

### Podman

If you are using [Podman](https://podman.io/) to run docker containers, export
`HOST_IP`. If you don't you'll get this error running exercises:
> unable to upgrade to tcp, received 500

Here's how to export your `HOST_IP`:
  * If macOS: `export HOST_IP=$(ipconfig getifaddr en0)`
  * If Ubuntu: `export HOST_IP=$(hostname -I | awk '{print $1}')`

## Model Context Protocol flow

Some examples optionally use Model Context Protocol ([MCP][mcp]) for tool
discovery and execution.

This uses the "stdio" transport which involves launching a subprocess. For
convenience, the MCP server is defined in the same project as the normal
example.

The main difference is that instead of calling a local function to get the
latest version of Elasticsearch, the agent creates and MCP server process and
discovers the function via the MCP protocol. When the LLM uses that function,
it uses the same protocol to invoke the function. Otherwise, the flow is the
same.

Here's a diagram of the MCP variant, which notably augments the original by
decoupling tool discovery and execution from the agent, which is now also an
MCP client. MCP-related interactions are highlighted for emphasis.

```mermaid
sequenceDiagram
    participant Agent as Agent (MCP Client)

    rect rgb(191, 223, 255)
    activate LLM
    create participant MCP as MCP Server (subprocess)
    Agent->>+MCP: create stdio client transport
    Agent->>+MCP: initialize: {clientInfo, protocolVersion}
    MCP-->>-Agent: response: {capabilities, instructions, serverInfo}
    Agent->>+MCP: tools/list
    MCP-->>-Agent: response: {tools: [{name: "get_latest_elasticsearch_version", ...}]}
    end

    create participant LLM

    Agent->>LLM: user: "What is the latest version of Elasticsearch 8?"
    activate LLM
    LLM->>Agent: assistant: {"function": {"name": "get_latest_elasticsearch_version", "arguments": "{\"majorVersion\": 8}"}}
    deactivate LLM
    activate Agent

    rect rgb(191, 223, 255)
    Agent->>+MCP: tools/call: {get_latest_elasticsearch_version, {majorVersion: 8}}
    MCP-->>-Agent: response: {output: "8.18.0"}
    end

    Agent->>LLM: [user, assistant, tool: "8.18.0"]
    deactivate Agent
    activate LLM
    LLM->>Agent: content: "The latest version of Elasticsearch 8 is 8.18.0"
    deactivate LLM
```

> [!NOTE]
> How to join traces across MCP client-server transports is not yet
> standardized. While most here support a compatible approach, your framework
> might not and result in split traces. Please follow this [pull request][mcp-otel]
> to the MCP specification for updates.

---
[openai-chat]: https://platform.openai.com/docs/api-reference/chat
[openai-responses]: https://platform.openai.com/docs/api-reference/responses
[ollama-responses]: https://github.com/ollama/ollama/issues/10309
[native]: https://opentelemetry.io/docs/languages/java/instrumentation/#native-instrumentation
[mcp]: https://modelcontextprotocol.io/specification
[mcp-otel]: https://github.com/modelcontextprotocol/modelcontextprotocol/pull/414
