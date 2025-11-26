# Quick Start Guide

Get the Travel Assistant Agent running in 5 minutes!

## Prerequisites Checklist

- [ ] Python 3.11+ installed
- [ ] AWS Account with Bedrock access
- [ ] AWS CLI configured (`aws configure`)
- [ ] Bedrock AgentCore SDK installed (`pip install bedrock-agentcore`)
- [ ] (Optional) AgentCore CLI access for deployment

## Step 1: Get API Keys

### Tavily API Key (Required)
1. Visit [https://tavily.com](https://tavily.com)
2. Sign up and get your API key
3. Save it for the next step

### Elastic API Key (Optional - for observability)
1. Visit [https://cloud.elastic.co](https://cloud.elastic.co)
2. Create a serverless deployment
3. Go to Management > API Keys > Create API Key
4. Save the key and OTLP endpoint

## Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 3: Configure Environment

```bash
# Option 1: Export directly
export TAVILY_API_KEY="your-key-here"

# Option 2: Create .env file
cp env.example .env
# Edit .env with your values
```

## Step 4: Launch the Agent

Choose one of the following methods:

**Note**: Requires access to the `agentcore` CLI tool from Bedrock AgentCore Starter Toolkit.

1. Set AWS credentials (required before running agentcore):
```bash
export AWS_ACCESS_KEY_ID=your-aws-access-key-id
export AWS_SECRET_ACCESS_KEY=your-aws-secret-access-key
export AWS_REGION=us-east-1
export AWS_PROFILE=your-aws-profile  # Optional
```

2. Configure the entrypoint:
```bash
agentcore configure --entrypoint claudeserver.py --name travel_assistant_quickstart
```

3. Launch with minimal config:
```bash
agentcore launch --env TAVILY_API_KEY="your-tavily-key"
```

4. Or launch with full observability:
```bash
agentcore launch \
  --env OTEL_EXPORTER_OTLP_ENDPOINT="https://your-id.ingest.region.cloud.elastic.co:443" \
  --env OTEL_EXPORTER_OTLP_HEADERS="Authorization=ApiKey your-elastic-key" \
  --env OTEL_EXPORTER_OTLP_PROTOCOL="http/protobuf" \
  --env OTEL_METRICS_EXPORTER="otlp" \
  --env OTEL_TRACES_EXPORTER="otlp" \
  --env OTEL_LOGS_EXPORTER="otlp" \
  --env OTEL_RESOURCE_ATTRIBUTES="service.name=travel_assistant_quickstart,service.version=1.0.0" \
  --env AGENT_OBSERVABILITY_ENABLED="true" \
  --env DISABLE_ADOT_OBSERVABILITY="true" \
  --env TAVILY_API_KEY="your-tavily-key"
```

## Step 5: Test It!

**Quick test:**
```bash
agentcore invoke '{"prompt":"Best places to visit in Netherlands"}'
```

**Using test scripts:**

Fast search (5-10 seconds):
```bash
./invoke.sh
```

Delayed search (120+ seconds):
```bash
./invoke_india_best_places.sh
```

## Expected Output

You should see:
- Search results from both Tavily and DuckDuckGo
- Travel recommendations with descriptions
- Source URLs for more information

## Step 6: Verify Observability (If Configured)

1. Go to your Elastic Cloud deployment
2. Navigate to **Observability** > **APM**
3. Find the `travel_assistant` service
4. View traces, metrics, and logs

## Troubleshooting

**"TAVILY_API_KEY not set"**
- Make sure you exported the variable or passed it via `--env`

**"Bedrock Access Denied"**
- Enable Claude 3.5 Sonnet model in AWS Bedrock console
- Check IAM permissions

**"Timeout Error"**
- Increase timeout settings
- For India search, this is expected (120s delay)

**No Observability Data**
- Verify OTLP endpoint is correct
- Check Elastic API key permissions
- Ensure all OTEL_* variables are set


