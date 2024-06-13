from openai import AzureOpenAI
import openai
import json
from functools import wraps
from opentelemetry import trace

counters = {'completion_count': 0, 'token_count': 0, 'prompt_tokens': 0, 'completion_tokens': 0}

# Define the formula
def calculate_cost(response):
    if response.model in ['gpt-4', 'gpt-4-0314']:
        cost = (response.usage.prompt_tokens * 0.03 + response.usage.completion_tokens * 0.06) / 1000
    elif response.model in ['gpt-4-32k', 'gpt-4-32k-0314']:
        cost = (response.usage.prompt_tokens * 0.06 + response.usage.completion_tokens * 0.12) / 1000
    elif 'gpt-3.5-turbo' in response.model:
        cost = response.usage.total_tokens * 0.002 / 1000
    elif 'davinci' in response.model:
        cost = response.usage.total_tokens * 0.02 / 1000
    elif 'curie' in response.model:
        cost = response.usage.total_tokens * 0.002 / 1000
    elif 'babbage' in response.model:
        cost = response.usage.total_tokens * 0.0005 / 1000
    elif 'ada' in response.model:
        cost = response.usage.total_tokens * 0.0004 / 1000
    else:
        cost = 0
    return cost


def count_completion_requests_and_tokens(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        counters['completion_count'] += 1
        response = func(*args, **kwargs)

        token_count = response.usage.total_tokens
        prompt_tokens = response.usage.prompt_tokens
        completion_tokens = response.usage.completion_tokens
        cost = calculate_cost(response)
        strResponse = json.dumps(response, default=str)

        # Set OpenTelemetry attributes
        span = trace.get_current_span()
        if span:
            span.set_attribute("completion_count", counters['completion_count'])
            span.set_attribute("token_count", token_count)
            span.set_attribute("prompt_tokens", prompt_tokens)
            span.set_attribute("completion_tokens", completion_tokens)
            span.set_attribute("model", response.model)
            span.set_attribute("cost", cost)
            span.set_attribute("response", strResponse)
        return response
    return wrapper

# Monkey-patch the openai.Completion.create function
openai.chat.completions.create = count_completion_requests_and_tokens(openai.chat.completions.create)