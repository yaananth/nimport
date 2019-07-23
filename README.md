# nimport

## package
`pip install -r requirements.txt`
`python setup.py sdist`

## publish
`pip install twine`
`twine upload --repository-url https://test.pypi.org/legacy/ dist/*`

## use
`pip install --index-url https://test.pypi.org/simple/ nimport==0.3`

# Resources
- https://packaging.python.org/guides/using-testpypi/
- https://libraries.io/pypi/twine
- https://test.pypi.org/manage/projects/
- https://pygithub.readthedocs.io/en/latest/introduction.html