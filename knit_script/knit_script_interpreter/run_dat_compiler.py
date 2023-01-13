"""used to run js DAT compiler"""

import os
from typing import Optional

from Naked.toolshed.shell import execute_js


def knitout_to_dat(knitout_file_name: str, dat_file_name: Optional[str] = None, js_compiler_file:Optional[str] = None) -> bool:
    """
    Creates a dat file for the corresponding knitout
    :param knitout_file_name:  the filename of the knitout to compile
    :param dat_file_name:  the dat filename to compile to. Defaults to the same as knitout
    :param js_compiler_file: Specification for location of javascript code to convert knitout to dat
    """
    directory = os.path.dirname(__file__)
    if js_compiler_file is None:
        js_compiler_file = f"{directory}{os.path.sep}knitout-to-dat.js"

    arguments = f"{knitout_file_name} {dat_file_name}"
    print(f"\n################Converting {knitout_file_name} to DAT file {dat_file_name} ########\n")
    success = execute_js(js_compiler_file, arguments)
    return success

