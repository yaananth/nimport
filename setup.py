from setuptools import setup, find_packages

NAME = "nimport"
VERSION = '0.9.5'

INSTALL_REQUIRES = [
    'PyGithub',
    'websocket-client',
    'IPython',
    'nbformat',
]

setup(
    name=NAME,
    version=VERSION,
    install_requires=INSTALL_REQUIRES,
    packages=find_packages()
)
