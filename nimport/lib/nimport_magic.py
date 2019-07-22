from IPython.core.magic import magics_class, line_magic, Magics, Configurable
from nimport.lib.constants import Constants
import logging

_MAGIC_NAME = "nimport"


@magics_class
class Nimportmagic(Magics, Configurable):

    @line_magic(Constants.MAGIC_NAME)
    def run(self, line):
        print('hi ' + line)
