#
# Copyright Elasticsearch B.V. and contributors
# SPDX-License-Identifier: Apache-2.0
#
import json
import os

import pytest
import yaml


@pytest.fixture
def default_openai_env(monkeypatch):
    """Prevent offline tests from failing due to requiring the ENV OPENAI_API_KEY."""

    if "OPENAI_API_KEY" not in os.environ:
        monkeypatch.setenv("OPENAI_API_KEY", "test_openai_api_key")


@pytest.fixture(scope="module")
def vcr_config():
    """Scrub sensitive headers and gunzip responses so they are readable"""
    sensitive_request_headers = [
        "authorization",
        "cookie",
        "openai-organization",
        "openai-project",
    ]
    sensitive_response_headers = {"openai-organization", "set-cookie"}
    return {
        "decode_compressed_response": True,
        "filter_headers": sensitive_request_headers,
        "before_record_response": lambda r: {
            **r,
            "headers": {k: v for k, v in r["headers"].items() if k.lower() not in sensitive_response_headers},
        },
    }


class LiteralBlockScalar(str):
    """Formats the string as a literal block scalar, preserving whitespace and
    without interpreting escape characters"""


def literal_block_scalar_presenter(dumper, data):
    """Represents a scalar string as a literal block, via '|' syntax"""
    return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")


yaml.add_representer(LiteralBlockScalar, literal_block_scalar_presenter)


def process_string_value(string_value):
    """Pretty-prints JSON or returns long strings as a LiteralBlockScalar"""
    try:
        json_data = json.loads(string_value)
        return LiteralBlockScalar(json.dumps(json_data, indent=2))
    except (ValueError, TypeError):
        if len(string_value) > 80:
            return LiteralBlockScalar(string_value)
    return string_value


def convert_body_to_literal(data):
    """Searches the data for body strings, attempting to pretty-print JSON"""
    if isinstance(data, dict):
        for key, value in data.items():
            # Handle response body case (e.g., response.body.string)
            if key == "body" and isinstance(value, dict) and "string" in value:
                value["string"] = process_string_value(value["string"])

            # Handle request body case (e.g., request.body)
            elif key == "body" and isinstance(value, str):
                data[key] = process_string_value(value)

            else:
                convert_body_to_literal(value)

    elif isinstance(data, list):
        for idx, choice in enumerate(data):
            data[idx] = convert_body_to_literal(choice)

    return data


class PrettyPrintJSONBody:
    """This makes request and response body recordings more readable."""

    @staticmethod
    def serialize(cassette_dict):
        cassette_dict = convert_body_to_literal(cassette_dict)
        return yaml.dump(cassette_dict, default_flow_style=False, allow_unicode=True)

    @staticmethod
    def deserialize(cassette_string):
        return yaml.load(cassette_string, Loader=yaml.Loader)


@pytest.fixture(scope="module", autouse=True)
def fixture_vcr(vcr):
    vcr.register_serializer("yaml", PrettyPrintJSONBody)
    return vcr
