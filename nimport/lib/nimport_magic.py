from IPython.core.magic import magics_class, line_magic, Magics, Configurable
from IPython.display import display, Javascript
from IPython.lib import backgroundjobs as bg

from .constants import Constants
from .tokens import Tokens
from .parser import Parser
from ..providers.constants import Constants as ProviderConstants
from ..providers.github import GithubProvider

import logging
import asyncio
import time
import websocket
import json
from threading import Thread
import random


_MAGIC_NAME = "nimport"
_WS_BaseUrl = "wss://connect.websocket.in/nimport?room_id={0}"
jobs = bg.BackgroundJobManager()


@magics_class
class Nimportmagic(Magics, Configurable):
    _providers = {}

    githubProvider = GithubProvider()
    _providers[ProviderConstants.GitHub] = githubProvider

    _gotMessage: bool = False

    @line_magic(Constants.MAGIC_NAME)
    def run(self, line):
        results = Parser.parse(line)
        providerName = results[Tokens.Provider]
        provider = self._providers[providerName]
        if provider:
            fileContents = provider.getFile(
                results[Tokens.Container], results[Tokens.Path], results[Tokens.ProviderOptions])
            display(fileContents)
            self.waitForParams()
        else:
            display("Unknown provider: " + providerName)

    @classmethod
    def waitForParams(self):
        url = _WS_BaseUrl.format(self.getRoomId())
        ws = websocket.create_connection(url)
        display(Javascript(self.getJSContent(url)))
        result = json.loads(ws.recv())
        display(result)
        ws.close()

    @classmethod
    def getJSContent(self, url):
        js = """
        var websocket = new WebSocket("%s");

        websocket.onopen = function (event) {
            websocket.send(JSON.stringify({
                link: window.location.href
            }));
        };
        """ % (url)
        return js

    @classmethod
    def getRoomId(self):
        return random.randint(0, 99999999999999999999)
