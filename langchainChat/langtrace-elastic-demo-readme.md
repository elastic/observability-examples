# Langtrace Elastic Demo

This project demonstrates the integration of Langtrace with Elastic APM for tracing AI-powered applications. It uses LangChain, Azure OpenAI, and DuckDuckGo search to create a simple chat interface with AI-assisted responses.

## Prerequisites

- Python 3.8+
- An Azure OpenAI account
- An Elastic APM account

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/elastic/observability-examples.git
   cd langchainChat
   ```
2. Create and activate a virtual environment:

   ```
   # On macOS and Linux:
   python3 -m venv venv
   source venv/bin/activate

   # On Windows:
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. Install the required packages:

   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root and add the following environment variables:

   ```
   # Azure OpenAI settings
   AZURE_OPENAI_ENDPOINT=your_azure_openai_endpoint
   AZURE_OPENAI_DEPLOYMENT_NAME=your_deployment_name
   AZURE_OPENAI_API_VERSION=your_api_version
   AZURE_OPENAI_API_KEY=your_api_key

   # OpenTelemetry settings
   OTEL_EXPORTER_OTLP_ENDPOINT=your_elastic_apm_server_url
   OTEL_EXPORTER_OTLP_HEADERS="Authorization=Bearer your_elastic_apm_secret_token"
   OTEL_SERVICE_NAME=langtrace-elastic-demo
   OTEL_RESOURCE_ATTRIBUTES="service.name=<servicename>,service.version=1.2,deployment.environment=dev"

   ```

Note: The OTEL_EXPORTER_OTLP_HEADERS should include the full header string, including the "Authorization=Bearer" prefix.

There is an example file `ENV` in this directory

```
cp ENV .env
```

Edit the file with your favorite editor and put in the proper values


## Usage

Run the app with:

```
opentelemetry-instrument python langtrace-elastic-demo.py
```

This will start an interactive chat interface. Type your questions and the AI will respond with information from recent web searches.

Type 'quit' to exit the chat.

## Example Trace

![Alt text](img/Xnapper-2024-08-16-12.36.03.png "Langtrace traces")

## How it works

1. The script initializes Langtrace with an Elastic APM exporter.
2. It sets up an Azure OpenAI model and a DuckDuckGo search tool.
3. When you ask a question, it performs a web search and uses the results to generate an AI response.
4. All operations are traced using Langtrace, which sends the trace data to Elastic APM.


