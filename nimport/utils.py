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
_WS_BaseUrl = "wss://connect.websocket.in/v2/400?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6ImY0NmNjY2FmZDE1ODM0ZDZmY2E5M2RlOWYzNDA1MjNhMDRmZmEyZGRjY2QzNjlmOTYyYTBhYTA2Nzg2NzM3YzI4ZTc4OTllODJkYTY2YjUzIn0.eyJhdWQiOiI4IiwianRpIjoiZjQ2Y2NjYWZkMTU4MzRkNmZjYTkzZGU5ZjM0MDUyM2EwNGZmYTJkZGNjZDM2OWY5NjJhMGFhMDY3ODY3MzdjMjhlNzg5OWU4MmRhNjZiNTMiLCJpYXQiOjE1NzkwMTIwMTYsIm5iZiI6MTU3OTAxMjAxNiwiZXhwIjoxNjEwNjM0NDE2LCJzdWIiOiIzMzciLCJzY29wZXMiOltdfQ.eAzGpPU_Dr6Qy8Xx-je3BepxIXnMQTtGlb0LdL_70z7dyuYiz7D-3WquI0dj0HRsy3-sTwU5Wpl7xJrq6tAYiKddAowOnKoLCpJY9MbSLOXxlwGSsZ_PaLdMEOuCc6cYewljHzkqE1pYrDG7Wuf4PXojgGVMFKYg-gW2eDIChfnECsFplYtPU3RjseVVwoxEOBSqJBR53GxjmI2PrWszngP080MZKyjq2XpdCXzjmMdslfuIiLdTKWQW6TOFsT-5QqU-RYbVt45miDkR2vK6ptTuTRdPG6IMfOebIqRMOgbeIJjj12R_FCkjwTh2awNZNsoH8X63w4DPB7MZmQ4A9ECJGhhkwqynWD9plWc0m4hsvTGFCdgWMLh81VH4EmH2VAoxO6599sBT5khdlZ7fy2RrY_FdVUVO4VmfHPzFwr8SUkL6toZl_8vXaxE8iReilDuP5-J1qJ-iuDA75z-hNPjdD_bYFfN8W_obIYbuUpCCptNUNiws2o-aiz6-qL_kx375WP2QZ3spN0bCOyvcdwHOPpU4cyYPPpPTDpg54T2_Me4dNCllJ4dS9wUScK253dqQ4ubC3LbqmF5CaEg_yfAmgP8rbSXi6zka0V-YDsQp8zXby9BzThCpGUMe6gEwxb8T_R0W1Q91MNoURdfLmzpd5UX52PomC3kN022AyLY&room_id={0}"


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
