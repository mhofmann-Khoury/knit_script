"""Console function for processing knit_script"""
import getopt
import sys
from typing import Any

from knit_script.knit_graphs.Knit_Graph import Knit_Graph
from knit_script.knit_script_interpreter.Knit_Script_Interpreter import Knit_Script_Interpreter
from knit_script.knitout_compilers.compile_knitout import knitout_to_dat
from knit_script.knitting_machine.Machine_State import Machine_State
from knit_script.knitting_machine.machine_specification.Header_ID import Header_ID


def knit_script_to_knitout(pattern: str, out_file_name: str, pattern_is_filename: bool = True,
                           visualize_instruction_graph: bool = False, header_values: dict[Header_ID: Any] | None = None,
                           **python_variables) -> tuple[Knit_Graph, Machine_State]:
    """
    Processes a knit script pattern into knitout and a dat file for shima seiki machines and returns the resulting knit graph from the operations.

    :param header_values: Values used to set the the type of machine state
    :param visualize_instruction_graph: If true, generates a visualization of the instruction graph.
    :param pattern_is_filename: If true, the pattern is a filename.
    :param out_file_name: The output location for knitout and dat files.
    :param pattern: The knit script pattern or a file containing it.
    :param python_variables: Python variables to load into knit script scope.
    :return: The KnitGraph constructed during parsing on virtual machine
    """
    interpreter = Knit_Script_Interpreter()
    _knitout, knit_graph, machine_state = interpreter.write_knitout(pattern, out_file_name, pattern_is_filename,
                                                                    optimize=False, visualize_instruction_graph=visualize_instruction_graph, header_values = header_values,
                                                                    **python_variables)
    return knit_graph, machine_state


def knit_script_to_knitout_to_dat(pattern: str, knitout_name: str, dat_name: str | None = None, pattern_is_filename: bool = False,
                                  visualize_instruction_graph: bool = False, header_values: dict[Header_ID: Any] | None = None,
                                  **python_variables) -> tuple[Knit_Graph, Machine_State]:
    """
    Processes a knit script pattern into knitout and a dat file for shima seiki machines and returns the resulting knit graph from the operations.
    :param header_values:
    :param pattern_is_filename: If true, the pattern is a filename.
    :param dat_name: Output location for dat file.
    If none, dat file shares the name with knitout.
    :param knitout_name: The output location for knitout.
    :param pattern: The knit script pattern or a file containing it.
    :param visualize_instruction_graph: If true, generates a visualization of the instruction graph.
    :param python_variables: Python variables to load into scope.
    :return: The KnitGraph constructed during parsing on a virtual machine
    """
    interpreter = Knit_Script_Interpreter()
    _knitout, knit_graph, machine_state = interpreter.write_knitout(pattern, knitout_name, pattern_is_filename,
                                                                    optimize=False, visualize_instruction_graph=visualize_instruction_graph, header_values=header_values,
                                                                    **python_variables)
    success = knitout_to_dat(knitout_name, dat_name)
    assert success, f"Dat file could not be produced from {knitout_name}"
    return knit_graph, machine_state


def main():
    """
        Run the interpreter to generate knitout and optionally a dat file.
        The First argument is the input pattern. Either a string or a filename
        -k and --knitout specify the knitout file name. Defaults to the same name as pattern
        -d and --dat specify the dat file name. Defaults to none and no DAT file is produced
        --string specifies if the pattern is a string. Defaults to false
    """
    argv = sys.argv[1:]
    pattern_str = False
    knitout = None
    dat = None
    try:
        opts, args = getopt.getopt(argv, "k:d:",
                                   ["knitout =", "dat =", "string"])
        assert len(args) == 1, f"Expected knit script pattern but got {args}"
        pattern = args[0]
        for opt, arg in opts:
            if opt in ['-k', '--knitout']:
                knitout = arg
            elif opt in ['-d', '--dat']:
                dat = arg
            elif opt == "--string":
                pattern_str = True
        if knitout is None:
            assert not pattern_str, "Cannot make knitout file without a output name or a knit script file"
            knitout = pattern[0:pattern.index('.')] + '.k'
        if dat is not None:
            _knit_graph, _machine_state = knit_script_to_knitout_to_dat(pattern, knitout, dat, pattern_is_filename=not pattern_str)
            print(f"Generated Knitout to {knitout} and DAT to {dat}")
        else:
            _knit_graph, _machine_state = knit_script_to_knitout(pattern, knitout, pattern_is_filename=not pattern_str)
            print(f"Generated Knitout to {knitout}")

    except getopt.GetoptError as e:
        print(e)


if __name__ == "__main__":
    main()
