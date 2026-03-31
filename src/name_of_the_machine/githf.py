# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
import sys
from os import path
import yaml
import urllib.request
import urllib.error


def download_github_file(owner, repo, file_path, token):
    """
    Downloads a file from a GitHub repository using the GitHub REST API.
    We request the raw content by using the 'application/vnd.github.v3.raw' accept header.
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}"

    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3.raw",
        "User-Agent": "Name-of-the-Machine"
    }

    req = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            return response.read()
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.reason}")
        error_info = e.read().decode('utf-8')
        print(f"Details: {error_info}")
        return None
    except urllib.error.URLError as e:
        print(f"URL Error: {e.reason}")
        return None


def fetch_instructions(config):
    """Retrieve the system prompt from a private GitHub repo.
    Falls back to the local machina.yaml if GitHub is unreachable.
    Returns the 'name' of the Machine in dashed format.
    Returns the 'description' field from the YAML as the system prompt string.
    """
    try:
        raw_yaml = download_github_file(
            owner=config.machine_organization_name,
            repo=config.private_repo_with_text,
            file_path=config.system_prompt_file,
            token=config.github_token
        )
    except Exception as e:
        print(f"Warning: could not fetch the instructions from GitHub: {e}",
              file=sys.stderr)
        local_path = path.join(path.dirname(__file__), 'machina.yaml')
        with open(local_path, 'r') as f:
            raw_yaml = f.read()

    # Parse
    parsed = yaml.safe_load(raw_yaml)
    name = parsed.get('name')
    config.name = name
    instructions = parsed.get('description', 'You are a helpful assistant.')
    config.instructions = instructions
    return name, instructions
