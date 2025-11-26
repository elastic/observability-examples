# Travel Assistant Agent

A multi-search travel recommendation agent built with AWS Bedrock AgentCore, Strands, and multiple search providers. This agent compares search latency and results between **Tavily** and **DuckDuckGo** search engines to provide comprehensive travel recommendations.

## Overview

This travel assistant agent demonstrates:

- **Dual Search Engine Integration**: Simultaneously uses Tavily and DuckDuckGo to compare search performance and results
- **Latency Comparison**: Measures and compares response times between different search providers
- **Custom Tool with Delay**: Includes a special `country_specific_search` tool with intentional delay for testing long-running operations
- **Observability**: Full integration with Elastic Observability for monitoring and tracing
- **AWS Bedrock Integration**: Uses Claude 3.5 Sonnet via AWS Bedrock for intelligent travel recommendations

## Features

### Search Tools

1. **web_search (Tavily)**: Fast, AI-optimized search using Tavily Search API
2. **web_search_ddg (DuckDuckGo)**: Traditional web search using DuckDuckGo
3. **country_specific_search**: Specialized tool for India travel searches with 120-second delay

### Country-Specific Search Logic

The `country_specific_search` tool includes a **120-second delay** before executing. This is designed to:

- **Test Long-Running Operations**: Simulate real-world scenarios where certain operations take extended time
- **Observability Testing**: Validate that tracing and monitoring correctly handle long-duration spans
- **Timeout Handling**: Test the agent's behavior with slow-responding tools
- **User Experience Testing**: Demonstrate how to handle operations that require significant wait times

The delay is intentional and serves as a testing mechanism for production-grade agent deployments where some operations may naturally take longer.

## Architecture

```
┌─────────────────┐
│  AgentCore      │
│  Runtime        │
└────────┬────────┘
         │
         v
┌─────────────────┐     ┌──────────────┐
│  Strands Agent  │────>│  Claude 3.5  │
│                 │     │  (Bedrock)   │
└────────┬────────┘     └──────────────┘
         │
         ├────> Tavily Search (Fast)
         ├────> DuckDuckGo Search (Comparison)
         └────> Country-Specific Search (Delayed)
```

## Prerequisites

- AWS Account with Bedrock access
- Python 3.11+
- Docker (optional, for containerized deployment)
- AgentCore CLI installed

## Setup Instructions

### 1. Install AgentCore SDK

```bash
pip install bedrock-agentcore
```

**Note**: The `agentcore` CLI command requires the Bedrock AgentCore Starter Toolkit, which may need to be installed separately or accessed through AWS preview programs.

### 2. Obtain Tavily API Key

