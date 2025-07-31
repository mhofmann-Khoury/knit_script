"""Function for processing knit_script into knitout code"""
from typing import Any

from knit_graphs.Knit_Graph import Knit_Graph
from virtual_knitting_machine.Knitting_Machine import Knitting_Machine

from knit_script.knit_script_interpreter.Knit_Script_Interpreter import Knit_Script_Interpreter


def knit_script_to_knitout(pattern: str, out_file_name: str, pattern_is_filename: bool = True,
                           **python_variables: dict[str: Any]) -> tuple[Knit_Graph, Knitting_Machine]:
    """Processes a knit script pattern into knitout file.

    This function takes a knit script pattern and converts it to knitout format.
    It returns the resulting knitgraph from the operations and the final machine state.

    Args:
        pattern: The knit script pattern string or filename containing the pattern.
        out_file_name: The output location for knitout file.
        pattern_is_filename: If True, the knitscript interpreter will look for a file containing the pattern.
            If False, the pattern string is assumed to be knitscript code.
            Defaults to True.
        **python_variables: Additional Python variables to load into knit script scope.

    Returns:
        A tuple containing:
            - Knit_Graph: The knit graph constructed during parsing.
            - Knitting_Machine: The virtual machine state after processing.
    """
    interpreter = Knit_Script_Interpreter()
    _knitout, knit_graph, machine_state = interpreter.write_knitout( pattern, out_file_name, pattern_is_filename,  **python_variables)
    return knit_graph, machine_state
