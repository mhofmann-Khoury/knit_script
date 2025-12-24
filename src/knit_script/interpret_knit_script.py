"""Module containing the knit_script_to_knitout function"""

from typing import Any

from knit_graphs.Knit_Graph import Knit_Graph
from virtual_knitting_machine.Knitting_Machine import Knitting_Machine

from knit_script.debugger.knitscript_debugger import Knit_Script_Debugger
from knit_script.knit_script_interpreter.Knit_Script_Interpreter import Knit_Script_Interpreter
from knit_script.knit_script_interpreter.knitscript_logging.knitscript_logger import Knit_Script_Logger, KnitScript_Error_Log, KnitScript_Warning_Log


def knit_script_to_knitout(
    pattern: str,
    out_file_name: str,
    pattern_is_filename: bool = True,
    info_logger: Knit_Script_Logger | None = None,
    warning_logger: KnitScript_Warning_Log | None = None,
    error_logger: KnitScript_Error_Log | None = None,
    debugger: Knit_Script_Debugger | None = None,
    **python_variables: Any,
) -> tuple[Knit_Graph, Knitting_Machine]:
    """Convert a knit script pattern into knitout format.

    This function serves as the main entry point for converting knit script patterns into knitout code.
    It processes the input pattern through the Knit Script Interpreter,
    which builds a knit graph representation and maintains the state of a virtual knitting machine throughout the conversion process.

    The function supports both file-based patterns and direct pattern strings, allowing for flexible input methods.
    Additional Python variables can be passed to extend the knit script execution environment.

    Args:
        pattern (str):
            The knit script pattern to process.
            This can be either:
            - A filename containing the knit script pattern (when pattern_is_filename=True)
            - A string containing the actual knit script code (when pattern_is_filename=False)
        out_file_name (str): The output file path where the generated knitout code will be written. The file should have a '.k' extension by convention.
        pattern_is_filename (bool, optional):
            If True, treats pattern as a filename to read from. Otherwise, treats pattern as the actual knit script code. Defaults expecting files for the pattern.
        debugger (Knit_Script_Debugger, optional): The optional debugger to attach to this process. Defaults to having no debugger.
        info_logger (Knit_Script_Logger, optional): The logger to attach to this context. Defaults to a standard logger which outputs only to console.
        warning_logger (KnitScript_Warning_Log, optional): The warning logger to attach to this context. Defaults to a standard warning logger which outputs only to console.
        error_logger (KnitScript_Error_Log, optional): The error logger to attach to this context. Defaults to a standard error logger which outputs only to console.
        **python_variables (Any): Additional keyword arguments that will be loaded into the knit script execution scope as Python variables. These can be referenced within the knit script pattern.

    Returns:
        Tuple[Knit_Graph, Knitting_Machine]:
            A tuple containing:
            - Knit_Graph: The constructed knit graph representing the pattern structure, including all stitches, connections, and knitting operations.
            - Knitting_Machine: The final state of the virtual knitting machine after processing the pattern, including needle positions, yarn carriers, and machine configuration.

    Raises:
        FileNotFoundError: If pattern_is_filename is True and the specified pattern file cannot be found.
    """
    interpreter = Knit_Script_Interpreter(info_logger=info_logger, warning_logger=warning_logger, error_logger=error_logger, debugger=debugger)
    _knitout, knit_graph, machine_state, _return_value = interpreter.write_knitout(pattern, out_file_name, pattern_is_filename, **python_variables)
    return knit_graph, machine_state


def knit_script_to_knitout_with_return(
    pattern: str,
    out_file_name: str,
    pattern_is_filename: bool = True,
    info_logger: Knit_Script_Logger | None = None,
    warning_logger: KnitScript_Warning_Log | None = None,
    error_logger: KnitScript_Error_Log | None = None,
    debugger: Knit_Script_Debugger | None = None,
    **python_variables: Any,
) -> tuple[Knit_Graph, Knitting_Machine, Any | None]:
    """Convert a knit script pattern into knitout format and return any return value from the execution.

    This function serves as the main entry point for converting knit script patterns into knitout code.
    It processes the input pattern through the Knit Script Interpreter,
    which builds a knit graph representation and maintains the state of a virtual knitting machine throughout the conversion process.

    The function supports both file-based patterns and direct pattern strings, allowing for flexible input methods.
    Additional Python variables can be passed to extend the knit script execution environment.

    Args:
        pattern (str):
            The knit script pattern to process.
            This can be either:
            - A filename containing the knit script pattern (when pattern_is_filename=True)
            - A string containing the actual knit script code (when pattern_is_filename=False)
        out_file_name (str): The output file path where the generated knitout code will be written. The file should have a '.k' extension by convention.
        pattern_is_filename (bool, optional):
            If True, treats pattern as a filename to read from. Otherwise, treats pattern as the actual knit script code. Defaults expecting files for the pattern.
        debugger (Knit_Script_Debugger, optional): The optional debugger to attach to this process. Defaults to having no debugger.
        info_logger (Knit_Script_Logger, optional): The logger to attach to this context. Defaults to a standard logger which outputs only to console.
        warning_logger (KnitScript_Warning_Log, optional): The warning logger to attach to this context. Defaults to a standard warning logger which outputs only to console.
        error_logger (KnitScript_Error_Log, optional): The error logger to attach to this context. Defaults to a standard error logger which outputs only to console.
        **python_variables (Any): Additional keyword arguments that will be loaded into the knit script execution scope as Python variables. These can be referenced within the knit script pattern.

    Returns:
        Tuple[Knit_Graph, Knitting_Machine, Any | None]:
            A tuple containing:
            - Knit_Graph: The constructed knit graph representing the pattern structure, including all stitches, connections, and knitting operations.
            - Knitting_Machine: The final state of the virtual knitting machine after processing the pattern, including needle positions, yarn carriers, and machine configuration.
            - Any | None: The return value from the knitscript execution.

    Raises:
        FileNotFoundError: If pattern_is_filename is True and the specified pattern file cannot be found.
    """
    interpreter = Knit_Script_Interpreter(info_logger=info_logger, warning_logger=warning_logger, error_logger=error_logger, debugger=debugger)
    _knitout, knit_graph, machine_state, return_value = interpreter.write_knitout(pattern, out_file_name, pattern_is_filename, **python_variables)
    return knit_graph, machine_state, return_value
