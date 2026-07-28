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


def decode_output(output):
    # Parse the result
    text = ''; thoughts = ''
    for part in output:
        part_type = part.get('type', None)
        if part_type == 'message':
            text = " ".join([chunk['text'] for chunk in part['content'] if chunk['type'] == 'output_text'])
        elif part_type == 'reasoning':
            thoughts = " ".join([chunk['text'] for chunk in part['summary'] if chunk['type'] == 'summary_text'])
    function_calls = [part for part in output if part['type'] == 'function_call']
    return thoughts, text, function_calls


def respond(messages=None, instructions=None, tools=None, **kwargs):
    """ All parameters should be in kwargs, but they are optional
    """
    # The configuration.
    api_key = environ.get('FIREWORKS_API_KEY')
    api_base = environ.get('FIREWORKS_BASE_URL', 'https://api.fireworks.ai/inference/v1')
    default_model = environ.get('FIREWORKS_MODEL', 'accounts/fireworks/models/kimi-k3')

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + api_key,
        "User-Agent": "Name-of-the-Machine"
    }

    # Receive the instruction
    instruction = kwargs.get('system_instruction', instructions)

    # Define the initial payload
    payload = {
        "model":            kwargs.get("model", default_model),
        "instructions":     instruction,
        "input":            messages,
        "max_output_tokens": kwargs.get("max_tokens", 132000),
        "reasoning": {
            "effort": "max",
            "summary": "detailed"
        }
    }
    # Convert data dictionary to JSON and encode it to bytes
    data_bytes = json.dumps(payload).encode('utf-8')
    # Create the Request object
    req = urllib.request.Request(
        f'{api_base}/responses',
        data=data_bytes,
        headers=headers,
        method="POST")
    # Try to query
    try:
        # Execute the request
        with urllib.request.urlopen(req, timeout=3000) as response:
            response_data = response.read().decode('utf-8')
            output = json.loads(response_data)
            thoughts, text, function_calls = decode_output(output.get('output', {}))

    except urllib.error.HTTPError as e:
        # Handle HTTP errors (e.g., 401 Unauthorized, 400 Bad Request)
        error_info = e.read().decode('utf-8', errors='ignore')
        print(f"HTTP Error {e.code}: {e.reason}")
        print(f"Error Details: {error_info}")
        return '', ''

    except urllib.error.URLError as e:
        # Handle network/connection errors
        print(f"Failed to reach the server: {e.reason}")
        return '', ''

    return thoughts, text


if __name__ == "__main__":
    ...