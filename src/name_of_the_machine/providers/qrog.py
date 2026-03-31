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


def respond(messages=None, instructions=None, **kwargs):
    """
    Sends a request to the Groq Responses API using only Python's built-in urllib.
    """
    api_base = environ.get('GROQ_API_BASE', 'https://api.groq.com/openai/v1')
    api_key = environ.get('GROQ_API_KEY', '')
    default_model = environ.get('GROQ_DEFAULT_MODEL', 'openai/gpt-oss-120b')

    instruction = kwargs.get('system_instruction', instructions)

    # Define the payload
    payload = {
        "model": kwargs.get("model", default_model),
        "instructions": instruction,
        "input": messages,
        "max_output_tokens": kwargs.get("max_tokens", 65536),
        "reasoning": {
            "effort": "high"
        }
    }

    # Convert data dictionary to JSON and encode it to bytes
    data_bytes = json.dumps(payload).encode('utf-8')

    # Set the mandatory headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
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
                elif part['type'] == 'reasoning':
                    for chunk in part['content']:
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


if __name__ == "__main__":
    ...