# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
import re
import html


def plato_text_to_cmj(plato_text, machine_name):
    """
    Transforms platoText format to CMJ format.
    """
    if plato_text is None or not isinstance(plato_text, str):
        raise ValueError("Invalid input: plato_text must be a string.")

    trimmed_plato_text = plato_text.strip()
    if not trimmed_plato_text:
        return []

    assistant_name_upper = machine_name.upper()

    cmj_messages = []

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

        role = 'user'
        if speaker.upper() == assistant_name_upper:
            role = 'assistant'
        elif speaker.upper() == 'INSTRUCTIONS':
            role = 'system'

        cmj_messages.append({
            'role': role,
            'name': speaker,
            'content': final_utterance
        })

    return cmj_messages


def cmj_to_plato_text(cmj_messages):
    """
    Transforms a list of CMJ message dicts to platoText format.
    """
    if not isinstance(cmj_messages, list):
        return ""

    plato_text = ""

    for message in cmj_messages:
        if isinstance(message, dict) and isinstance(message.get('name'), str) and isinstance(message.get('content'),
                                                                                             str):
            speaker = message['name'].strip()

            utterance = re.sub(r'\n{2,}', '\n\t', message['content'])
            utterance = utterance.strip()

            plato_text += f"{speaker}: {utterance}\n\n"

    return plato_text


def plato_text_to_muj(plato_text, machine_name):
    """
    Transforms platoText format to MUJ (Multi-User JSON) array for OpenAI
    responses API.
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
    Assistant messages have a name in each of them and are joined into a single
    utterance.

    This is for the Theatron type of imitation of performance.
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


def new_plato_text(thoughts, text, machine_name):
    """
    Transforms a pair of text variables 'thoughts' and 'text' received
    from the LLM and cleaned up from the markdown crap into a plato_text
    format as new utterances of this machine, with its name as a speaker.
    Does not form a 'thoughts' utterance if there were not 'thoughts'.

    The result is later added to the input plato_text that came to the
    machine through a pipe.
    """
    result = ""
    if thoughts and thoughts.strip():
        cleaned_thoughts = re.sub(r'\n{2,}', '\n\t', thoughts.strip())
        result += f"{machine_name}: (thinking) {cleaned_thoughts}\n\n"

    if text and text.strip():
        cleaned_text = re.sub(r'\n{2,}', '\n\t', text.strip())
        result += f"{machine_name}: {cleaned_text}\n\n"

    return result


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

    # --- Step 0: Unescape HTML Entities First ---
    text = html.unescape(text)

    # --- Step 1: Normalize Newlines & Initial Cleanup ---
    text = text.replace('\r\n', '\n')

    # --- Step 2: Remove Fenced Code Blocks completely ---
    # Multiline flag allows ^ to match start of lines.
    text = re.sub(r'^```[^\n]*\n([\s\S]*?)\n```', '', text, flags=re.MULTILINE)
    text = re.sub(r'^~~~[^\n]*\n([\s\S]*?)\n~~~', '', text, flags=re.MULTILINE)
    # Catch ones that might not be at start of line or properly closed with newline
    text = re.sub(r'```[^\n]*\n([\s\S]*?)```', '', text)
    text = re.sub(r'~~~[^\n]*\n([\s\S]*?)~~~', '', text)

    # --- Step 3: Remove HTML Comments and Tags ---
    text = re.sub(r'<!--[\s\S]*?-->', '', text)

    # We want <br> to become newline before stripping tags to preserve line breaks
    text = re.sub(r'<br\s*/?>', '\n', text, flags=re.IGNORECASE)
    # Strip other HTML tags, keeping inner text
    text = re.sub(r'<[^>]+>', '', text)

    # --- Step 4: Remove Block-Level Markdown Elements ---
    # Horizontal rules
    text = re.sub(r'^\s*(?:-|\*|_){3,}\s*$', '', text, flags=re.MULTILINE)
    # Blockquotes: remove leading >
    text = re.sub(r'^\s*>\s*', '', text, flags=re.MULTILINE)

    # --- Step 5: Remove Headers ---
    # ATX headers (# Header)
    text = re.sub(r'^\s*#{1,6}\s*', '', text, flags=re.MULTILINE)
    # Setext headers (Underlines Header\n===)
    text = re.sub(r'^([^\n]+)\n\s*(?:=|-){2,}\s*$', r'\1', text, flags=re.MULTILINE)

    # --- Step 6: Remove Links and Images ---
    # Images: ![alt](url) -> remove entire image
    text = re.sub(r'!\[.*?\]\([^\)]*\)', '', text)
    # Links: [text](url) -> keep `text`
    text = re.sub(r'\[([^\]]+)\]\([^\)]*\)', r'\1', text)

    # --- Step 7: Remove Inline Markdown Elements ---
    text = re.sub(r'`([^`]+)`', r'\1', text)
    # Bold / Italic - ensure we catch both, ordering matters (*** then ** then *)
    text = re.sub(r'\*{3}([^*]+)\*{3}', r'\1', text)
    text = re.sub(r'_{3}([^_]+)_{3}', r'\1', text)
    text = re.sub(r'\*{2}([^*]+)\*{2}', r'\1', text)
    text = re.sub(r'_{2}([^_]+)_{2}', r'\1', text)
    text = re.sub(r'\*([^*]+)\*', r'\1', text)
    text = re.sub(r'_([^_]+)_', r'\1', text)
    # Strikethrough
    text = re.sub(r'~~([^~]+)~~', r'\1', text)

    # --- Step 8: Remove List Markers ---
    text = re.sub(r'^\s*(?:[-*+]|\d+\.)\s+', '', text, flags=re.MULTILINE)

    # --- Step 9: Final Whitespace & Paragraph Normalization ---
    # Strip spaces from each line
    lines = [line.strip() for line in text.split('\n')]
    text = '\n'.join(lines)

    # Convert tabs and multiple spaces to single space
    text = text.replace('\t', ' ')
    text = re.sub(r' {2,}', ' ', text)

    # Consolidate multiple newlines to paragraph separator `\n\t`
    text = re.sub(r'\n{2,}', '\n\t', text)

    # --- Step 10: Final Trimming ---
    text = text.strip()
    text = re.sub(r'^[\n\t]+', '', text)
    text = re.sub(r'[\n\t]+$', '', text)

    return text


def messages_to_mpj(messages):
    contents = []
    for message in messages:
        if message['role'] == 'user':
            obj = dict(role='user', parts=[dict(text=message['content'])])
        elif message['role'] == 'assistant':
            obj = dict(role='model', parts=[dict(text=message['content'])])
        else:
            obj = {}
        contents.append(obj)
    return contents