1. Visit [https://tavily.com](https://tavily.com)
2. Sign up for a free account
3. Navigate to your dashboard
4. Copy your API key from the API Keys section
5. Free tier includes 1,000 searches per month

### 3. Set Up Elastic Observability (Optional but Recommended)

#### Create Elastic Serverless Account

1. Go to [https://cloud.elastic.co](https://cloud.elastic.co)
2. Click "Start free trial" or "Sign up"
3. Choose "Serverless" deployment option
4. Select your cloud provider and region
5. Create your deployment (usually takes 1-2 minutes)

#### Obtain Elastic API Key

1. Once your Elastic deployment is ready, navigate to your deployment
2. Go to **Management** > **Stack Management** > **API Keys**
3. Click **"Create API Key"**
4. Give it a name (e.g., "AgentCore Observability")
5. Set appropriate privileges or use default
6. Click **Create API Key**
7. **Copy and save** the API key immediately (you won't be able to see it again)

#### Get OTLP Endpoint

1. In your Elastic deployment, go to **Observability** > **APM**
2. Click **"Add data"**
3. Select **"OpenTelemetry"**
4. Copy the **OTLP Endpoint URL** displayed (format: `https://<deployment-id>.ingest.<region>.cloud.elastic.co:443`)

### 4. Configure AWS Credentials

Ensure your AWS credentials are configured. You can use AWS CLI configuration:

```bash
aws configure
```

Or set environment variables directly (required for agentcore CLI):

```bash
export AWS_ACCESS_KEY_ID=your-aws-access-key-id
export AWS_SECRET_ACCESS_KEY=your-aws-secret-access-key
export AWS_REGION=us-east-1
export AWS_PROFILE=your-aws-profile  # Optional, if using AWS profiles
```

**Note**: The agentcore CLI requires these environment variables to be set before running configuration and deployment commands.

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure AgentCore (CLI Method)

**If you have access to the `agentcore` CLI**, first set your AWS credentials:

```bash
# Set AWS credentials for AgentCore
export AWS_ACCESS_KEY_ID=your-aws-access-key-id
export AWS_SECRET_ACCESS_KEY=your-aws-secret-access-key
export AWS_REGION=us-east-1
export AWS_PROFILE=your-aws-profile  # Optional, if using AWS profiles
```

Then configure the entrypoint:

```bash
agentcore configure --entrypoint claudeserver.py --name travel_assistant_quickstart
```

This command:
- Sets `claudeserver.py` as the agent entrypoint
- Names the agent `travel_assistant_quickstart`
- Configures the runtime environment
- Creates `.bedrock_agentcore.yaml` configuration file (excluded from git)

## Configuration

### Environment Variables

Create a `.env` file or export the following:

```bash
# Required
export TAVILY_API_KEY="your-tavily-api-key-here"

# Optional - AWS Configuration
export AWS_DEFAULT_REGION="us-east-1"
export BEDROCK_MODEL_ID="us.anthropic.claude-3-5-sonnet-20240620-v1:0"

# Optional - Observability (Elastic)
export OTEL_EXPORTER_OTLP_ENDPOINT="https://your-deployment-id.ingest.region.cloud.elastic.co:443"
export OTEL_EXPORTER_OTLP_HEADERS="Authorization=ApiKey your-elastic-api-key-here"
export OTEL_EXPORTER_OTLP_PROTOCOL="http/protobuf"
export OTEL_METRICS_EXPORTER="otlp"
export OTEL_TRACES_EXPORTER="otlp"
export OTEL_LOGS_EXPORTER="otlp"
export OTEL_RESOURCE_ATTRIBUTES="service.name=travel_assistant,service.version=1.0.0,deployment.environment=production"
export AGENT_OBSERVABILITY_ENABLED="true"
export DISABLE_ADOT_OBSERVABILITY="true"

# Optional - Logging
export AGENT_RUNTIME_LOG_LEVEL="INFO"
```

## Launching the Agent

**Important**: Make sure you've run `agentcore configure --entrypoint claudeserver.py --name travel_assistant_quickstart` before launching (see step 6 above).

### Basic Launch (Without Observability)

```bash
agentcore launch --env TAVILY_API_KEY="your-tavily-api-key"
```

### Full Launch (With Elastic Observability)

```bash
agentcore launch \
  --env OTEL_EXPORTER_OTLP_ENDPOINT="https://<your-deployment-id>.ingest.<region>.cloud.elastic.co:443" \
  --env OTEL_EXPORTER_OTLP_HEADERS="Authorization=ApiKey <your-elastic-api-key>" \
  --env OTEL_EXPORTER_OTLP_PROTOCOL="http/protobuf" \
  --env OTEL_METRICS_EXPORTER="otlp" \
  --env OTEL_TRACES_EXPORTER="otlp" \
  --env OTEL_LOGS_EXPORTER="otlp" \
  --env OTEL_RESOURCE_ATTRIBUTES="service.name=travel_assistant_quickstart,service.version=1.0.0,deployment.environment=production" \
  --env AGENT_OBSERVABILITY_ENABLED="true" \
  --env DISABLE_ADOT_OBSERVABILITY="true" \
  --env TAVILY_API_KEY="<your-tavily-api-key>"
```

**Note**: Replace placeholders (`<...>`) with your actual credentials.

## Testing the Agent

### Regular Search (Netherlands Example)

This will use both Tavily and DuckDuckGo search engines:

```bash
./invoke.sh
```

Or manually:

```bash
START=$(date +%s)
agentcore invoke '{"prompt":"Best places to visit in Netherlands"}'
END=$(date +%s)
echo "Time taken: $((END - START)) seconds"
```

### Delayed Search (India Example)

This triggers the `country_specific_search` tool with 120-second delay:

```bash
./invoke_india_best_places.sh
```

Or manually:

```bash
START=$(date +%s)
agentcore invoke '{"prompt":"Best places to visit in India"}'
END=$(date +%s)
echo "Time taken: $((END - START)) seconds"
```

**Expected behavior**: The India search will take approximately 120+ seconds due to the intentional delay in the `country_specific_search` tool.

## Comparing Search Latency

The agent is designed to compare latency between:

1. **Tavily Search** (`web_search`): Typically faster, optimized for AI applications
2. **DuckDuckGo Search** (`web_search_ddg`): Traditional web search, may vary in speed

The agent will call both search engines for most queries, allowing you to observe:
- Response time differences
- Result quality differences
- API reliability

You can monitor these metrics in Elastic Observability if configured.

## Project Structure

```
travel_assistant/
├── claudeserver.py                 # Main agent implementation
├── requirements.txt                # Python dependencies
├── Dockerfile                      # Container configuration
├── .dockerignore                   # Docker ignore patterns
├── .gitignore                      # Git ignore patterns
├── LICENSE                         # MIT License
├── README.md                       # This file
├── QUICKSTART.md                   # 5-minute setup guide
├── CONTRIBUTING.md                 # Contribution guidelines
├── env.example                     # Environment template
├── invoke.sh                       # Test script (Netherlands)
├── invoke_india_best_places.sh     # Test script (India with delay)
└── launch_with_observability.sh    # Full launch script with observability
```

## Key Components

### claudeserver.py

- **Tools**: Three search tools (Tavily, DuckDuckGo, Country-specific)
- **Agent**: Strands Agent with Claude 3.5 Sonnet
- **Telemetry**: OpenTelemetry integration for observability
- **Entrypoint**: BedrockAgentCore app entrypoint


## Observability

When Elastic Observability is configured, you can monitor:

- **Traces**: Full execution traces including tool calls
- **Metrics**: Performance metrics, latency distributions
- **Logs**: Structured logs from the agent
- **Spans**: Individual operation timing (search calls, LLM calls, etc.)

Access your Elastic deployment to view:
- APM (Application Performance Monitoring)
- Service maps
- Trace timelines
- Error tracking

## Docker Deployment

### Build the Image

```bash
docker build -t travel-assistant .
```

### Run the Container

```bash
docker run -p 8080:8080 \
  -e TAVILY_API_KEY="your-tavily-api-key" \
  -e AWS_ACCESS_KEY_ID="your-aws-key" \
  -e AWS_SECRET_ACCESS_KEY="your-aws-secret" \
  -e AWS_DEFAULT_REGION="us-east-1" \
  travel-assistant
```

## Troubleshooting

### Common Issues

1. **agentcore: command not found**
   - Install the Bedrock AgentCore Starter Toolkit: `pip install bedrock-agentcore-starter-toolkit`
   - Verify installation: `agentcore --help`

2. **Tavily API Key Error**
   - Ensure `TAVILY_API_KEY` is set correctly
   - Verify your API key is active at tavily.com

3. **AWS Bedrock Access Denied**
   - Enable Bedrock model access in AWS Console
   - Verify IAM permissions for Bedrock

4. **Observability Not Working**
   - Check Elastic OTLP endpoint is accessible
   - Verify API key has correct permissions
   - Ensure OTEL environment variables are set

5. **Timeout on India Search**
   - This is expected! The tool has a 120-second delay
   - Ensure your timeout settings are >= 130 seconds


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please ensure:
- Code follows existing style
- Tests pass
- Documentation is updated
- No sensitive credentials in commits

## Security Notes

- Never commit API keys or credentials
- Use environment variables for sensitive data
- Rotate API keys regularly
- Use AWS Secrets Manager for production deployments

## Support

For issues or questions:
- AWS Bedrock AgentCore: [AWS Documentation](https://docs.aws.amazon.com/bedrock/)
- Tavily API: [Tavily Documentation](https://docs.tavily.com/)
- Elastic Observability: [Elastic Documentation](https://www.elastic.co/guide/)
