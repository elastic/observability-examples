# run like this: uv run --exact -q --env-file .env chat.py
# /// script
# dependencies = [
#     "openai",
#     "elastic-opentelemetry",
#     "openinference-instrumentation-openai",
#     "opentelemetry-instrumentation-httpx"
# ]
# ///
# ruff: noqa: E402
from opentelemetry.instrumentation import auto_instrumentation

# This must precede any other imports you want to instrument!
auto_instrumentation.initialize()

import argparse
import os

import openai

model = os.getenv("CHAT_MODEL", "gpt-4o-mini")


def main():
    parser = argparse.ArgumentParser(description="OpenTelemetry-Enabled OpenAI Test Client")
    parser.add_argument(
        "--use-responses-api", action="store_true", help="Use the responses API instead of chat completions."
    )
    args = parser.parse_args()

    client = openai.Client()

    messages = [
        {
            "role": "user",
            "content": "Answer in up to 3 words: Which ocean contains Bouvet Island?",
        }
    ]

    # vllm-specific switch to disable thinking, ignored by other inference platforms.
    # See https://qwen.readthedocs.io/en/latest/deployment/vllm.html#thinking-non-thinking-modes
    if "qwen3" in model.lower():
        extra_body = {"chat_template_kwargs": {"enable_thinking": False}}
    else:
        extra_body = {}
    if args.use_responses_api:
        response = client.responses.create(
            model=model, input=messages[0]["content"], temperature=0, extra_body=extra_body
        )
        print(response.output[0].content[0].text)
    else:
        chat_completion = client.chat.completions.create(
            model=model, messages=messages, temperature=0, extra_body=extra_body
        )
        print(chat_completion.choices[0].message.content)


if __name__ == "__main__":
    main()
