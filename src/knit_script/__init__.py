"""
knit_script: A comprehensive library for interpreting Knit Script files.

This package provides tools for parsing, validating, and executing knit script files used to control automatic V-Bed knitting machines.

Core Functionality:
    - knit_script_to_knitout(): Simple function to interpret knitscript programs into knitout programs.

Example:
    Basic usage - execute a knitout file:

    >>> from knit_script.interpret_knit_script import knit_script_to_knitout
    >>> knit_graph, knitting_machine = knit_script_to_knitout("pattern.ks", "pattern.k", pattern_is_filename= True)

    Advanced usage with variables from python preloaded into the knitscript interpreter:

    >>> from knit_script.interpret_knit_script import knit_script_to_knitout
    >>> width = 10
    >>> knit_graph, knitting_machine = knit_script_to_knitout("pattern.ks", "pattern.k", pattern_is_filename= True, width=width)
"""

# Import version information (single source of truth)
from ._version import __version__

# Core functionality - the main public API
from knit_script.interpret_knit_script import knit_script_to_knitout

# Define the minimal public API - only core functions
__all__ = [
    "__version__",
    "knit_script_to_knitout",  # Simple execution function for most users
]

# Package metadata
__author__ = "Megan Hofmann"
__email__ = "m.hofmann@northeastern.edu"
__license__ = "MIT"
__description__ = ("Knit Script is a domain specific programming language for writing v-bed knitting machine instructions."
                   " The language is loosely based on conventions from Python 3 but includes support for controlling a knitting machine."
                   " The code is interpreted into knitout which can then be processed into instructions for different types of knitting machines.")


# Utility functions (not in __all__ - available but not imported by star import)
def get_version() -> str:
    """Get the current version of knitout_interpreter.

    Returns:
        The version string from the package metadata.
    """
    return __version__


# Additional metadata for programmatic access
def get_package_info() -> dict[str, str]:
    """Get comprehensive package information.

    Returns:
        Dictionary containing package metadata including information
        from both the package and pyproject.toml.
    """
    return {
        "name": "knitout-interpreter",
        "version": __version__,
        "author": __author__,
        "email": __email__,
        "license": __license__,
        "homepage": "https://github.com/mhofmann-Khoury/knit_script",
        "repository": "https://github.com/mhofmann-Khoury/knit_script",
        "documentation": "https://github.com/mhofmann-Khoury/knit_script#readme",
        "bug_tracker": "https://github.com/mhofmann-Khoury/knit_script/issues",
        "pypi": "https://pypi.org/project/knit-script/",
    }
