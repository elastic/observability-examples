import os
import asyncio
#from dotenv import load_dotenv
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from langtrace_python_sdk import langtrace, with_langtrace_root_span
from langchain_openai import AzureChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnableSequence
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper


#set up tracing and initialize
otel_traces_exporter = os.environ.get('OTEL_TRACES_EXPORTER') or 'otlp'
otel_metrics_exporter = os.environ.get('OTEL_TRACES_EXPORTER') or 'otlp'
environment = os.environ.get('ENVIRONMENT') or 'dev'
otel_service_version = os.environ.get('OTEL_SERVICE_VERSION') or '1.0.0'
resource_attributes = os.environ.get('OTEL_RESOURCE_ATTRIBUTES') or 'service.version=1.0,deployment.environment=production'

otel_exporter_otlp_headers = os.environ.get('OTEL_EXPORTER_OTLP_HEADERS')
# fail if secret token not set
if otel_exporter_otlp_headers is None:
    raise Exception('OTEL_EXPORTER_OTLP_HEADERS environment variable not set')
#else:
#    otel_exporter_otlp_fheaders= f"Authorization=Bearer%20{secret_token}"

otel_exporter_otlp_endpoint = os.environ.get('OTEL_EXPORTER_OTLP_ENDPOINT')
# fail if server url not set
if otel_exporter_otlp_endpoint is None:
    raise Exception('OTEL_EXPORTER_OTLP_ENDPOINT environment variable not set')
else:
    exporter = OTLPSpanExporter(endpoint=otel_exporter_otlp_endpoint, headers=otel_exporter_otlp_headers)

print(otel_exporter_otlp_endpoint, otel_exporter_otlp_headers)


# Initialize Langtrace with Elastic exporter
langtrace.init(
    custom_remote_exporter=exporter,
    batch=True,
)

# Initialize Azure OpenAI model
model = AzureChatOpenAI(
    azure_endpoint=os.environ['AZURE_OPENAI_ENDPOINT'],
    azure_deployment=os.environ['AZURE_OPENAI_DEPLOYMENT_NAME'],
    openai_api_version=os.environ['AZURE_OPENAI_API_VERSION'],
    model="gpt-4o"
)

# Initialize DuckDuckGo search
wrapper = DuckDuckGoSearchAPIWrapper(region="us-en", time="d", max_results=2)
search = DuckDuckGoSearchResults(api_wrapper=wrapper, source="news")

# Create a prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI assistant. Use the provided search results to answer the user's query."),
    ("human", "{human_input}"),
    ("ai", "To answer this query, I'll need to search for some information. Let me do that for you."),
    ("human", "Here are the search results:\n{search_result}"),
    ("ai", "Based on this information, here's my response:")
])

# Create the RunnableSequence
chain = RunnableSequence(
    {
        "human_input": lambda x: x["query"],
        "search_result": lambda x: search.run(x["query"]),
    }
    | prompt
    | model
)

@with_langtrace_root_span()
async def chat_interface():
    print("Welcome to the AI Chat Interface!")
    print("Type 'quit' to exit the chat.")
    
    while True:
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() == 'quit':
            print("Thank you for chatting. Goodbye!")
            break
        
        print("AI: Thinking...")
        try:
            result = await chain.ainvoke({"query": user_input})
            print(f"AI: {result.content}")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    asyncio.run(chat_interface())
