# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
import sys
from os import environ, path
from .githf import fetch_instructions
from .utilities import (plato_text_to_muj,
                        plato_text_to_mpuj,
                        plato_text_to_cmj,
                        llm_soup_to_text)


def machine(plato_text, config, **kwargs):
    """Core agent logic.

    1. Fetches the system prompt from a private GitHub repo.
    2. Calls Provider
    3. Returns a (thoughts, text) tuple.
    """
    # Fetch the confidential system prompt, name is for a checkup.
    name, system_prompt = fetch_instructions(config)

    # Load an appropriate library and query the API.
    provider = config.provider
    api_key  = config.provider_api_key
    
    if provider == 'OpenAI':
        # Transform plato_text to MUJ format
        messages = plato_text_to_muj(plato_text=plato_text,
                                     machine_name=name)
        # Call OpenAI API via opehaina
        environ['OPENAI_API_KEY'] = api_key
        try:
            from .providers import openai
        except ImportError:
            print("openai module is missing.", file=sys.stderr)
            sys.exit(1)
            
        thoughts, text = openai.respond(
            messages=messages,
            instructions=system_prompt,
            **kwargs
        )

        thoughts = llm_soup_to_text(thoughts)
        return thoughts, text

    elif provider == 'Gemini':
        # Transform plato_text to MPUJ format
        messages = plato_text_to_mpuj(plato_text=plato_text,
                                     machine_name=name)
        # Call Gemini through castor-polux
        environ['GEMINI_API_KEY'] = api_key
        try:
            from .providers import castor_pollux
        except ImportError:
            print("No module castor-pollux", file=sys.stderr)
            sys.exit(1)
            
        thoughts, text = castor_pollux.respond(
            messages=messages,
            instructions=system_prompt,
            **kwargs
        )

        thoughts = llm_soup_to_text(thoughts)
        return thoughts, text

    elif provider == 'Anthropic':
        # Transform plato_text to MUJ format
        messages = plato_text_to_muj(plato_text=plato_text,
                                     machine_name=name)

        # Call the Anthropic API via electroid
        environ['ANTHROPIC_API_KEY'] = api_key
        try:
            from .providers import electroid
        except ImportError:
            print("no electroid module", file=sys.stderr)
            sys.exit(1)
            
        text, thoughts = electroid.respond(
            messages=messages,
            instructions=system_prompt,
            **kwargs
        )
        return text, thoughts

    elif provider == 'Groq':
        # Transform plato_text to MUJ format
        messages = plato_text_to_muj(plato_text=plato_text,
                                     machine_name=name)
        # Call OpenAI API via opehaina
        environ['GROQ_API_KEY'] = api_key
        try:
            from .providers import qrog
        except ImportError:
            print("openai module is missing.", file=sys.stderr)
            sys.exit(1)

        thoughts, text = qrog.respond(
            messages=messages,
            instructions=system_prompt,
            **kwargs
        )

        thoughts = llm_soup_to_text(thoughts)
        return thoughts, text

    elif provider == 'Xai':
        # Transform plato_text to MUJ format
        messages = plato_text_to_muj(plato_text=plato_text,
                                     machine_name=name)
        # Call OpenAI API via opehaina
        environ['XAI_API_KEY'] = api_key
        try:
            from .providers import strangelove
        except ImportError:
            print("openai module is missing.", file=sys.stderr)
            sys.exit(1)

        thoughts, text = strangelove.respond(
            messages=messages,
            instructions=system_prompt,
            **kwargs
        )

        thoughts = llm_soup_to_text(thoughts)
        return thoughts, text

    elif provider == 'DepSek':
        # Transform plato_text to CMJ format
        messages = plato_text_to_cmj(plato_text=plato_text,
                                     machine_name=name)
        # Call OpenAI API via opehaina
        environ['DEPSEK_API_KEY'] = api_key
        try:
            from .providers import depsek
        except ImportError:
            print("openai module is missing.", file=sys.stderr)
            sys.exit(1)

        thoughts, text = depsek.respond(
            messages=messages,
            instructions=system_prompt,
            **kwargs
        )

        return thoughts, text

    elif provider == 'Meta':
        # Transform plato_text to CMJ format
        messages = plato_text_to_cmj(plato_text=plato_text,
                                     machine_name=name)
        # Call OpenAI API via opehaina
        environ['META_API_KEY'] = api_key
        try:
            from .providers import camelids
        except ImportError:
            print("openai module is missing.", file=sys.stderr)
            sys.exit(1)

        thoughts, text = camelids.respond(
            messages=messages,
            instructions=system_prompt,
            **kwargs
        )

        return thoughts, text


if __name__ == '__main__':
    print('You have launched main')
