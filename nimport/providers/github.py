from nimport.providers.provider import Provider
from github import Github
import requests
from IPython.display import display
from nimport.lib.parser import Parser
import json

_Token = "token"


@Provider.register
class GithubProvider():
    # https://pygithub.readthedocs.io/en/latest/examples/Repository.html#get-a-specific-content-file
    def getFile(self, container: str, path: str, options: dict):
        if _Token in options:
            token = Parser.normalize(options[_Token])
            # Authorized
            g = Github(token)
        else:
            # Anonymous
            g = Github()

        repo = g.get_repo(container)
        result = repo.get_contents(path)
        response = requests.get(result.raw_data["download_url"])
        return response.json()
