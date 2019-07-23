from IPython.display import display, Javascript
import nbformat as nbf
import json
import os


def open_nb(path, params=None):
    '''edit papermill parameters and redirect to new notebook in same project'''
    assert os.path.isfile(path)
    assert path.endswith('.ipynb')
    if params:
        # find parameter cell in notebook
        nb = nbf.read(path, nbf.NO_CONVERT)
        parameter_cells = [c for c in nb.cells if 'parameters' in c.get(
            'metadata', {}).get('tags', [])]
        pc = parameter_cells[0] if parameter_cells else None
        if pc:
            # overwrite cell contents, write notebook
            lines = [k + '=' + json.dumps(v) for k, v in params.items()]
            pc['source'] = '\n'.join(lines)
            nbf.write(nb, path)

    # redirect
    js = '''var o = window.location.href.split("/"); o[o.length - 1] = "''' + \
        path + '''"; window.location = o.join("/");'''
    display(Javascript(js))
