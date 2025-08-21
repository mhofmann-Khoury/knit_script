"""Function for processing knit_script into knitout code.

This module provides functionality to convert knit script patterns into knitout format, which is used for controlling knitting machines.
The conversion process involves parsing the knit script, building a knit graph representation, and generating the corresponding knitout instructions.

Example:
    Basic usage - execute a knitout file:

    >>> from knit_script.interpret_knit_script import knit_script_to_knitout
    >>> knitgraph, knitting_machine = knit_script_to_knitout("pattern.ks", "pattern.k", pattern_is_filename= True)

    Advanced usage with variables from python preloaded into the knitscript interpreter:

    >>> from knit_script.interpret_knit_script import knit_script_to_knitout
    >>> width = 10
    >>> knitgraph, knitting_machine = knit_script_to_knitout("pattern.ks", "pattern.k", pattern_is_filename= True, width=width)

Attributes:
    This module does not define any module-level attributes.
"""
from typing import Any, Tuple

from knit_graphs.Knit_Graph import Knit_Graph
from virtual_knitting_machine.Knitting_Machine import Knitting_Machine

from knit_script.knit_script_interpreter.Knit_Script_Interpreter import (
    Knit_Script_Interpreter,
)


def knit_script_to_knitout( pattern: str,  out_file_name: str,  pattern_is_filename: bool = True,  **python_variables: Any) -> Tuple[Knit_Graph, Knitting_Machine]:
    """Convert a knit script pattern into knitout format.

    This function serves as the main entry point for converting knit script patterns into knitout code.
    It processes the input pattern through the Knit Script Interpreter,
    which builds a knit graph representation and maintains the state of a virtual knitting machine throughout the conversion process.

    The function supports both file-based patterns and direct pattern strings,
    allowing for flexible input methods. Additional Python variables can be passed to extend the knit script execution environment.

    Args:
        pattern (str): The knit script pattern to process. This can be either:
            - A filename containing the knit script pattern (when pattern_is_filename=True)
            - A string containing the actual knit script code (when pattern_is_filename=False)
        out_file_name (str): The output file path where the generated knitout code  will be written. The file should have a '.k' extension by convention.
        pattern_is_filename (bool, optional): Determines how to interpret the pattern parameter. If True, treats pattern as a filename to read from.
            If False, treats pattern as the actual knit script code. Defaults to True.
        **python_variables (Any): Additional keyword arguments that will be loaded into the knit script execution scope as Python variables. These can be referenced within the knit script pattern.

    Returns:
        Tuple[Knit_Graph, Knitting_Machine]: A tuple containing:
            - Knit_Graph: The constructed knit graph representing the pattern structure, including all stitches, connections, and knitting operations.
            - Knitting_Machine: The final state of the virtual knitting machine after processing the pattern, including needle positions, yarn carriers, and machine configuration.

    Raises:
        FileNotFoundError: If pattern_is_filename is True and the specified pattern file cannot be found.
        ValueError: If the pattern contains invalid knit script syntax or operations.
        TypeError: If the provided arguments are of incorrect types.

    Example:
        Basic usage - execute a knitout file:

        >>> from knit_script.interpret_knit_script import knit_script_to_knitout
        >>> knitgraph, knitting_machine = knit_script_to_knitout("pattern.ks", "pattern.k", pattern_is_filename= True)

        Advanced usage with variables from python preloaded into the knitscript interpreter:

        >>> from knit_script.interpret_knit_script import knit_script_to_knitout
        >>> width = 10
        >>> knitgraph, knitting_machine = knit_script_to_knitout("pattern.ks", "pattern.k", pattern_is_filename= True, width=width)

    Note:
        The function creates intermediate representations and machine states that can be used for further analysis or debugging of the knitting pattern.
        The knitout file is automatically written during the conversion process.

    See Also:
        Knit_Script_Interpreter: The underlying interpreter that performs the conversion.
        Knit_Graph: The graph representation of knitting patterns.
        Knitting_Machine: The virtual machine state representation.
    """
    interpreter = Knit_Script_Interpreter()
    _knitout, knit_graph, machine_state = interpreter.write_knitout(
        pattern, out_file_name, pattern_is_filename, **python_variables
    )
    return knit_graph, machine_state
