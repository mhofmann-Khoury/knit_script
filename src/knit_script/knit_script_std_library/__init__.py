import os


def get_ks_library_path() -> str:
    """
    Returns:
        str: The path-like string to the Knit Script Standard Library package being initiated.
    """
    return os.path.dirname(__file__)
