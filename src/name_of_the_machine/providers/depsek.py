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
    api_key = environ.get("DEPSEK_API_KEY")
    api_base = environ.get("DEPSEK_API_BASE", "https://api.deepseek.com")
    default_model = environ.get("DEPSEK_DEFAULT_MODEL", "deepseek-v4-pro")

    instruction = kwargs.get('system_instruction', instructions)
    first_message = [dict(role='system', content=instruction)] if instruction else []

    # add contents and user text to the first (instruction) message
    first_message.extend(messages)
    instruction_and_contents = first_message

    # Define the payload
    payload = {
        "model":            kwargs.get("model", default_model),
        "messages":         instruction_and_contents,
        "max_tokens":       kwargs.get("max_tokens", 32000),
        "temperature":      kwargs.get("temperature", 1.0),
        "reasoning_effort": kwargs.get("reasoning_effort", "max"),
        "thinking": {
            "type": "enabled"
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
        f'{api_base}/chat/completions',
        data=data_bytes,
        headers=headers,
        method="POST")

    try:
        # Execute the request
        with urllib.request.urlopen(req, timeout=300) as response:
            response_data = response.read().decode('utf-8')
            output = json.loads(response_data)
            message = output['choices'][0]['message']
            text = message['content']
            thoughts = message['reasoning_content']

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