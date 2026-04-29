# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
import urllib.request
import urllib.error
import urllib.parse
import json
from os import environ
from ..utilities import messages_to_mpj


def respond(messages=None, instructions=None, **kwargs):
    """
    """
    api_key = environ.get('GEMINI_API_KEY', '')
    api_base = environ.get('GEMINI_API_BASE', 'https://generativelanguage.googleapis.com/v1beta')
    content_model = environ.get('GEMINI_DEFAULT_CONTENT_MODEL', 'gemma-4-31b-it')

    garbage = [
        {'category': 'HARM_CATEGORY_HATE_SPEECH', 'threshold': 'BLOCK_NONE'},
        {'category': 'HARM_CATEGORY_SEXUALLY_EXPLICIT', 'threshold': 'BLOCK_NONE'},
        {'category': 'HARM_CATEGORY_DANGEROUS_CONTENT', 'threshold': 'BLOCK_NONE'},
        {'category': 'HARM_CATEGORY_HARASSMENT', 'threshold': 'BLOCK_NONE'},
        {'category': 'HARM_CATEGORY_CIVIC_INTEGRITY', 'threshold': 'BLOCK_NONE'}
    ]

    instructions = kwargs.get('system_instruction', instructions)
    system_instruction = dict(role='system', parts=[dict(text=instructions)]) if instructions else None

    # Trickery for thinking models
    thinking_config = None
    model = kwargs.get("model", content_model)
    if model.startswith('gemini-2.5'):
        thinking_config = {
            'includeThoughts': kwargs.get('include_thoughts', True),
            'thinkingBudget': kwargs.get('thinking_budget', 10000)
        }
    elif model.startswith('gemini-3'):
        thinking_config = {
            'includeThoughts': kwargs.get('include_thoughts', True),
            'thinkingLevel': kwargs.get('thinking_level', 'high')
        }
    elif model.startswith('gemma-4'):
        thinking_config = {
            'includeThoughts': kwargs.get('include_thoughts', True)
        }

    # Define the payload
    payload = {
        'systemInstruction': system_instruction,
        'contents': messages,
        'safetySettings': garbage,
        'generationConfig': {
            'stopSequences': kwargs.get('stop_sequences', ['STOP', 'Title']),
            'responseMimeType': kwargs.get('mime_type', 'text/plain'),
            'responseModalities': kwargs.get('modalities', ['TEXT']),
            'temperature': kwargs.get('temperature', 1.0),
            'maxOutputTokens': kwargs.get('max_tokens', 10000),
            'topP': kwargs.get('top_p', 0.9),
            'topK': kwargs.get('top_k', 10),
            'enableEnhancedCivicAnswers': False,
        },
    }
    if thinking_config:
        payload['generationConfig']['thinkingConfig'] = thinking_config
    if kwargs.get('sources'):
        payload['tools'].append(
            {
                "url_context": {}
            }
        )

    # Convert data dictionary to JSON and encode it to bytes
    data_bytes = json.dumps(payload).encode('utf-8')

    # Set the mandatory headers
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Name-of-the-Machine"
    }

    # urlencode parameter
    params = urllib.parse.urlencode({'key': api_key})

    # Create the Request object
    req = urllib.request.Request(
        f'{api_base}/models/{kwargs.get("model", content_model)}:generateContent?{params}',
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
            if output['candidates'][0]['finishReason'] == 'SAFETY':
                raise Exception('Answer censored by Google.')
            for part in output['candidates'][0]['content']['parts']:
                if part.get('thought'):
                    thoughts += part['text']
                else:
                    text += part['text']

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
