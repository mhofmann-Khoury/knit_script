"""Console function for processing knit_script"""
from typing import Any

from knit_graphs.Knit_Graph import Knit_Graph
from knitout_interpreter.knitout_compilers.compile_knitout import compile_knitout
from knitout_interpreter.knitout_operations.Header_Line import Knitout_Header_Line_Type
from virtual_knitting_machine.Knitting_Machine import Knitting_Machine

from knit_script.knit_script_interpreter.Knit_Script_Interpreter import Knit_Script_Interpreter


def knit_script_to_knitout(pattern: str, out_file_name: str, pattern_is_filename: bool = True,
                           visualize_instruction_graph: bool = False, header_values: dict[Knitout_Header_Line_Type: Any] | None = None,
                           **python_variables) -> tuple[Knit_Graph, Knitting_Machine]:
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
                                                                    optimize=False, visualize_instruction_graph=visualize_instruction_graph, header_values=header_values,
                                                                    **python_variables)
    return knit_graph, machine_state


def knit_script_to_knitout_to_dat(pattern: str, knitout_name: str, dat_name: str | None = None, pattern_is_filename: bool = False,
                                  visualize_instruction_graph: bool = False, header_values: dict[Knitout_Header_Line_Type: Any] | None = None,
                                  **python_variables) -> tuple[Knit_Graph, Knitting_Machine]:
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
    success = compile_knitout(knitout_name, dat_name)
    assert success, f"Dat file could not be produced from {knitout_name}"
    return knit_graph, machine_state
