"""used to run js DAT compiler"""

from typing import Optional

from Naked.toolshed.shell import execute_js
from pkg_resources import resource_stream


def knitout_to_dat(knitout_file_name: str, dat_file_name: Optional[str] = None) -> bool:
    """
    Creates a dat file for the corresponding knitout
    :param knitout_file_name:  the filename of the knitout to compile
    :param dat_file_name:  the dat filename to compile to. Defaults to the same as knitout
    """
    js_compiler_file = resource_stream("knit_script.knitout_compilers", "knitout-to-dat.js").name
    arguments = f"{knitout_file_name} {dat_file_name}"
    print(f"\n################Converting {knitout_file_name} to DAT file {dat_file_name} ########\n")
    success = execute_js(js_compiler_file, arguments)
    return success
