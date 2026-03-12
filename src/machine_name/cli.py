# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from os import environ
import sys
import signal
from .config import settings
import json
import click
import fileinput


def handle_sigint(signum, frame):
    # Send the acknowledgment to stderr
    sys.stderr.write("machine-name: SIGINT received, exiting.\n")
    sys.stderr.flush()
    sys.exit(0)


# Register the signal interceptor
signal.signal(signal.SIGINT, handle_sigint)


@click.command()
@click.option('--provider-api-key', envvar='PROVIDER_API_KEY',
              default='no_provider_key', help='Language Model API provider key.')
@click.option('--github-token', envvar='GITHUB_TOKEN',
              default='', help='GitHub API token for private repo access.')
def run(provider_api_key, github_token, mode):
    """
        $ text | ./run.py                   # Accepts text from the pipe
        $ ./run.py /home/user/file.txt      # Reads file.
        $ ./run.py < /home/user/file.txt    # Reads file.

        secrets come through the environment variables.
    """
    if provider_api_key:
        if provider_api_key.startswith('sk-proj-'):
            settings['provider'] = 'OpenAI'
            environ['OPENAI_API_KEY'] = provider_api_key
        elif provider_api_key.startswith('sk-ant-'):
            settings['provider'] = 'Anthropic'
            environ['ANTHROPIC_API_KEY'] = provider_api_key
        elif provider_api_key.startswith('AIzaSy'):
            settings['provider'] = 'Gemini'
            environ['GEMINI_API_KEY'] = provider_api_key
        elif provider_api_key.startswith('gsk_'):
            settings['provider'] = 'Groq'
            environ['GROQ_API_KEY'] = provider_api_key
        elif provider_api_key.startswith('xai-'):
            settings['provider'] = 'XAI'
            environ['XAI_API_KEY'] = provider_api_key
        elif provider_api_key.startswith('LLM|'):
            settings['provider'] = 'Meta'
            environ['META_API_KEY'] = provider_api_key
        else:
            if settings['provider'] == '':
                raise ValueError(f"Unrecognized API key prefix and no provider specified.")
    if github_token:
        environ['GITHUB_TOKEN'] = github_token

    raw_input = ''
    for line in fileinput.input(encoding="utf-8"):
        raw_input += line

    from .machine import machine
    machine_name = {settings['name']}
    try:
        text, thoughts = machine(raw_input)
        # json.dump((thoughts_output, text_output), sys.stdout)
        sys.stdout.write(f'{machine_name}: (to itself) {thoughts}\n')
        sys.stdout.write(f'{machine_name}: {text}\n')
        sys.stdout.flush()
    except Exception as e:
        sys.stderr.write(f'{machine_name} did not work {e}')
        sys.stderr.flush()
        sys.exit(0)


def _run_single(machine):
    """One-shot mode: read full JSON from stdin, respond, exit."""
    raw_input = ''
    for line in fileinput.input(encoding="utf-8"):
        raw_input += line
    messages = json.loads(raw_input)

    text, thoughts = machine(messages)
    json.dump([text, thoughts], sys.stdout)


def _run_daemon(machine):
    """Daemon: line-delimited JSON loop.

    Each line on stdin is a JSON array of messages.
    Each response is a JSON array [text, thoughts] followed by newline.
    Loops until SIGINT on stdin.
    """
    print("daemon", file=sys.stderr)
    try:
        # Loop blocks until input is available on stdin
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue

            try:
                messages = json.loads(line)
            except json.JSONDecodeError as e:
                print(f"Error: invalid JSON: {e}", file=sys.stderr)
                continue

            if not isinstance(messages, list):
                print("Error: expected a JSON array of messages.",
                      file=sys.stderr)
                continue

            text, thoughts = machine(messages)
            json.dump([text, thoughts], sys.stdout)
            sys.stdout.write('\n')
            sys.stdout.flush()
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == '__main__':
    run()
