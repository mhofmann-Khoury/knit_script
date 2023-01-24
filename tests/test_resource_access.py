import os
from typing import Optional

import pkg_resources


def get_test_resource(file_name: str, sub_directory: Optional[str] = None) -> str:
    """
    :param file_name: name of resource to search for in test folder
    :param sub_directory: subdirectory of test folder to acces from
    :return: the path name
    """
    if sub_directory is None:
        sub_directory = ""
    else:
        sub_directory = f"{sub_directory}{os.sep}"
    resource = pkg_resources.resource_stream(f"tests", f"{sub_directory}{file_name}")
    name = resource.name
    return name
