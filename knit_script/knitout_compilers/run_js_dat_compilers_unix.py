"""Isolated code for running DAT compiler on unix"""
import subprocess


def run_js_compiler_unix(dat_file_name, js_compiler_file, knitout_file_name):
    """

    :param dat_file_name:
    :param js_compiler_file:
    :param knitout_file_name:
    :return: True if DAT compiled successfully
    """
    node_command = ["node", str(js_compiler_file), knitout_file_name, dat_file_name]
    node_process = subprocess.run(node_command, capture_output=True, text=True)
    if node_process.stdout is not None:
        print(f"DAT Compiler Output:\n\t{node_process.stdout}")
    if node_process.stderr is not None:
        print(f"DAT Compiler Error:\n\t{node_process.stderr}")
    if node_process.stderr is not None and node_process.stderr.strip() != "":
        print(node_process.stderr)
        return False
    else:
        return True
