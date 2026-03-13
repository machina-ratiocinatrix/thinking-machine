# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
import re


def plato_text_to_muj(plato_text, machine_name):
    """
    Transforms platoText format to MUJ (Multi-User JSON) array for OpenAI API.
    Consecutive non-assistant messages are grouped into a single 'user' message.
    Assistant messages have only the utterance.
    """
    if plato_text is None or not isinstance(plato_text, str):
        raise ValueError("Invalid input: plato_text must be a string.")

    trimmed_plato_text = plato_text.strip()
    if not trimmed_plato_text:
        return []

    assistant_name_upper = machine_name.upper()

    muj_messages = []
    current_role = None
    current_parts = []
    current_is_thoughts = None

    message_blocks = re.split(r'\n\n(?=[A-Za-z0-9_-]+:\s*)', trimmed_plato_text)

    for block in message_blocks:
        current_block = block.strip()
        if not current_block:
            continue

        speaker_match = re.match(r'^([A-Za-z0-9_-]+):\s*', current_block)
        if not speaker_match:
            continue

        speaker = speaker_match.group(1)
        raw_utterance = current_block[len(speaker_match.group(0)):]

        is_thoughts = False
        if raw_utterance.strip().startswith('(thinking)'):
            is_thoughts = True
            raw_utterance = re.sub(r'^\s*\(thinking\)\s*', '', raw_utterance)

        utterance = re.sub(r'\n{2,}', '\n\t', raw_utterance).strip()

        final_utterance = utterance
        if is_thoughts:
            final_utterance = f"(thinking) {utterance}"

        is_assistant_message = speaker.upper() == assistant_name_upper
        role = 'assistant' if is_assistant_message else 'user'

        if role != current_role or (role == 'assistant' and is_thoughts != current_is_thoughts):
            if len(current_parts) > 0:
                muj_messages.append({
                    'role': current_role,
                    'content': '\n\n'.join(current_parts)
                })
            current_role = role
            current_is_thoughts = is_thoughts
            current_parts = []

        if is_assistant_message:
            current_parts.append(final_utterance)
        else:
            current_parts.append(f"{speaker}: {final_utterance}")

    if len(current_parts) > 0:
        muj_messages.append({
            'role': current_role,
            'content': '\n\n'.join(current_parts)
        })

    return muj_messages


def another_plato_text_to_muj(plato_text, machine_name):
    """
    Transforms platoText format to MUJ (Multi-User JSON) array for OpenAI API.
    Consecutive non-assistant messages are grouped into a single 'user' message.
    Assistant messages have name and are joined into a single utterance (with name).
    """
    # trimmed_plato_text = plato_text.strip()
    # if not trimmed_plato_text:
    #     return []

    assistant_name_upper = machine_name.upper()

    muj_messages = []
    current_role = None
    current_parts = []

    message_blocks = re.split(r'\n\n(?=[A-Za-z0-9_-]+:\s*)', plato_text)

    for block in message_blocks:
        current_block = block.strip()
        if not current_block:
            continue

        speaker_match = re.match(r'^([A-Za-z0-9_-]+):\s*', current_block)
        if not speaker_match:
            continue

        speaker = speaker_match.group(1)
        raw_utterance = current_block[len(speaker_match.group(0)):]

        is_thoughts = False
        if raw_utterance.strip().startswith('(thinking)'):
            is_thoughts = True
            raw_utterance = re.sub(r'^\s*\(thinking\)\s*', '', raw_utterance)

        # questionable replacement of double newline with new paragraph delimiter
        utterance = re.sub(r'\n{2,}', '\n\t', raw_utterance).strip()

        final_utterance = utterance
        if is_thoughts:
            final_utterance = f"(thinking) {utterance}"

        is_assistant_message = speaker.upper() == assistant_name_upper
        role = 'assistant' if is_assistant_message else 'user'

        if role != current_role:
            if len(current_parts) > 0:
                muj_messages.append({
                    'role': current_role,
                    'content': '\n\n'.join(current_parts)
                })
            current_role = role
            current_parts = []

        current_parts.append(f"{speaker}: {final_utterance}")

    if len(current_parts) > 0:
        muj_messages.append({
            'role': current_role,
            'content': '\n\n'.join(current_parts)
        })

    return muj_messages


