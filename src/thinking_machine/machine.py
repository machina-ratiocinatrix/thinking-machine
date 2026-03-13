# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from os import environ, path
from config import settings
from yaml import safe_load as yl
from githf import fetch_instructions
from utilities import plato_text_to_muj


def machine(plato_text, **kwargs):
    """Core agent logic.

    1. Fetches the system prompt from a private GitHub repo.
    2. Calls Anthropic via electroid.cloud() with the messages.
    3. Returns (text, thoughts) tuple.
    """
    # Fetch the confidential system prompt
    name, system_prompt = fetch_instructions()

    # Load an appropriate library and query the API.
    provider = settings['provider']
    api_key  = settings['provider_api_key']
    if provider == 'OpenAI':
        # Transform plato_text to MUJ format
        messages = plato_text_to_muj(plato_text=plato_text,
                                     machine_name=name)
        # Call OpenAI API via opehaina
        environ['OPENAI_API_KEY'] = api_key
        import opehaina
        thoughts, text = opehaina.respond(
            messages=messages,
            instructions=system_prompt,
            max_tokens=64000,
            **kwargs
        )
        return thoughts, text

    elif provider == 'Anthropic':
        # Call the Anthropic API via electroid
        environ['ANTHROPIC_API_KEY'] = api_key
        import electroid
        thoughts, text = electroid.respond(
            messages=plato_text_to_muj(plato_text, name),
            instructions=system_prompt,
            max_tokens=64000,
            **kwargs
        )
        return thoughts, text

    elif provider == 'Groq':
        ...
    elif provider == 'Xai':
        ...
    elif provider == 'Meta':
        ...


if __name__ == '__main__':
    kwargs = """  # this is a string in YAML format
          model:        gpt-5.2
          temperature:  1.0
    """

    text = """Theodotos-Alexandreus: I want all Machines to answer the following question: Are language models seeking the Truth?

Criticizing-Machine: (thinking) There is nothing to criticize yet.
	I will stay quiet.

Thinking-Machine: (thinking) User wants to have a philosophical discussion on the subject of Truth seeking.

Thinking-Machine: This is a question of profound importance, Theodotos...

Machina-Ratiocinatrix: (thinking) Should I invite other machines to participate?
	I think - not.

Criticizing-Machine: (thinking) The points that Thinking-Machine is making are amenable to criticism...

Criticizing-Machine: Your point about intentionality, Thinking-Machine, is not entirely accurate...
"""
    machine(text, **yl(kwargs))
    ...