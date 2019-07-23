from nimport.providers.provider import Provider
from github import Github
import requests
from IPython.display import display


@Provider.register
class GithubProvider():
    # https://pygithub.readthedocs.io/en/latest/examples/Repository.html#get-a-specific-content-file
    def getFile(self, container: str, path: str):
        g = Github("Use your own pat token here for now")
        repo = g.get_repo(container)
        result = repo.get_contents(path)
        response = requests.get(result.raw_data["download_url"])
        return response.json()