def plato_text_to_mpuj(plato_text, machine_name):
    """
    Transforms platoText format to MPUJ (Multi-Part User JSON) array for Gemini API.
    Consecutive non-model messages are grouped into a single 'user' message
    with multiple parts. Each part includes the speaker's name and utterance.
    Model messages have a single part with the utterance.
    """
    if plato_text is None or not isinstance(plato_text, str):
        raise ValueError("Invalid input: plato_text must be a string.")

    trimmed_plato_text = plato_text.strip()
    if not trimmed_plato_text:
        return []

    model_name_upper = machine_name.upper()

    mpuj_messages = []
    current_role = None
    current_parts = []

    message_blocks = re.split(r'\n\n(?=[A-Za-z0-9_-]+:\s*)', trimmed_plato_text)

    for block in message_blocks:
        current_block = block.strip()
        if not current_block:
            continue

        speaker_match = re.match(r'^([A-Za-z0-9_-]+):\s*', current_block)
        if not speaker_match:
            continue

        speaker = speaker_match.group(1)
        raw_utterance = current_block[len(speaker_match.group(0)):]

        is_thoughts = False
        if raw_utterance.strip().startswith('(thinking)'):
            is_thoughts = True
            raw_utterance = re.sub(r'^\s*\(thinking\)\s*', '', raw_utterance)

        utterance = re.sub(r'\n{2,}', '\n\t', raw_utterance).strip()

        final_utterance = utterance
        if is_thoughts:
            final_utterance = f"(thinking) {utterance}"

        is_model_message = speaker.upper() == model_name_upper
        role = 'model' if is_model_message else 'user'

        if role != current_role:
            if len(current_parts) > 0:
                mpuj_messages.append({
                    'role': current_role,
                    'parts': current_parts
                })
            current_role = role
            current_parts = []

        current_parts.append({'text': f"{speaker}: {final_utterance}"})

    if len(current_parts) > 0:
        mpuj_messages.append({
            'role': current_role,
            'parts': current_parts
        })

    return mpuj_messages


def llm_soup_to_text(llm_response):
    """
    Cleans and transforms text from Large Language Models (LLMs) by:
    - Removing all Markdown formatting (bold, italics, headers, lists, code blocks, links, etc.).
    - Consolidating multiple newlines into a consistent paragraph separator (`\n\t`).
    - Removing extraneous tabs and multiple spaces.
    - Trimming leading/trailing whitespace.
    """
    if not isinstance(llm_response, str):
        return ""

    text = llm_response

    # --- Step 1: Normalize Newlines & Initial Cleanup ---
    text = text.replace('\r\n', '\n')
    text = re.sub(r'\n{2,}', '\n\n', text)

    # --- Step 2: Remove Block-Level Markdown Elements ---
    text = re.sub(r'`{3,}[^\n]*\n([\s\S]*?)\n`{3,}', '', text)
    text = re.sub(r'~{3,}[^\n]*\n([\s\S]*?)\n~{3,}', '', text)
    text = re.sub(r'<!--[\s\S]*?-->', '', text)
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'^\s*(?:-|\*|_){3,}\s*$', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\s*>\s*', '', text, flags=re.MULTILINE)

    # --- Step 3: Remove Inline Markdown Elements ---
    text = re.sub(r'^\s*#{1,6}\s*', '', text, flags=re.MULTILINE)
    text = re.sub(r'^([^\n]+)\n\s*(?:=|-){2,}\s*$', r'\1', text, flags=re.MULTILINE)
    text = re.sub(r'!?\[.*?\]\(.*?\)', '', text)
    text = re.sub(r'`([^`]+)`', r'\1', text)
    text = re.sub(r'\*\*([^*]+?)\*\*', r'\1', text)
    text = re.sub(r'__([^_]+?)__', r'\1', text)
    text = re.sub(r'\*([^*]+?)\*', r'\1', text)
    text = re.sub(r'_([^_]+?)_', r'\1', text)
    text = re.sub(r'^\s*(?:[-*+]|\d+\.)\s+', '', text, flags=re.MULTILINE)

    # --- Step 4: Final Whitespace & Paragraph Normalization ---
    text = '\n'.join(line.strip() for line in text.split('\n'))
    text = text.replace('\t', ' ')
    text = re.sub(r' {2,}', ' ', text)
    text = text.replace('\n\n', '\n\t')

    # --- Step 5: Final Trimming ---
    text = text.strip()
    text = re.sub(r'^[\n\t]+', '', text)
    text = re.sub(r'\n\t{2,}', '\n\t', text)

    return text


def new_plato_text(thoughts, text, machine_name):
    """
    Transforms a pair of text variables 'thoughts' and 'text' received
    from the LLM and cleaned up into a plato_text format as utterances
    of the machine, with its name as a speaker.
    Does not form a 'thoughts' utterance if there were not 'thoughts'.
    """
    result = ""
    if thoughts and thoughts.strip():
        # cleaned_thoughts = re.sub(r'\n{2,}', '\n\t', thoughts.strip())
        result += f"{machine_name}: (thinking) {thoughts}\n\n"

    if text and text.strip():
        # cleaned_text = re.sub(r'\n{2,}', '\n\t', text.strip())
        result += f"{machine_name}: {text}\n\n"

    return result

