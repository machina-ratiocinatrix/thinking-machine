# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from os import environ
from dataclasses import dataclass, field


@dataclass
class Config:
    github_token: str               = field(default_factory=lambda: environ.get('GITHUB_TOKEN', ''))
    github_name: str                = field(default_factory=lambda: environ.get('GITHUB_NAME', ''))
    github_email: str               = field(default_factory=lambda: environ.get('GITHUB_EMAIL', ''))
    provider_api_key: str           = field(default_factory=lambda: environ.get('PROVIDER_API_KEY', ''))
    provider: str                   = field(default_factory=lambda: environ.get('PROVIDER', 'OpenAI'))
    machine_organization_name: str  = field(default_factory=lambda: environ.get('MACHINE_ORGANIZATION_NAME', 'machina-ratiocinatrix'))
    private_repo_with_text: str     = field(default_factory=lambda: environ.get('PRIVATE_REPO_WITH_TEXT','thinking_machine'))
    system_prompt_file: str         = field(default_factory=lambda: environ.get('SYSTEM_PROMPT_FILE', 'machina.yaml'))
    name: str                       = field(default_factory=lambda: environ.get('MACHINE-NAME','thinking-machine'))
    instructions: str               = field(default_factory=lambda: environ.get('MACHINE-DESCRIPTION','The Assistant is Thinking-Machine.'))