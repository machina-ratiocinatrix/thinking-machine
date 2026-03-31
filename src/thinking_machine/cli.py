# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from os import environ
import sys
import click
import fileinput
from .config import Config
from .utilities import new_plato_text


@click.command()
@click.option('--provider-api-key', envvar='PROVIDER_API_KEY',
              default='no_provider_key', help='Language Model API provider key.')
@click.option('--github-token', envvar='GITHUB_TOKEN',
              default='', help='GitHub API token for private repo access.')
@click.option('--debug/--no-debug', default=False, help='Print full stack trace on errors.')
def run(provider_api_key, github_token, debug):
    """
        $ text | ./run.py                   # Accepts text from the pipe
        $ ./run.py /home/user/file.txt      # Reads file.
        $ ./run.py < /home/user/file.txt    # Reads file.

        secrets come through the environment variables.
    """
    config = Config()
    
    if provider_api_key:
        if provider_api_key.startswith('sk-'):
            if provider_api_key.startswith('sk-proj-'):
                config.provider = 'OpenAI'
                environ['OPENAI_API_KEY'] = provider_api_key
            elif provider_api_key.startswith('sk-ant-'):
                config.provider = 'Anthropic'
                environ['ANTHROPIC_API_KEY'] = provider_api_key
            else:
                config.provider = 'DepSek'
                environ['DEPSEK_API_KEY'] = provider_api_key
        elif provider_api_key.startswith('AIzaSy'):
            config.provider = 'Gemini'
            environ['GEMINI_API_KEY'] = provider_api_key
        elif provider_api_key.startswith('gsk_'):
            config.provider = 'Groq'
            environ['GROQ_API_KEY'] = provider_api_key
        elif provider_api_key.startswith('xai-'):
            config.provider = 'XAI'
            environ['XAI_API_KEY'] = provider_api_key
        elif provider_api_key.startswith('LLM|'):
            config.provider = 'Meta'
            environ['META_API_KEY'] = provider_api_key
        elif provider_api_key == 'no_provider_key':
            sys.stderr.write(f'No provider key!\n')
            sys.stderr.flush()
            sys.exit(1)
        else:
            if config.provider == '':
                raise ValueError(f"Unrecognized API key prefix and no provider specified.")
                
        config.provider_api_key = provider_api_key
        
    if github_token:
        config.github_token = github_token
        environ['GITHUB_TOKEN'] = github_token

    raw_input = ''
    for line in fileinput.input(encoding="utf-8"):
        raw_input += line

    from .machine import machine

    try:
        thoughts, text = machine(raw_input, config)
        output = raw_input + '\n\n' + new_plato_text(thoughts, text, config.name)
        sys.stdout.write(output)
        sys.stdout.flush()
    except Exception as e:
        if debug:
            import traceback
            traceback.print_exc()
        else:
            sys.stderr.write(f'Machine did not work {e}\n')
            sys.stderr.flush()
        sys.exit(1)


if __name__ == '__main__':
    run()
