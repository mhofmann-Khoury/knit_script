"""Isolated code for running DAT compiler on windows"""


def run_js_compiler_unix(dat_file_name, js_compiler_file, knitout_file_name):
    """

    :param dat_file_name:
    :param js_compiler_file:
    :param knitout_file_name:
    :return: True if DAT compiled successfully
    """
    raise NotImplementedError("Needs Unix JS run commands")
    # node_process = node.run([js_compiler_file, knitout_file_name, dat_file_name])
    # if node_process.stdout is not None:
    #     print(f"DAT Compiler Output:\n\t{node_process.stdout}")
    # if node_process.stderr is not None:
    #     print(f"DAT Compiler Error:\n\t{node_process.stderr}")
    # return node_process.stderr is None
