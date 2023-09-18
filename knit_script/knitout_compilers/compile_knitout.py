"""used to run js DAT compiler"""
import platform
from importlib.resources import files
from pathlib import Path
import platform


def get_compiler_folder(folder_path: str | None = None):
    """
    :param folder_path: the folder of compilers or default location
    :return: The path or package that contains the dat compilers at the given folder or the default compiler folder
    """
    if folder_path is None:
        return files("knit_script.knitout_compilers")
    else:
        try:
            return files(folder_path)
        except Exception as e:  # todo figure out what this error is
            path = Path(folder_path)
            assert path.exists(), f"{folder_path} is not a valid directory or does not exist"
            assert path.is_dir(), f"{folder_path} is not a directory"
            return path


def get_dat_compiler(folder_path: str | None = None, dat_compiler_name: str | None = None):
    """
    :param folder_path: defaults to standard compiler package
    :param dat_compiler_name: the name of the compiler javascript file
    :return: the path to the dat compiler
    """
    if dat_compiler_name is None:
        dat_compiler_name = "knitout-to-dat.js"
    compiler_folder = get_compiler_folder(folder_path)
    dat_path = compiler_folder.joinpath(dat_compiler_name)
    assert dat_path.exists(), f"no DAT compiler named {dat_compiler_name} found at {folder_path}"
    assert dat_path.is_file()
    return dat_path


def get_kcode_compiler(folder_path: str | None = None, dat_compiler_name: str | None = None):
    """
    :param folder_path: defaults to standard compiler package
    :param dat_compiler_name: the name of the compiler javascript file
    :return: the path to the dat compiler
    """
    if dat_compiler_name is None:
        dat_compiler_name = "knitout-to-kcode.js"
    dat_path = get_compiler_folder(folder_path).joinpath(dat_compiler_name)
    assert dat_path.exists(), f"no KCODE compiler named {dat_compiler_name} found at {folder_path}"
    assert dat_path.is_file()
    return dat_path


def knitout_to_dat(knitout_file_name: str, dat_file_name: str | None = None, compiler_folder: str | None = None, compiler: str | None = None) -> bool:
    """
    Creates a dat file for the corresponding knitout
    :param compiler: the name of the compiler
    :param compiler_folder: the folder holding the compilers
    :param knitout_file_name:  the filename of the knitout to compile
    :param dat_file_name:  the dat filename to compile to. Defaults to the same as knitout
    """
    js_compiler_file = get_dat_compiler(compiler_folder, compiler)
    print(f"\n################Converting {knitout_file_name} to DAT file {dat_file_name} ########\n")
    if platform.system() == "Windows":
        # Run Node.js and return the exit code.
        from knit_script.knitout_compilers.run_js_dat_compilers_windows import run_js_compiler_windows
        return run_js_compiler_windows(dat_file_name, js_compiler_file, knitout_file_name)
    else:
        from knit_script.knitout_compilers.run_js_dat_compilers_unix import run_js_compiler_unix
        return run_js_compiler_unix(dat_file_name, js_compiler_file, knitout_file_name)

