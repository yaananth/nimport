from setuptools import setup, find_packages

NAME = "nimport"
VERSION = '0.10.17'

INSTALL_REQUIRES = [
    # Comment these while testing locally if using samples/sample.ipynb for faster devloop
    'PyGithub',
    'websocket-client',
    'IPython',
    'nbformat',
]

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name=NAME,
    version=VERSION,
    author="Yash",
    author_email="yashanantha@outlook.com",
    description="A cool way to import notebooks into notebooks! Also can parameterize notebooks when it loads!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yaananth/nimport",
    install_requires=INSTALL_REQUIRES,
    packages=find_packages(exclude=['tests'])
)
