from typing import Any

from knit_graphs.Knit_Graph import Knit_Graph
from knitout_interpreter.debugger.knitout_debugger import Knitout_Debugger
from knitout_interpreter.knitout_operations.Header_Line import Knitout_Header_Line
from knitout_interpreter.knitout_operations.Knitout_Line import Knitout_Line
from knitout_interpreter.run_knitout import run_knitout
from resources.test_loggers import get_test_error_logger, get_test_info_logger, get_test_warning_logger
from virtual_knitting_machine.Knitting_Machine import Knitting_Machine

from knit_script.debugger.knitscript_debugger import Knit_Script_Debugger
from knit_script.interpret_knit_script import knit_script_to_knitout, knit_script_to_knitout_with_return
from knit_script.knit_script_interpreter.knitscript_logging.knitscript_logger import Knit_Script_Logger, KnitScript_Error_Log, KnitScript_Warning_Log


def interpret_test_ks(
    ks_pattern: str,
    out_file_name: str = "test.k",
    pattern_is_filename: bool = False,
    ks_debugger: Knit_Script_Debugger | None = None,
    info_logger: Knit_Script_Logger | None = None,
    warning_logger: KnitScript_Warning_Log | None = None,
    error_logger: KnitScript_Error_Log | None = None,
    print_k_lines: bool = False,
    execute_knitout: bool = True,
    ko_debugger: Knitout_Debugger | None = None,
    **python_variables: Any,
) -> tuple[list[Knitout_Line], Knit_Graph, Knitting_Machine]:
    """
    Process the given knit script pattern and printout the resulting knitout file.
    Args:
        ks_pattern: The knitscript pattern in a string or the filename of the knitscript pattern.
        out_file_name: The name of the knitout file to generate for this test.
        pattern_is_filename: If true, look for the pattern in a file. Otherwise, processes the pattern as a string.
        ks_debugger: The optional knitscript debugger to attach to this test process.
        info_logger (Knit_Script_Logger, optional): The logger to attach to this context. Defaults to a standard logger which outputs only to console.
        warning_logger (KnitScript_Warning_Log, optional): The warning logger to attach to this context. Defaults to a standard warning logger which outputs only to console.
        error_logger (KnitScript_Error_Log, optional): The error logger to attach to this context. Defaults to a standard error logger which outputs only to console.
        print_k_lines: If True, prints out the resulting knitout for review.
        execute_knitout: If True, executes the resulting knitout and returns the parsed knitout line objects.
        ko_debugger: The optional knitout debugger to attach to the knitout executer process
        **python_variables [Any]: The keyword variable pairs of python variables to initiate the knitscript interpreter with.

    Returns: Tuple:
        - List of Knitout_Lines that make up the resulting knitout file. This will be empty if the knitout was not executed.
        - The Knitgraph produced by processing the given knitscript pattern.
        - The Knitting Machine after processing the given knitscript pattern.

    """
    if info_logger is None:
        info_logger = get_test_info_logger()
    if warning_logger is None:
        warning_logger = get_test_warning_logger()
    if error_logger is None:
        error_logger = get_test_error_logger()
    knit_graph, machine_state = knit_script_to_knitout(
        ks_pattern, out_file_name, pattern_is_filename=pattern_is_filename, debugger=ks_debugger, info_logger=info_logger, warning_logger=warning_logger, error_logger=error_logger, **python_variables
    )
    if print_k_lines:
        with open(out_file_name, "r") as f:
            lines = f.readlines()
            for line in lines:
                print(line)
    if execute_knitout:
        klines, machine_state, knit_graph = run_knitout(out_file_name, debugger=ko_debugger)
        return klines, knit_graph, machine_state
    else:
        return [], knit_graph, machine_state


def interpret_test_ks_with_return(
    ks_pattern: str,
    out_file_name: str = "test.k",
    pattern_is_filename: bool = False,
    ks_debugger: Knit_Script_Debugger | None = None,
    info_logger: Knit_Script_Logger | None = None,
    warning_logger: KnitScript_Warning_Log | None = None,
    error_logger: KnitScript_Error_Log | None = None,
    print_k_lines: bool = False,
    execute_knitout: bool = True,
    ko_debugger: Knitout_Debugger | None = None,
    **python_variables: Any,
) -> tuple[list[Knitout_Line], Knit_Graph, Knitting_Machine, Any | None]:
    """
    Process the given knit script pattern and printout the resulting knitout file.
    Args:
        ks_pattern: The knitscript pattern in a string or the filename of the knitscript pattern.
        out_file_name: The name of the knitout file to generate for this test.
        pattern_is_filename: If true, look for the pattern in a file. Otherwise, processes the pattern as a string.
        ks_debugger: The optional knitscript debugger to attach to this test process.
        info_logger (Knit_Script_Logger, optional): The logger to attach to this context. Defaults to a standard logger which outputs only to console.
        warning_logger (KnitScript_Warning_Log, optional): The warning logger to attach to this context. Defaults to a standard warning logger which outputs only to console.
        error_logger (KnitScript_Error_Log, optional): The error logger to attach to this context. Defaults to a standard error logger which outputs only to console.
        print_k_lines: If True, prints out the resulting knitout for review.
        execute_knitout: If True, executes the resulting knitout and returns the parsed knitout line objects.
        ko_debugger: The optional knitout debugger to attach to the knitout executer process
        **python_variables [Any]: The keyword variable pairs of python variables to initiate the knitscript interpreter with.

    Returns: Tuple:
        - List of Knitout_Lines that make up the resulting knitout file. This will be empty if the knitout was not executed.
        - The Knitgraph produced by processing the given knitscript pattern.
        - The Knitting Machine after processing the given knitscript pattern.

    """
    if info_logger is None:
        info_logger = get_test_info_logger()
    if warning_logger is None:
        warning_logger = get_test_warning_logger()
    if error_logger is None:
        error_logger = get_test_error_logger()
    knit_graph, machine_state, return_val = knit_script_to_knitout_with_return(
        ks_pattern, out_file_name, pattern_is_filename=pattern_is_filename, debugger=ks_debugger, info_logger=info_logger, warning_logger=warning_logger, error_logger=error_logger, **python_variables
    )
    if print_k_lines:
        with open(out_file_name, "r") as f:
            lines = f.readlines()
            for line in lines:
                print(line)
    if execute_knitout:
        klines, machine_state, knit_graph = run_knitout(out_file_name, debugger=ko_debugger)
        return klines, knit_graph, machine_state, return_val
    else:
        return [], knit_graph, machine_state, return_val


def count_lines(klines: list[Knitout_Line], exclude_types=None, include_types: set[type] | None = None) -> int:
    """

    Args:
        klines: The list of Knitout_Line objects to count.
        exclude_types: The set of knitout line types to exclude from the count. (E.g., skip count of header lines)
        include_types: The set of knitout line types to include in the count.
            If there are no inclusion types, all knitout lines are included.

    Returns:
        The count of knitout lines that match the given inclusion and exclusion types.
    """
    if exclude_types is None:
        exclude_types = {Knitout_Header_Line}
    if include_types is None:
        include_types = set()
    if len(exclude_types) == len(include_types) == 0:
        return len(klines)

    def _included(line: Knitout_Line) -> bool:
        if len(include_types) == 0:
            return True
        else:
            return type(line) in include_types

    def _excluded(line: Knitout_Line) -> bool:
        return type(line) in exclude_types

    return len(set(k for k in klines if _included(k) and not _excluded(k)))
