# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from os import environ


settings = dict(
    github_token                = environ.get('GITHUB_TOKEN', ''),
    github_name                 = environ.get('GITHUB_NAME', ''),
    github_email                = environ.get('GITHUB_EMAIL', ''),
    provider_api_key            = environ.get('PROVIDER_API_KEY', ''),
    provider                    = environ.get('PROVIDER', ''),
    machine_organization_name   = environ.get('MACHINE_ORGANIZATION_NAME', 'machine-name'),
    private_repo_with_text      = environ.get('PRIVATE_REPO_WITH_TEXT','machine_name'),
    system_prompt_file          = environ.get('SYSTEM_PROMPT_FILE', 'machina.yaml'),
    name                        = '',
    instructions                = ''
)