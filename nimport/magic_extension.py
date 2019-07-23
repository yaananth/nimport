'''
https://ipython.readthedocs.io/en/stable/config/extensions/
'''
from .lib.nimport_magic import Nimportmagic as Magic

def load_ipython_extension(ip):
    ip.register_magics(Magic)


def unload_ipython_extension(ip):
    # nothing here for now
    print("unloaded")
