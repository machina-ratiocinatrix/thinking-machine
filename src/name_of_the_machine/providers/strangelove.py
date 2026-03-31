# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
import urllib.request
import urllib.error
import json
from os import environ


def respond(messages, instructions, **kwargs):
    """
    """
    api_key = environ.get("XAI_API_KEY")
    api_base = environ.get("XAI_API_BASE", "https://api.x.ai/v1")
    default_model = environ.get("XAI_DEFAULT_MODEL", "grok-4.20-reasoning")

    instruction = kwargs.get('system_instruction', instructions)

    # Define the payload
    payload = {
        "model": kwargs.get("model", default_model),
        "instructions": instructions,
        "input": messages,
        "max_output_tokens": kwargs.get("max_tokens", 64000),
        "reasoning": {
            "summary": "detailed"
        }
    }

    # Convert data dictionary to JSON and encode it to bytes
    data_bytes = json.dumps(payload).encode('utf-8')

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + api_key,
        "User-Agent": "Name-of-the-Machine"
    }

    # Create the Request object
    req = urllib.request.Request(
        f'{api_base}/responses',
        data=data_bytes,
        headers=headers,
        method="POST")

    try:
        # Execute the request
        with urllib.request.urlopen(req, timeout=300) as response:
            response_data = response.read().decode('utf-8')
            output = json.loads(response_data)
            text = ''
            thoughts = ''
            for part in output['output']:
                if part['type'] == 'message':
                    for chunk in part['content']:
                        text += chunk['text']
                elif part['type'] == 'reasoning_content':
                    for chunk in part['summary']:
                        thoughts += chunk['text']

        return thoughts, text

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


if __name__ == '__main__':
    ...
