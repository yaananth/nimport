from nimport.providers.provider import Provider
from nimport.providers.constants import Constants

from github import Github
import requests
from IPython.display import display
from nimport.lib.parser import Parser
import json
import sys
import os


class GithubProvider(Provider):
    def clone(self, container: str, path: str, options: dict):
        rmFolder = "rm -rf " + self.getContainerName(container)
        command = "git clone --depth=1 https://github.com/" + container + ".git"
        display(rmFolder)
        display(command)
        os.system(rmFolder)
        os.system(command)
        return ""

    # https://pygithub.readthedocs.io/en/latest/examples/Repository.html#get-a-specific-content-file
    def getFile(self, container: str, path: str, options: dict):
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

    def getContainerName(self, container: str):
        return container.split("/")[-1]
