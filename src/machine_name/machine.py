# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from os import environ, path
from .config import settings
import sys
import yaml
from . import githf  # from .


def _fetch_instructions():
    """Retrieve the system prompt from a private GitHub repo.
    Falls back to the local machina.yaml if GitHub is unreachable.
    Returns the 'description' field from the YAML as the system prompt string.
    """
    try:
        repo = githf.connect_to_repo(
            organization=settings['machine_organization_name'],
            repository_name=settings['private_repo_with_text'],
            private=True
        )
        raw_yaml = githf.read_file(
            repository=repo,
            file_path=settings['system_prompt_file']
        )
    except Exception as e:
        print(f"Warning: could not fetch prompt from GitHub: {e}",
              file=sys.stderr)
        local_path = path.join(path.dirname(__file__), 'machina.yaml')
        with open(local_path, 'r') as f:
            raw_yaml = f.read()

    # Parse whatever you've gotten.
    parsed = yaml.safe_load(raw_yaml)
    name = parsed.get('name')
    settings['name'] = name
    instructions = parsed.get('description', 'You are a helpful assistant.')
    settings['instructions'] = instructions
    return name, instructions


def machine(messages):
    """Core agent logic.

    1. Fetches the system prompt from a private GitHub repo.
    2. Calls Anthropic via electroid.cloud() with the messages.
    3. Returns (text, thoughts) tuple.
    """
    # Fetch the confidential system prompt
    name, system_prompt = _fetch_instructions()

    # Load an appropriate library and query the API.
    provider = settings['provider']
    api_key  = settings['provider_api_key']
    if provider == 'OpenAI':
        # Call OpenAI API via opehaina
        environ['OPENAI_API_KEY'] = api_key
        import opehaina
        text, thoughts = opehaina.stream(
            messages=messages,
            system=system_prompt,
            max_tokens=100000
        )
        return text, thoughts

    elif provider == 'Anthropic':
        # Call the Anthropic API via electroid
        environ['ANTHROPIC_API_KEY'] = api_key
        import electroid
        text, thoughts = electroid.stream(
            messages=messages,
            system=system_prompt,
            max_tokens=100000
        )
        return text, thoughts

    elif provider == 'Groq':
        ...
    elif provider == 'Xai':
        ...
    elif provider == 'Meta':
        ...


if __name__ == '__main__':
    machine([])
