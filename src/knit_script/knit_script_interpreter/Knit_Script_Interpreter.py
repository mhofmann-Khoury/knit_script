"""Interpreter processes knit-script into knitout instructions.

This module provides the main interpreter class for converting knit script patterns into knitout instructions.
The interpreter handles parsing, context management, and execution of knit script code while maintaining machine state and generating the corresponding knitout output.

The interpreter supports debugging capabilities, variable injection, and error handling for robust knit script processing.

Attributes:
    This module defines the Knit_Script_Interpreter class and supporting functionality.
"""
from __future__ import annotations

from inspect import stack
from typing import Any, cast

from knit_graphs.Knit_Graph import Knit_Graph
from knitout_interpreter.knitout_operations.Knitout_Line import Knitout_Line
from virtual_knitting_machine.Knitting_Machine import Knitting_Machine

from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knit_script_interpreter.Knit_Script_Parser import Knit_Script_Parser
from knit_script.knit_script_std_library.carriers import cut_active_carriers


class Knit_Script_Interpreter:
    """A class to manage interpretation of knit script files with parglare parser.

    The Knit_Script_Interpreter serves as the main entry point for processing knit script patterns.
    It manages the parsing process, maintains execution context, handles variable injection, and coordinates the generation of knitout instructions.

    The interpreter provides comprehensive error handling and debugging capabilities, making it suitable for both development and production use cases.

    Attributes:
        _parser (Knit_Script_Parser): The underlying parser for knit script syntax.
        _knitscript_context (Knit_Script_Context): The execution context containing variables, machine state, and other runtime information.
    """

    def __init__(self, debug_grammar: bool = False, debug_parser: bool = False, debug_parser_layout: bool = False,
                 context: None | Knit_Script_Context = None, starting_variables: None | dict[str, Any] = None) -> None:
        """Initialize the knit script interpreter.

        Creates a new interpreter instance with the specified configuration options.
        The interpreter can be customized with debugging flags, a custom execution context, and initial variables.

        Args:
            debug_grammar (bool, optional): If True, provides full parglare output for grammar states during parsing. Useful for debugging grammar issues. Defaults to False.
            debug_parser (bool, optional): If True, provides full parglare output for parsed file shift-reduce status. Useful for debugging parsing issues. Defaults to False.
            debug_parser_layout (bool, optional): If True, provides layout information from the parser. Useful for debugging whitespace and indentation issues. Defaults to False.
            context (Knit_Script_Context, optional): A pre-configured knit script context to use instead of creating a new one. If None, a new context will be created. Defaults to None.
            starting_variables (dict[str, Any], optional): Initial variables to load into the knit script execution scope.
                These variables will be  available for use within knit script patterns. Defaults to None.

        Note:
            Debug flags should only be enabled during development as they produce verbose output that can impact performance.
        """
        self._parser: Knit_Script_Parser = Knit_Script_Parser(debug_grammar, debug_parser, debug_parser_layout)

        if context is None:
            self._knitscript_context: Knit_Script_Context = Knit_Script_Context(parser=self._parser)
        else:
            self._knitscript_context: Knit_Script_Context = context
            self._knitscript_context.parser = self._parser

        self._add_variables(starting_variables)

    def _add_variables(self, python_variables: None | dict[str, Any]) -> None:
        """Add Python variables to the knit script execution context.

        This method injects Python variables into the knit script context, making them available for use within knit script patterns.
        Variables are added to the current scope and can be referenced by name in the script.

        Args:
            python_variables (dict[str, Any], optional): Dictionary mapping variable  names to their values. If None or empty, no variables are added.

        Note:
            Variable names must be valid Python identifiers to be accessible  within knit script code.
        """
        if python_variables is None:
            python_variables = {}
        for key, value in python_variables.items():
            self._knitscript_context.add_variable(key, value)

    def _reset_context(self) -> None:
        """Reset the interpreter context to its initial state.

        This method resets the knit script context to a clean starting state, clearing all variables, machine operations, and execution history. The parser reference is preserved.

        Note:
            This operation cannot be undone. All context state will be lost.
        """
        self._knitscript_context = Knit_Script_Context(parser=self._parser)

    def parse(self, pattern: str, pattern_is_file: bool = False) -> list[Any]:
        """Execute the parsing process for the given knit script pattern.

        This method processes the input pattern through the parglare parser,
        converting the knit script syntax into an abstract syntax tree (AST) representation that can be executed by the interpreter.

        Args:
            pattern (str): Either a knit script string to be parsed directly,  or a filename containing the knit script code to be parsed.
            pattern_is_file (bool, optional): If True, treats the pattern parameter as a filename and reads the script from that file.
                If False, treats pattern as the actual knit script code. Defaults to False.

        Returns:
            list[Any]: A list of parsed statements representing the abstract syntax tree of the knit script. Each element corresponds to a top-level statement or expression in the script.

        Raises:
            FileNotFoundError: If pattern_is_file is True and the specified file cannot be found or accessed.
            ParseError: If the knit script contains syntax errors that prevent successful parsing.
        """
        return cast(list[Any], self._parser.parse(pattern, pattern_is_file))

    def write_knitout(self, pattern: str, out_file_name: str, pattern_is_file: bool = False, reset_context: bool = True,
                      **python_variables: dict[str, Any]) -> tuple[list[Knitout_Line], Knit_Graph, Knitting_Machine]:
        """Write pattern knitout instructions to the specified output file.

        This is the main method for converting knit script patterns into knitout format.
        It handles the complete workflow: parsing, interpretation, execution, and file output generation.

        The method processes the input pattern, executes all knit script instructions, generates the corresponding knitout commands, and writes them to the specified output file.
        It also returns the internal representations for further analysis.

        Args:
            pattern (str): The knit script pattern to convert. Can be either:
                - A filename containing knit script code (when pattern_is_file=True)
                - A string containing the actual knit script code (when pattern_is_file=False)
            out_file_name (str): The path where the generated knitout file will be written. Convention is to use '.k' extension for knitout files.
            pattern_is_file (bool, optional): Determines how to interpret the pattern  parameter. If True, reads from the specified file.
                If False, treats pattern as direct script code. Defaults to False.
            reset_context (bool, optional): If True, resets the interpreter context  to its initial state after processing.
                If False, preserves the context state for subsequent operations. Defaults to True.
            **python_variables (dict[str, Any]): Additional keyword arguments that will be injected into the knit script execution scope as variables.

        Returns:
            tuple[list[Knitout_Line], Knit_Graph, Knitting_Machine]: A tuple containing:
                - list[Knitout_Line]: The complete sequence of knitout instructions generated from the pattern.
                - Knit_Graph: The knit graph representation showing the structure and relationships of all stitches in the pattern.
                - Knitting_Machine: The final state of the virtual knitting machine after executing all pattern instructions.

        Raises:
            FileNotFoundError: If pattern_is_file is True and the pattern file cannot be found.
            Knit_Script_Exception: If the knit script contains semantic errors or invalid operations.
            Knitting_Machine_Exception: If machine operations fail due to invalid states or impossible operations.
            AssertionError: If assertions within the knit script fail.

        Note:
            If an error occurs during processing, an error.k file will be generated containing any knitout instructions that were successfully processed before the error, along with error comments.
        """
        if pattern_is_file:
            self._knitscript_context.ks_file = pattern
        else:
            caller_file = stack()[1].filename
            self._knitscript_context.ks_file = caller_file

        self._add_variables(python_variables)
        self._interpret_knit_script(pattern, pattern_is_file)
        self._knitscript_context.knitout.extend(cut_active_carriers(self._knitscript_context.machine_state))

        knitout = self._knitscript_context.knitout
        with open(out_file_name, "w", encoding="utf-8", newline='\n') as out:
            out.writelines([str(k) for k in knitout])

        machine_state = self._knitscript_context.machine_state
        knitgraph = machine_state.knit_graph

        if reset_context:
            self._reset_context()

        return knitout, knitgraph, machine_state

    def _interpret_knit_script(self, pattern: str, pattern_is_file: bool) -> list[Knitout_Line]:
        """Interpret a knit script pattern into knitout instructions.

        This internal method handles the core interpretation logic, including parsing the pattern, executing statements, and handling errors.
        It provides comprehensive error handling and generates debug output.

        Args:
            pattern (str): The pattern string or filename to interpret.
            pattern_is_file (bool): Whether the pattern parameter is a filename.

        Returns:
            list[Knitout_Line]: The generated knitout instructions.

        Note:
            This method includes comprehensive error handling.
            If an error occurs, it will attempt to save any successfully generated knitout instructions to an error.k file before re-raising the exception.
        """
        statements = self.parse(pattern, pattern_is_file)
        on_file = ""
        if pattern_is_file:
            on_file = f" on {pattern}"
        print(f"\n###################Start Knit Script Interpreter{on_file}###################\n")
        self._knitscript_context.execute_statements(statements)
        return cast(list[Knitout_Line], self._knitscript_context.knitout)

    def knit_script_evaluate_expression(self, exp: Expression) -> Any:
        """Evaluate a knit script expression within the current context.

        This method evaluates knit script expressions using the current interpreter context, including all available variables and state.
        It provides a way to evaluate expressions outside the normal script execution flow.

        Args:
            exp (Expression): The knit script expression object to evaluate. This should be a properly parsed expression from the knit script abstract syntax tree.

        Returns:
            Any: The result of evaluating the expression. The type depends on the expression being evaluated (e.g., int, str, list, etc.).
        """
        return exp.evaluate(self._knitscript_context)
