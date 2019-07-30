# Nimport

## Requirements
- Needs `git` to be installed for `github` provider to work

## Use
```
!pip install --upgrade nimport
%load_ext nimport
```

## Examples
- Get a file from public repo and navigate to that file
    ```
    %nimport container="yaananth/hack-sample-note2" path="one.ipynb" provider="github" providerOptions={} navigate="trueOrAnythingHere"
    ```

- Get a file from public repo and display a link to that file
    ```
    %nimport container="yaananth/hack-sample-note2" path="one.ipynb" provider="github" providerOptions={}
    ```

- Get a file from private repo and navigate to that file
    ```
    %nimport container="yaananth/hack-sample-note2" path="one.ipynb" provider="github" providerOptions={{"token":"PATTOKENHERE"}} navigate="trueOrAnythingHere"
    ```

- Clone a public repo and navigate to the boot strap file

    Needs `git` to be accessible
    ```
    %nimport container="yaananth/pipeline-delays" path="delays.ipynb" provider="github" providerOptions={"clone":"true"}
    ```

- Parameterize notebook from URL    
    ```
    from nimport.utils import open_nb, load_params
    params = load_params(currentUrl)
    open_nb("pipeline-delays/delays.ipynb", params, redirect=True)
    ```

- Get URL from browser into python (Javascript to python communication in nteract)
    ```
    clientData = {}
    def callback(x):
        global clientData
        clientData = x
    parse_client_data(callback)
    print(clientData)
    ```    

## Develop

### Package
`pip install -r requirements.txt`

`python setup.py sdist`

### Publish
`pip install twine`

`twine upload dist/*`

### Test
- Load [sample.ipynb](https://github.com/yaananth/nimport/blob/master/samples/sample.ipynb)

# Resources
- https://packaging.python.org/guides/using-testpypi/
- https://libraries.io/pypi/twine
- https://test.pypi.org/manage/projects/
- https://pygithub.readthedocs.io/en/latest/introduction.html
