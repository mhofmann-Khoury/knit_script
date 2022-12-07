"""used to run js DAT compiler"""

import os
from typing import Optional

from Naked.toolshed.shell import execute_js


def knitout_to_dat(knitout_file_name: str, dat_file_name: Optional[str] = None) -> bool:
    """
    Creates a dat file for the corresponding knitout
    Parameters
    ----------
    knitout_file_name: the filename of the knitout to compile
    dat_file_name: the dat filename to compile to. Defaults to the same as knitout
    """
    cur_directory = os.path.dirname(__file__)
    script_directory = f"{cur_directory}{os.path.sep}dat-compiler{os.path.sep}knitout-backend-swg-master"
    script = f"{script_directory}{os.path.sep}knitout-to-dat.js"
    if dat_file_name is None:
        knitout_name = knitout_file_name[:knitout_file_name.rindex(".")]
        dat_file_name = f"{knitout_name}.dat"
    arguments = f"{knitout_file_name} {dat_file_name}"
    print(f"################  Converting {knitout_file_name} to DAT FILE ########")
    success = execute_js(script, arguments)
    return success
