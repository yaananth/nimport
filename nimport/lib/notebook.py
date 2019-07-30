import json
from urllib.parse import urlparse, ParseResult, urlunparse
from IPython.display import display

ExtensionName = '.ipynb'


def write(content, name):
    notebookname = name
    display("Creating/updating file.." + notebookname)
    with open(notebookname, 'w') as outfile:
        json.dump(content, outfile)


class NoteBookUrl(object):
    @classmethod
    def __init__(self, url):
        self._url = url
        self.parse()

    @classmethod
    def parse(self):
        self._urlParsed = urlparse(self._url)
        self._name = self._urlParsed.path.split('/')[-1].split('.')[0]

    @classmethod
    def getName(self):
        return self._name

    @classmethod
    def getNewLink(self, newName):
        existing = self._urlParsed
        existingPath = existing.path.split('/')[:-1]
        existingPath.append(newName)
        newPathString = "/".join(existingPath)
        newUrl = ParseResult(scheme=existing.scheme, netloc=existing.netloc,
                             path=newPathString, params='', query='', fragment='')
        return urlunparse(newUrl)
