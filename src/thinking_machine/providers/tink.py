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


def respond(messages=None, instructions=None, tools=None, **kwargs):
    """ A version without tool calling.
    """
    api_key = environ.get("TINKER_API_KEY", '')
    default_model = environ.get("TINKER_DEFAULT_MODEL", 'thinkingmachines/Inkling')
    api_base = environ.get("TINKER_OAI_API_BASE",
                               'https://tinker.thinkingmachines.dev/services/tinker-prod/oai/api/v1')

    # Set the mandatory headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
        "User-Agent": "machine-thinking"
    }

    instruction         = kwargs.get('system_instruction', instructions)
    first_message       = [dict(role='system', content=instruction)] if instruction else []

    # contents can come in kwards or as an argument
    messages            = kwargs.get('messages', messages)

    first_message.extend(messages)
    instruction_and_contents = first_message

    payload = {
        'model': kwargs.get('model', default_model),
        'messages': instruction_and_contents,
        # 'response_format':          kwargs.get('response_format',{'type': 'text'}),
        'temperature': kwargs.get('temperature', 1.0),  # 0.0 to 2.0
        'max_tokens': kwargs.get('max_tokens', 4096),
        'top_p': kwargs.get('top_p', 0.9),
        'separate_reasoning': True,
        'reasoning_effort': kwargs.get('reasoning_effort', 'high'),  # 'low', 'medium', 'high'
        'stream': False
    }
    # Convert for sending.
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

    result = output.get('choices', {})
    if result:
        completion_message = result[0]['message']
        thoughts = completion_message.get('reasoning_content', '')
        text = completion_message.get('content', '')
    else:
        thoughts = ''
        text = ''

    return thoughts, text


if __name__ == '__main__':
   ...
