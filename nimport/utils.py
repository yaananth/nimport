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
        # this sends a blob of javascript to be executed in the nteract window
        js = '''var o = window.location.href.split("/"); o[o.length - 1] = "''' + \
            path + '''"; window.location = o.join("/");'''
        display(Javascript(js))

def clone_repo(git_url):
    '''
    clone a git repo, cleaning previous install
    '''
    assert git_url.endswith('.git')
    import shutil
    dirname = git_url.split('/')[-1].split('.')[0]
    if os.path.isdir(dirname):
        shutil.rmtree(dirname)
    cmd = 'git clone --depth=1 ' + git_url
    assert 0 == subprocess.check_output(cmd, shell=True)
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
        rc['url'] = components.scheme + "://" + components.netloc + components.path
    return rc

def dump_params(params):
    lines = [k + ' = ' + json.dumps(v) for k, v in params.items()]
    return '\n'.join(lines)