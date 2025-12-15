"""Module resources for loading knitscript sequences from the package resources."""

from importlib import resources
from pathlib import Path


def load_test_resource(test_resource_filename: str) -> str:
    """
    Load data from a resource file in the resources folder of the current module's package.

    Args:
        test_resource_filename: Name of the resource file to load (e.g., 'resource.txt', 'config.json')

    Returns:
        str: Content of the resource file

    Raises:
        FileNotFoundError: If the resource file doesn't exist
        ImportError: If the resources package structure is invalid
    """
    # Get the current module's package name using __name__
    current_package = __name__.rsplit(".", 1)[0]  # Remove the module name, keep the package
    sequence_resources_path = resources.files(current_package).joinpath(test_resource_filename)

    if not sequence_resources_path.is_file():
        raise FileNotFoundError(f"Resource file '{test_resource_filename}' not found in {current_package}")
    return str(sequence_resources_path)


def delete_generated_file(filename: str) -> bool:
    """
    Delete a file that was generated in the current package directory.

    This function deletes files relative to where this function is defined,
    not where it's called from. Useful for cleaning up generated files.

    Args:
        filename: Name of the file to delete (e.g., 'output.dat', 'temp.txt')

    Returns:
        bool: True if file was deleted successfully, False if file didn't exist

    Raises:
        PermissionError: If the file cannot be deleted due to permissions
        OSError: If there's an error deleting the file

    Examples:
        # Delete a file in the same directory as this module
        delete_generated_file('output.dat')

        # Delete a file in a subdirectory
        delete_generated_file('temp_file.txt', 'temp')
    """
    # Get the directory where this module is located
    current_module_file = Path(__file__).parent

    # Build the full path to the file
    file_path = current_module_file / filename

    try:
        if file_path.exists() and file_path.is_file():
            file_path.unlink()  # Delete the file
            return True
        else:
            return False  # File didn't exist
    except PermissionError:
        raise PermissionError(f"Permission denied: Cannot delete '{file_path}'")
    except OSError as e:
        raise OSError(f"Error deleting file '{file_path}': {e}")
