from setuptools import setup, find_packages

NAME = "nimport"
VERSION = '0.4'
with open('requirements.txt') as f:
    requires = f.read().splitlines()
    
setup(
    name=NAME,
    version=VERSION,
    packages=find_packages(),
    install_requires=requires
)
