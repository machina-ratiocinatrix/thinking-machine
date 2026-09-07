# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
import json
import urllib.request
import urllib.error
from os import environ


def respond(messages=None, instructions=None, **kwargs):
    """ All parameters should be in kwargs, but they are optional
    """
    # The configuration.
    api_key = environ.get("CHINF_API_KEY", '')
    default_model = environ.get("CHINF_DEFAULT_MODEL", 'gpt-5.6-luna')
    api_base = environ.get("CHINF_API_BASE", "https://api.cheaperinference.com/v1")

    # Set the mandatory headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
        "X-Api-Key": api_key,
        "Anthropic-Version": "2023-06-01",
        "User-Agent": "chinf"
    }

    # Receive the instruction
    instruction = kwargs.get('system_instruction', instructions)
    first_message = [dict(role='system', content=instruction)] if instruction else []

    # add contents and user text to the first (instruction) message
    first_message.extend(messages)
    instruction_and_contents = first_message

    # Define the initial payload
    payload = {
        "model":            kwargs.get("model", default_model),
        "messages":         instruction_and_contents,
        "max_tokens":       kwargs.get("max_tokens", 132000),
        "reasoning_effort": "max",
    }
    # Convert
    data_bytes = json.dumps(payload).encode('utf-8')
    # Create the Request object
    req = urllib.request.Request(
        f'{api_base}/chat/completions',
        data=data_bytes,
        headers=headers,
        method="POST")
    # Try to query
    try:
        # Execute the request
        with urllib.request.urlopen(req, timeout=3000) as response:
            response_data = response.read().decode('utf-8')
            output = json.loads(response_data)

    except urllib.error.HTTPError as e:
        # Handle HTTP errors (e.g., 401 Unauthorized, 400 Bad Request)
        error_info = e.read().decode('utf-8', errors='ignore')
        print(f"HTTP Error {e.code}: {e.reason}")
        print(f"Error Details: {error_info}")
        output = {}

    except urllib.error.URLError as e:
        # Handle network/connection errors
        print(f"Failed to reach the server: {e.reason}")
        output = {}
    # Discern what we got
    result = output.get('choices', {})
    if result:
        completion_message = result[0]['message']
        thoughts = completion_message.get('reasoning', '')
        text = completion_message.get('content', '')
    else:
        thoughts = ''
        text = ''

    return thoughts, text


if __name__ == "__main__":
    ...
