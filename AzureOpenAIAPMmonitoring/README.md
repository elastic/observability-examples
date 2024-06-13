# Monitor OpenAI API and GPT Models with OpenTelemetry and Elastic

As the use of AI-based solutions grows, developers need to monitor the performance and costs of these applications. This README demonstrates how to use OpenTelemetry and Elastic to monitor Azure OpenAI applications.

## OpenAI API and Cost Monitoring

The OpenAI API returns token counts and other useful information in each API response. Use this data can to calculate the cost of each API call based on Azure OpenAI's pricing.

## OpenTelemetry

OpenTelemetry is a powerful and widely adopted observability tool that you can use to monitor Azure OpenAI applications. This example uses Flask, Azure OpenAI API, and OpenTelemetry to instrument external calls and monitor the performance of Azure OpenAI API calls.

## Setup

1. Set up an Elastic Cloud Account and create a deployment.
2. Install the required Python libraries.

 - pip3 install opentelemetry-api
 - pip3 install opentelemetry-sdk
 - pip3 install opentelemetry-exporter-otlp
 - pip3 install opentelemetry-instrumentation
 - pip3 install opentelemetry-instrumentation-requests
 - pip3 install openai
 - pip3 install AzureOpenAI
 - pip3 install flask

4. Set the following environment variable using your Azure OpenAI and Elastic credentials:

- export AZURE_OPENAI_API_KEY="your-Azure-OpenAI-API-key"
- export AZURE_OPENAI_ENDPOINT="your-Azure-OpenAI-endpoint"
- export OPENAI_API_VERSION="your_api_version"
- export OTEL_EXPORTER_OTLP_AUTH_HEADER="your-otel-exporter-auth-header"
- export OTEL_EXPORTER_OTLP_ENDPOINT="your-otel-exporter-endpoint"

5. Check out the example Python application.

## Example Application

The example application demonstrates how to use OpenTelemetry to instrument a Flask application that makes Azure OpenAI API calls. The magic happens inside the `monitor` code that you can use freely to instrument your Azure OpenAI code.

## Monkey Patching

The app uses monkey patching to modify the behavior of the `chat.completions` call at runtime so that the response metrics can be captured and sent to the OpenTelemetry OTLP endpoint (Elastic).

## Cost Calculation

The `calculate_cost` function calculates the cost of a single request to the Azure OpenAI APIs based on the token counts and the model used.

## Elastic

Once the data is captured, you can view and analyze it in Elastic. You can use the captured data to build dashboards, monitor transactions and latency, and assess the performance of your Azure OpenAI service.

