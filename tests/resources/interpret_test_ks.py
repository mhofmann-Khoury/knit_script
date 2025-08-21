from typing import Any

from knit_graphs.Knit_Graph import Knit_Graph
from knitout_interpreter.knitout_operations.Header_Line import Knitout_Header_Line
from knitout_interpreter.knitout_operations.Knitout_Line import Knitout_Line
from knitout_interpreter.run_knitout import run_knitout
from virtual_knitting_machine.Knitting_Machine import Knitting_Machine

from knit_script.interpret_knit_script import knit_script_to_knitout


def interpret_test_ks(ks_pattern: str, out_file_name: str = 'test.k', pattern_is_filename: bool = False,
                      print_k_lines: bool = True, execute_knitout: bool = True,
                      **python_variables: dict[str: Any]) -> tuple[list[Knitout_Line], Knit_Graph, Knitting_Machine]:
    """
    Process the given knit script pattern and printout the resulting knitout file.
    Args:
        execute_knitout: If True, executes the resulting knitout and returns the parsed knitout line objects.
        print_k_lines: If True, prints out the resulting knitout for review.
        ks_pattern: The knitscript pattern in a string or the filename of the knitscript pattern.
        out_file_name: The name of the knitout file to generate for this test.
        pattern_is_filename: If true, look for the pattern in a file. Otherwise, processes the pattern as a string.
        **python_variables: The keyword variable pairs of python variables to initiate the knitscript interpreter with.

    Returns: Tuple:
        - List of Knitout_Lines that make up the resulting knitout file. This will be empty if the knitout was not executed.
        - The Knitgraph produced by processing the given knitscript pattern.
        - The Knitting Machine after processing the given knitscript pattern.

    """
    knit_graph, machine_state = knit_script_to_knitout(ks_pattern, out_file_name, pattern_is_filename=pattern_is_filename, **python_variables)
    if print_k_lines:
        with open(out_file_name, 'r') as f:
            lines = f.readlines()
            for line in lines:
                print(line)
    if execute_knitout:
        klines, machine_state, knit_graph = run_knitout(out_file_name)
        return klines, knit_graph, machine_state
    else:
        return [], knit_graph, machine_state


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
