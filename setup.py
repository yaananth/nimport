from setuptools import setup, find_packages

NAME = "nimport"
VERSION = '0.9.5'

setup(
    name=NAME,
    version=VERSION,
    packages=find_packages()
    #install_requires=["PyGithub", "websocket-client", "nbformat"]
)
