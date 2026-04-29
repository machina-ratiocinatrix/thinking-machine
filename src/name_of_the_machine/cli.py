# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
import os
import sys
import select
import fileinput
import argparse
import syslog
from .config import Config
from .utilities import new_plato_text


def options_and_arguments():
    # Initialize the parser
    parser = argparse.ArgumentParser(
        description="Name-of-the-Machine thinks for you about the meanings.",
        epilog="Example:  name-of-the-machine input_text.txt > output_text.txt"
        # thinking-machine -a multilogue.txt > tmp && mv tmp multilogue.txt
    )

    # Give the access key and token, or set the environment variables in advance.
    parser.add_argument('-p', '--provider-api-key',
                        default=os.getenv('PROVIDER_API_KEY', 'no_key'),
                        help="LLM provider API key (defaults to $PROVIDER_API_KEY)")
    parser.add_argument('-g', '--github-token',
                        default=os.getenv('GITHUB_TOKEN', 'no_token'),
                        help="GitHub API token (defaults to $GITHUB_TOKEN)")

    parser.add_argument('-a', '--append',
                        action='store_true',
                        help="Append the utterance to the input.")

    parser.add_argument('-d', '--debug',
                        action='store_true',
                        help="Debug flag.")

    # Add the interactive flag
    # parser.add_argument('-i', '--interactive',
    #                     action='store_true',
    #                     help="Enable interactive mode (defaults to False)")

    # Positional arguments (files)
    # '*' captures zero or more arguments into a list, nargs='+' one or more.
    parser.add_argument('filenames',
                        nargs='*',
                        help="Zero (when text comes though a pipe) or more files to process.")
    return parser


def run():
    """
    $ text | name-of-the-machine                        # Accepts text from the pipe
    $ echo "...<text>..." | name-of-the-machine         #

    $ name-of-the-machine multilogue.txt new_turn.txt    # ...or files.
    """

    args = options_and_arguments().parse_args()

    # If no files are provided AND no data is being piped in - exit.
    if not args.filenames:
        # Check if stdin (fd 0) is ready to be read
        readable, _, _ = select.select([sys.stdin], [], [], 0.1)
        if not readable:
            print("Error: No input files or piped text stream.")
            options_and_arguments().print_help()
            sys.exit(1)

    config = Config()
    
    if args.provider_api_key:
        if args.provider_api_key.startswith('sk-'):
            if args.provider_api_key.startswith('sk-proj-'):
                config.provider = 'OpenAI'
                os.environ['OPENAI_API_KEY'] = args.provider_api_key
            elif args.provider_api_key.startswith('sk-ant-'):
                config.provider = 'Anthropic'
                os.environ['ANTHROPIC_API_KEY'] = args.provider_api_key
            else:
                config.provider = 'DepSek'
                os.environ['DEPSEK_API_KEY'] = args.provider_api_key
        elif args.provider_api_key.startswith('AIzaSy'):
            config.provider = 'Gemini'
            os.environ['GEMINI_API_KEY'] = args.provider_api_key
        elif args.provider_api_key.startswith('gsk_'):
            config.provider = 'Groq'
            os.environ['GROQ_API_KEY'] = args.provider_api_key
        elif args.provider_api_key.startswith('xai-'):
            config.provider = 'XAI'
            os.environ['XAI_API_KEY'] = args.provider_api_key
        elif args.provider_api_key.startswith('LLM|'):
            config.provider = 'Meta'
            os.environ['META_API_KEY'] = args.provider_api_key
        elif args.provider_api_key == 'no_provider_key':
            sys.stderr.write(f'No provider key!\n')
            sys.stderr.flush()
            sys.exit(1)
        else:
            if config.provider == '':
                raise ValueError(f"Unrecognized API key prefix and no provider specified.")
                
        config.provider_api_key = args.provider_api_key
        
    if args.github_token:
        config.github_token = args.github_token
        os.environ['GITHUB_TOKEN'] = args.github_token

    # Ingest files line by line. Join is here for long files.
    lines = []
    for line in fileinput.input(files=args.filenames or ['-'], encoding="utf-8"):
        lines.append(line)
    raw_input = "".join(lines)

    from .machine import machine

    try:
        thoughts, text = machine(raw_input, config)
        output = new_plato_text(thoughts, text, config.name)
        if args.append:
            output = raw_input +'\n\n' + output
        sys.stdout.write(output)
        sys.stdout.flush()

        # Assesment and signals.
        utterance = "My answer is ready"
        # Open syslog connection
        syslog.openlog(
            ident="name-of-the-machine",
            logoption=syslog.LOG_NDELAY,
            facility=syslog.LOG_USER
        )
        # Signal (single line less than 4096 only!)
        syslog.syslog(syslog.LOG_INFO, f"name-of-the-machine: {utterance}.")
        syslog.closelog()

    except Exception as e:
        if args.debug:
            import traceback
            traceback.print_exc()
        else:
            sys.stderr.write(f'Machine did not work {e}\n')
            sys.stderr.flush()
        sys.exit(1)


if __name__ == '__main__':
    run()
