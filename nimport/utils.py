from IPython.display import display, Javascript
from urllib import parse
import nbformat
import json
import os
import subprocess
import shutil
import sys
import websocket
import random
import ssl
import datetime

from .lib.constants import Constants


# Yeah, there's token here, but it doesn't matter, it's just a websocket we use...u can steal it, but u get nothing, we get nothing...
_WS_BaseUrl = "wss://connect.websocket.in/v2/400?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjY1NDk1YzNlNzFkMzY4NGY2YjgzNWNkOWVkMmVlNmQ4OWYyNWY3NjY2M2IzNTg5NGU2MDQ1NTFkMjUxYjU2OGMzYWY1MTk1MzQwODQxODI3In0.eyJhdWQiOiI2IiwianRpIjoiNjU0OTVjM2U3MWQzNjg0ZjZiODM1Y2Q5ZWQyZWU2ZDg5ZjI1Zjc2NjYzYjM1ODk0ZTYwNDU1MWQyNTFiNTY4YzNhZjUxOTUzNDA4NDE4MjciLCJpYXQiOjE1NzQwOTQ5MDEsIm5iZiI6MTU3NDA5NDkwMSwiZXhwIjoxNjA1NzE3MzAxLCJzdWIiOiIyNyIsInNjb3BlcyI6W119.vAzoguucx4EL4wBZKeKZ2ubCNU0qmDWOOtpLLvzu8BOsO9cVvRp5kW9m_HXLyfdtWt_ReUAW6a-KKsswIPlY3rk_3SBbddkY7HEPIuq82vLDgYYy-MZlAh3e1OO4HX3YXnn6RqoXSSxQVAXJIWfALUnz8K0eDSoL4vB_ba2-9tY49mlHyn7u50LrWeGY8NCXyN3XqrTRj-S_pqS1G3sMMnwPhocyLGxGiJAUK8ujo9uE1AJtkoGOidDigmQ1q4XRZmqVhUCZJP2UN3w--mayhlkGcEYsF1-9wkhUFfllEa4m5orW40My-wybLmvKBDSQ6eNRQdGLa0bTdwUtheJDFJNt5MBYmgvafABiSozP5zMyVUx1ahKjFYzlOmgUq33_ii99qgbhBZ0K25Nn73m9i5963bf986t7Zao_QkEOvjqJZYUEBfQrcQSnmcIHMpf73aMdXw01pZLMfDH3Pu0WzZXu3Tlt3yNcAooDKrx8xEyo8q-H132AFy48OS3LYoLzF220DCSY1eg8s8fc2_cpsxYlp4xg_-cUEpmZGeoUqBW6MaYygF6JGsUPDuhZ4m_g-06ZakBlnxn-O9VG-Ck13tUEezIn_cc4LCRTZc1pOM9GsCIj-HnVMMxpSFMEGO0aToHU8-acA3z-yTZCcwzgktYv7dn4K2s2AYOkDwqwaIg&room_id={0}"


def open_nb(path, params=None, redirect=True):
    '''
    edit papermill parameters and redirect to new notebook in same project
    '''
    assert os.path.isfile(path)
    assert path.endswith('.ipynb')
    if params:
        # find parameter cell in notebook
        nb = nbformat.read(path, nbformat.NO_CONVERT)
        parameter_cells = [c for c in nb.cells if 'parameters' in c.get(
            'metadata', {}).get('tags', [])]
        pc = parameter_cells[0] if parameter_cells else None
        if pc:
            # overwrite cell contents, write notebook
            pc['source'] = dump_params(params)
            nbformat.write(nb, path)

    # redirect
    if redirect:
        redirectTo(path)


def redirectTo(path, basePath=""):
    # this sends a blob of javascript to be executed in the nteract window
    if basePath:
        js = """
        window.location = "%s" + "/" + "%s";
        """ % (basePath, path)
    else:
        js = """
        var o = window.location.href.split("/"); 
        o[o.length - 1] = "%s";
        window.location = o.join("/");
        """ % (path)
    display(Javascript(js))


def tokenize(path, params, startToken='{', endToken='}', transform = False):
    # load query
    assert os.path.isfile(path)
    with open(path, 'rt') as f:
        contents = f.read()
        assert contents, 'file was empty?'

    # enhance contents
    for k, v in params.items():
        if transform:
            if isinstance(v, str):
                v = '"' + v + '"'        
        contents = contents.replace(startToken + k + endToken, v)
    return contents


def clone_repo(repo):
    '''
    updates a git repo, cleaning previous install if needed
    '''
    if not repo:
        return
    
    assert repo.endswith('.git'), repo + ' is not a git repo'
    start = datetime.datetime.now()
    dirname = repo.split('/')[-1].split('.')[0]
    origin = os.getcwd()
    if os.path.isdir(os.path.join(dirname, '.git')):
        # pull master
        cmd = ' && '.join((
                'cd ' + dirname,
                'git reset --hard', 
                'git clean -xdf', 
                'git checkout master', 
                'git pull'))
    else:
        # clone
        if os.path.isdir(dirname):
            shutil.rmtree(dirname)
        cmd = 'git clone ' + repo
   
    print(cmd)
    rc = subprocess.call(cmd, shell=True)
    assert 0 == rc, 'something failed!'
    assert os.path.isdir(dirname)
    if dirname not in sys.path:
        sys.path.append(dirname)
    os.chdir(origin)
    print('Finished in', datetime.datetime.now() - start)
    return os.path.abspath(dirname)


def parse_params(url):
    '''
    azure notebooks does not allow access to URL parameters.
    this is a cheap function to parse them when provided manually.
    '''
    rc = {}
    if url:
        components = parse.urlsplit(url)
        rc = dict(parse.parse_qsl(components.query))
        rc['url'] = components.scheme + "://" + \
            components.netloc + components.path
        rc['baseUrl'] = "/".join(rc['url'].split("/")[:-1])
    return rc


def dump_params(params):
    lines = [k + ' = ' + json.dumps(v) for k, v in params.items()]
    return '\n'.join(lines)


def parse_client_data(callback):
    roomId = random.randint(0, 99999999999999999999)
    url = _WS_BaseUrl.format(roomId)

    def get_JS_WsContent(url):
        return """
            var websocket = new WebSocket("%s");

            websocket.onopen = function (event) {
                websocket.send(JSON.stringify({
                    "%s": window.location.href
                }));
            };
            """ % (url, Constants.CLIENT_DATA_URL)

    ws = websocket.create_connection(
        url, sslopt={"cert_reqs": ssl.CERT_NONE})
    display(Javascript(get_JS_WsContent(url)))
    data = json.loads(ws.recv())
    ws.close()
    callback(data)
