from .provider import Provider
from .constants import Constants
from ..lib.parser import Parser
from ..utils import clone_repo
from github import Github
import requests
import json
import sys
import os


class GithubProvider(Provider):
    def clone(self, container, path, options):
        repoName = "https://github.com/" + container + ".git"
        clone_repo(repoName)
        return ""

    # https://pygithub.readthedocs.io/en/latest/examples/Repository.html#get-a-specific-content-file
    def getFile(self, container, path, options):
        if Constants.OptionsToken in options:
            token = Parser.normalize(options[Constants.OptionsToken])
            # Authorized
            g = Github(token)
        else:
            # Anonymous
            g = Github()

        repo = g.get_repo(container)
        result = repo.get_contents(path)
        response = requests.get(result.raw_data["download_url"])
        return response.json()

    def getContainerName(self, container):
        return container.split("/")[-1]
