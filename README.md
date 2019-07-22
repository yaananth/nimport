# nimport

## package
`python setup.py sdist`

## publish
`twine upload --repository-url https://test.pypi.org/legacy/ dist/*`

## use
`pip install --index-url https://test.pypi.org/simple/ nimport==0.2`

# Resources
- https://packaging.python.org/guides/using-testpypi/
- https://libraries.io/pypi/twine
- https://test.pypi.org/manage/projects/