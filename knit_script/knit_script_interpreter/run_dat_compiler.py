"""used to run js DAT compiler"""

import os
import subprocess
from typing import Optional

from Naked.toolshed.shell import execute_js


def knitout_to_dat(knitout_file_name: str, dat_file_name: Optional[str] = None, js_compiler_file:Optional[str] = None) -> bool:
    """
    Creates a dat file for the corresponding knitout
    Parameters
    ----------
    knitout_file_name: the filename of the knitout to compile
    dat_file_name: the dat filename to compile to. Defaults to the same as knitout
    :param js_compiler_file: Specification for location of javascript code to convert knitout to dat
    """
    directory = os.path.dirname(__file__)
    # directory = 'C:\\Users\\Megan\\bin'
    if js_compiler_file is None:
        js_compiler_file = f"{directory}{os.path.sep}knitout_to_dat.js"

    arguments = f"{knitout_file_name} {dat_file_name}"
    print(f"################  Converting {knitout_file_name} to DAT FILE ########")
    success = execute_js(js_compiler_file, arguments)
    return success

