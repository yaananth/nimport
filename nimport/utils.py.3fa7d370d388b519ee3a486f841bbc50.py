from IPython.display import display, Javascript
from urllib import parse
import nbformat
import json
import os
import subprocess
import shutil
import sys


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


def tokenize(path, params, startToken='{', endToken='}'):
    # load query
    assert os.path.isfile(path)
    with open(path, 'rt') as f:
        contents = f.read()
        assert contents, 'file was empty?'

    # enhance contents
    for k, v in params.items():
        if isinstance(v, str):
            v = '"' + v + '"'
            contents = contents.replace(startToken + k + endToken, v)
    return contents


def clone_repo(repo):
    '''
    clone a git repo, cleaning previous install
    '''
    if not repo:
        return
    assert repo.endswith('.git')
    print("Cloning... " + repo)
    import shutil
    dirname = repo.split('/')[-1].split('.')[0]
    if os.path.isdir(dirname):
        shutil.rmtree(dirname)
    cmd = 'git clone --depth=1 ' + repo
    subprocess.call(cmd, shell=True)
    assert os.path.isdir(dirname)
    if dirname not in sys.path:
        sys.path.append(dirname)
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
