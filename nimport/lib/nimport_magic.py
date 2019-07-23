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

import logging
import asyncio
import time
import websocket
import json
from threading import Thread
import random
import ssl


_MAGIC_NAME = "nimport"
_WS_BaseUrl = "wss://connect.websocket.in/nimport?room_id={0}"
_Result_Content = "content"
_Result_Url = "url"
jobs = bg.BackgroundJobManager()


@magics_class
class Nimportmagic(Magics, Configurable):
    _providers = {}

    githubProvider = GithubProvider()
    _providers[ProviderConstants.GitHub] = githubProvider

    _gotMessage: bool = False

    _result = {}

    @line_magic(Constants.MAGIC_NAME)
    def run(self, line):
        display(line)
        results = Parser.parse(line)
        providerName = results[Tokens.Provider]
        provider = self._providers[providerName]
        if provider:
            providerResult = provider.get(
                results[Tokens.Container], results[Tokens.Path], results[Tokens.ProviderOptions])
            self._result[_Result_Content] = providerResult
            self.waitForParams(results, provider)
        else:
            display("Unknown provider: " + providerName)

    @classmethod
    def waitForParams(cls, inputs, provider):
        display("Trying to get the current link...")
        url = _WS_BaseUrl.format(cls.getRoomId())
        ws = websocket.create_connection(
            url, sslopt={"cert_reqs": ssl.CERT_NONE})
        display(Javascript(cls.getJSWsContent(url)))
        data = json.loads(ws.recv())
        cls._result[_Result_Url] = data[_Result_Url]
        ws.close()
        cls.postContent(inputs, provider)

    @classmethod
    def postContent(cls, inputs, provider):
        display("Got link...making final adjustments")
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
        if Tokens.Navigate in inputs:
            display(Javascript(cls.getJSPostContent(newUrl)))
        else:
            display("Navigate to:")
            display(newUrl)

    @classmethod
    def getJSWsContent(cls, url):
        js = """
        var websocket = new WebSocket("%s");

        websocket.onopen = function (event) {
            websocket.send(JSON.stringify({
                url: window.location.href
            }));
        };
        """ % (url)
        return js

    @classmethod
    def getJSPostContent(cls, url):
        js = """
        if (window) {
            window.location.href = "%s"
        }
        """ % (url)
        return js

    @classmethod
    def getRoomId(cls):
        return random.randint(0, 99999999999999999999)
