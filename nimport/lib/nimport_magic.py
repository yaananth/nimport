from IPython.core.magic import magics_class, line_magic, Magics, Configurable
from IPython.display import display, Javascript
from IPython.lib import backgroundjobs as bg

from .constants import Constants
from .tokens import Tokens
from .parser import Parser
from ..providers.provider import Provider
from ..providers.constants import Constants as ProviderConstants
from ..providers.github import GithubProvider
from .notebook import write, NoteBookUrl, ExtensionName
from ..utils import parse_client_data

import logging
import asyncio
import time
import json
from threading import Thread

_MAGIC_NAME = "nimport"
_Result_Content = "content"
_Result_Url = Constants.CLIENT_DATA_URL
jobs = bg.BackgroundJobManager()


@magics_class
class Nimportmagic(Magics, Configurable):
    _providers = {}

    githubProvider = GithubProvider()
    _providers[ProviderConstants.GitHub] = githubProvider

    _result = {}

    @line_magic(Constants.MAGIC_NAME)
    def run(self, line):
        results = Parser.parse(line)
        providerName = results[Tokens.Provider]
        provider = self._providers[providerName]
        if provider:
            providerResult = provider.get(
                results[Tokens.Container], results[Tokens.Path], results[Tokens.ProviderOptions])
            self._result[_Result_Content] = providerResult
            if Tokens.Navigate in results:
                self.waitForParams(results, provider)
            else:
                print("Successful!")
        else:
            print("Unknown provider: " + providerName)

    @classmethod
    def waitForParams(cls, inputs, provider):
        print("Asked to navigate, so trying to get the current client data...")

        def callback(data):
            print("Got client data...")
            print(data)
            cls._result[_Result_Url] = data[_Result_Url]
            cls.postContent(inputs, provider)

        parse_client_data(callback)

    @classmethod
    def postContent(cls, inputs, provider):
        content = cls._result[_Result_Content]
        url = cls._result[_Result_Url]
        newNoteBookName = inputs[Tokens.Path]
        if not content:
            # this is clone so notebook name should have the repo name
            newNoteBookName = provider.getContainerName(
                inputs[Tokens.Container]) + "/" + newNoteBookName

        notebookUrl = NoteBookUrl(url)
        if content:
            write(content, newNoteBookName)
        newUrl = notebookUrl.getNewLink(newNoteBookName)
        print("Navigating to..." + newUrl)
        display(Javascript(cls.getJSPostContent(newUrl)))

    @classmethod
    def getJSPostContent(cls, url):
        js = """
        if (window) {
            window.location.href = "%s"
        }
        """ % (url)
        return js
