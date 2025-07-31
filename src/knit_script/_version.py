"""
Version information for knitout_interpreter.

This module provides version information by reading from the installed package
metadata, ensuring a single source of truth with pyproject.toml.
"""

from importlib.metadata import version, PackageNotFoundError


try:
    # Get version from installed package metadata
    # This reads from pyproject.toml when the package is installed
    __version__ = version("knit-script")
except PackageNotFoundError:
    # Package is not installed (e.g., during development)
    # This happens when running from source without installation
    __version__ = "0.0.0+dev"

# Make version available for import
__all__ = ["__version__"]
