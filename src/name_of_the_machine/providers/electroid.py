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
    """ All parameters should be in kwargs, but they are optional
    """
    api_key = environ.get("ANTHROPIC_API_KEY")
    api_base = environ.get("ANTHROPIC_API_BASE", "https://api.anthropic.com/v1")
    api_type = environ.get("ANTHROPIC_VERSION", "2023-06-01")
    default_model = environ.get("ANTHROPIC_DEFAULT_MODEL", 'claude-opus-4-6')

    # Define the payload
    payload = {
        "model": kwargs.get("model", default_model),
        "thinking": {"type": "adaptive"},
        "system": kwargs.get("system_instruction", instructions),
        "messages": messages,
        "max_tokens": kwargs.get("max_tokens", 100000),
        "stop_sequences": kwargs.get("stop_sequences", ['stop']),
        "stream": kwargs.get("stream", False),
        "temperature": 1.0,
        "output_config": kwargs.get("output_config", {"effort": "low"}),
        "metadata": kwargs.get("metadata", None)
    }

    # Convert data dictionary to JSON and encode it to bytes
    data_bytes = json.dumps(payload).encode('utf-8')

    headers = {
        "x-api-key": api_key,
        "anthropic-version": api_type,
        "content-type": "application/json",
        "User-Agent": "Name-of-the-Machine"
    }

    # Create the Request object
    req = urllib.request.Request(
        f'{api_base}/messages',
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
            for chunk in output.get("content"):
                if chunk['type'] == 'text':
                    addition = chunk['text']
                    if addition not in ('\n\n', '\n'):
                        text += addition

                elif chunk['type'] == 'thinking':
                    thoughts += chunk['thinking']

            return thoughts, text

    except Exception as e:
        print("Unable to generate Message response")
        print(f"Exception: {e}")
        return ['', '']


if __name__ == "__main__":
    ...
