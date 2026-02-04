# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from os import environ
from github import Github, UnknownObjectException
from urllib3 import disable_warnings


github_token    = environ.get('GITHUB_TOKEN', '')
github_name     = environ.get('GITHUB_NAME', '')
github_email    = environ.get('GITHUB_EMAIL', '')

# The useless urllib3 warning is too maddening for an ordinary human being.
disable_warnings()


# Repo
def connectto_repo(organization=None,
                   repository_name=None,
                   private=False):
    """
    Establish a connection with a GitHub repository.

    Args:
        organization (str, optional): The name of the organization. If not provided,
            the repository is assumed to be owned by the authenticated user.
        repository_name (str): The name of the repository.
        private (bool, optional): Whether the repository is private. Defaults to False.

    Returns:
        github.Repository.Repository: The GitHub repository object if the connection is successful.
        None: If the connection fails.

    Raises:
        github.UnknownObjectException: If the repository does not exist.

    Note:
        The function requires the following environment variables to be set:
        - GITHUB_TOKEN: The personal access token for authentication.
        - GITHUB_NAME: The name of the authenticated user.
        - GITHUB_EMAIL: The email of the authenticated user.

    """

    gh = Github(github_token, verify=False)
    if organization:
        org = gh.get_organization(organization)
        try:
            repo = org.get_repo(f'{repository_name}')
        except UnknownObjectException:
            # print('Can not connect YOU to this repo in this organization')
            repo = None
        return repo
    else:
        user = gh.get_user()
        try:
            repo = user.get_repo(repository_name)
        except UnknownObjectException:
            # print('Can not connect YOU to this repo')
            repo = None
        return repo


def read_file(repository,
              file_path):
    """
    Read the contents of a file in a GitHub repository.

    Args:
        repository (github.Repository.Repository): The GitHub repository object.
        file_path (str): The path to the file in the repository, formatted as
            'directory_in_repo/subdirectory/file.ext'.

    Returns:
        str: The contents of the file as a string. If the file does not exist, an empty string is returned.

    Raises:
        github.UnknownObjectException: If the file does not exist in the repository.

    Note:
        This function assumes that the repository object has already been authenticated and connected.
    """
    try:
        # Get the file if it exists
        ingested_file = repository.get_contents(file_path)
        content = ingested_file.decoded_content.decode("utf-8")

    except UnknownObjectException:
        # The file doesn't exist
        # print('The file does not exist')
        content = ''

    return content
