# Nimport

## Use
```
!pip install PyGithub
!pip install websocket-client
!pip install nbformat
!pip install --index-url https://test.pypi.org/simple/ nimport==0.9.6
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
    %nimport container="yaananth/hack-sample-note2" path="one.ipynb" provider="github" providerOptions={"clone":"true"} navigate="trueOrAnythingHere"
    ```

## Develop

### Package
`pip install -r requirements.txt`
`python setup.py sdist`

### Publish
`pip install twine`
`twine upload --repository-url https://test.pypi.org/legacy/ dist/*`

### Test
- Load [sample.ipynb](https://github.com/yaananth/nimport/blob/master/samples/sample.ipynb)

# Resources
- https://packaging.python.org/guides/using-testpypi/
- https://libraries.io/pypi/twine
- https://test.pypi.org/manage/projects/
- https://pygithub.readthedocs.io/en/latest/introduction.html
