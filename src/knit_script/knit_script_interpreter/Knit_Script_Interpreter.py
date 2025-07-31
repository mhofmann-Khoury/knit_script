"""Interpreter processes knit-script into knitout instructions"""
from __future__ import annotations
from inspect import stack
from typing import Any, cast

from knit_graphs.Knit_Graph import Knit_Graph
from knitout_interpreter.knitout_compilers.compile_knitout import compile_knitout
from knitout_interpreter.knitout_operations.Knitout_Line import Knitout_Line, Knitout_Comment_Line
from virtual_knitting_machine.Knitting_Machine import Knitting_Machine
from virtual_knitting_machine.knitting_machine_exceptions.Knitting_Machine_Exception import Knitting_Machine_Exception

from knit_script.knit_script_exceptions.Knit_Script_Exception import Knit_Script_Exception
from knit_script.knit_script_interpreter.Knit_Script_Parser import Knit_Script_Parser
from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knit_script_std_library.carriers import cut_active_carriers


class Knit_Script_Interpreter:
    """A class to manage interpretation a knit script file with parglare."""

    def __init__(self, debug_grammar: bool = False, debug_parser: bool = False, debug_parser_layout: bool = False,
                 context: Knit_Script_Context | None = None, starting_variables: dict[str, Any] | None = None):
        """Instantiate the knit script interpreter.

        Args:
            debug_grammar: Will provide full parglare output for grammar states
            debug_parser: Will provide full parglare output for parsed file shift reduce status
            debug_parser_layout: Will provide layout information from parser
            context: Knit script context to use
            starting_variables: Initial variables to load into scope
        """
        self._parser: Knit_Script_Parser = Knit_Script_Parser(debug_grammar, debug_parser, debug_parser_layout)
        if context is None:
            self._knitscript_context: Knit_Script_Context = Knit_Script_Context(parser=self._parser)
        else:
            self._knitscript_context: Knit_Script_Context = context
            self._knitscript_context.parser = self._parser
        self._add_variables(starting_variables)

    def _add_variables(self, python_variables: dict[str, Any] | None) -> None:
        """Adds Python variables to the knit script context.

        Args:
            python_variables: Dictionary of variables to add
        """
        if python_variables is None:
            python_variables = {}
        for key, value in python_variables.items():
            self._knitscript_context.add_variable(key, value)

    def _reset_context(self) -> None:
        """Resets the context of the knit_script_interpreter to a starting state.

        Resets to a starting state with no set variables or operations on the machine.
        """
        self._knitscript_context = Knit_Script_Context(parser=self._parser)

    def parse(self, pattern: str, pattern_is_file: bool = False) -> list[Any]:
        """Executes the parsing code for the parglare parser.

        Args:
            pattern: Either a file or the knit script string to be parsed
            pattern_is_file: If true, assumes that the pattern is parsed from a file

        Returns:
            List of statements parsed from file
        """
        return cast(list[Any], self._parser.parse(pattern, pattern_is_file))

    def write_knitout(self, pattern: str, out_file_name: str, pattern_is_file: bool = False, reset_context: bool = True,
                      **python_variables: dict[str, Any]) -> tuple[list[Knitout_Line], Knit_Graph, Knitting_Machine]:
        """Writes pattern knitout instructions to the out file.

        Args:
            pattern: Pattern or pattern file name to turn to knitout
            out_file_name: The output file name
            pattern_is_file: True if the pattern is a file name
            reset_context: If true, resets context at end of program
            **python_variables: Values from python to load into the knit script scope

        Returns:
            Tuple containing knitout lines, knit graph, and machine state
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
        """Interprets a knit script pattern into knitout instructions.

        Args:
            pattern: The pattern string or file to interpret
            pattern_is_file: Whether the pattern is a file

        Returns:
            List of knitout lines generated

        Raises:
            AssertionError: If assertions in the script fail
            Knit_Script_Exception: If knit script specific errors occur
            Knitting_Machine_Exception: If machine operation errors occur
        """
        statements = self.parse(pattern, pattern_is_file)
        on_file = ""
        if pattern_is_file:
            on_file = f"on {pattern}"
        print(f"\n###################Start Knit Script Interpreter {on_file}###################\n")
        try:
            self._knitscript_context.execute_statements(statements)
        except (AssertionError, Knit_Script_Exception, Knitting_Machine_Exception) as e:
            self._knitscript_context.knitout.extend(cut_active_carriers(self._knitscript_context.machine_state))
            if len(self._knitscript_context.knitout) > 0:
                with open(f"error.k", "w") as out:
                    out.writelines([str(k) for k in self._knitscript_context.knitout])
                    if isinstance(e, Knitting_Machine_Exception) or isinstance(e, Knit_Script_Exception):
                        error_comments = [Knitout_Comment_Line(e.message)]
                        out.writelines([str(ec) for ec in error_comments])
                compile_knitout(f"error.k", f"error.dat")
            raise e
        return cast(list[Knitout_Line], self._knitscript_context.knitout)

    def knit_script_evaluate_expression(self, exp: Expression) -> Any:
        """Evaluates a knit script expression.

        Args:
            exp: Expression to evaluate

        Returns:
            Evaluation result
        """
        return exp.evaluate(self._knitscript_context)
