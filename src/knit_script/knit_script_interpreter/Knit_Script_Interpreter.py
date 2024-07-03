"""Interpreter processes knit-script into knitout instructions"""
from inspect import stack
from typing import Any

from knit_graphs.Knit_Graph import Knit_Graph
from knitout_interpreter.knitout_compilers.compile_knitout import compile_knitout
from knitout_interpreter.knitout_operations.Knitout_Line import Knitout_Line, Knitout_Comment_Line
from virtual_knitting_machine.Knitting_Machine import Knitting_Machine
from virtual_knitting_machine.knitting_machine_exceptions.Knitting_Machine_Exception import Knitting_Machine_Exception

from knit_script.knit_script_exceptions.Knit_Script_Exception import Knit_Script_Exception
from knit_script.knit_script_interpreter.Knit_Script_Parser import Knit_Script_Parser
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knit_script_std_library.carriers import cut_active_carriers


class Knit_Script_Interpreter:
    """
        A class to manage interpretation a knit script file with parglare
    """

    def __init__(self, debug_grammar: bool = False, debug_parser: bool = False, debug_parser_layout: bool = False,
                 context: Knit_Script_Context | None = None, starting_variables: dict[str, Any] | None = None):
        """
        Instantiate
        :param context:
        :param debug_grammar: Will provide full parglare output for grammar states
        :param debug_parser: Will provide full parglare output for parsed file shift reduce status
        :param debug_parser_layout: Will provide layout information from parser
        """
        self._parser: Knit_Script_Parser = Knit_Script_Parser(debug_grammar, debug_parser, debug_parser_layout)
        if context is None:
            self._knit_pass_context: Knit_Script_Context = Knit_Script_Context(parser=self._parser)
        else:
            self._knit_pass_context: Knit_Script_Context = context
            self._knit_pass_context.parser = self._parser
        self._add_variables(starting_variables)

    def _add_variables(self, python_variables: dict[str, Any] | None):
        if python_variables is None:
            python_variables = {}
        for key, value in python_variables.items():
            self._knit_pass_context.add_variable(key, value)

    def _reset_context(self):
        """
        Resets the context of the knit_script_interpreter to a starting state with no set variables or operations on the machine
        """
        self._knit_pass_context = Knit_Script_Context(parser=self._parser)

    def parse(self, pattern: str, pattern_is_file: bool = False) -> list:
        """
        Executes the parsing code for the parglare parser
        :param pattern: either a file or the knit script string to be parsed
        :param pattern_is_file: if true, assumes that the pattern is parsed from a file
        :return: list of statements parsed from file
        """
        return self._parser.parse(pattern, pattern_is_file)

    def write_knitout(self, pattern: str, out_file_name: str, pattern_is_file: bool = False, reset_context: bool = True,
                      **python_variables) -> tuple[list[Knitout_Line], Knit_Graph, Knitting_Machine]:
        """
        Writes pattern knitout instructions to the out file
        Parameters
        ----------
        pattern: pattern or pattern file name to turn to knitout
        out_file_name: the output file name
        pattern_is_file: true if the pattern is a file name
        :param python_variables: values from python to load into the knit script scope
        :param pattern_is_file: If true, interpret from file
        :param out_file_name: location to store knitout
        :param pattern: the pattern string or file name to interpret
        :param reset_context: If true, resets context at end of program
        """
        if pattern_is_file:
            self._knit_pass_context.ks_file = pattern
        else:
            caller_file = stack()[1].filename
            self._knit_pass_context.ks_file = caller_file
        self._add_variables(python_variables)
        self._interpret_knit_script(pattern, pattern_is_file)
        self._knit_pass_context.knitout.extend(cut_active_carriers(self._knit_pass_context.machine_state))
        knitout = self._knit_pass_context.knitout
        with open(out_file_name, "w", encoding="utf-8", newline='\n') as out:
            out.writelines([str(k) for k in knitout])
        machine_state = self._knit_pass_context.machine_state
        knitgraph = machine_state.knit_graph
        if reset_context:
            self._reset_context()
        return knitout, knitgraph, machine_state

    def _interpret_knit_script(self, pattern, pattern_is_file) -> list[Knitout_Line]:
        statements = self.parse(pattern, pattern_is_file)
        on_file = ""
        if pattern_is_file:
            on_file = f"on {pattern}"
        print(f"\n###################Start Knit Script Interpreter {on_file}###################\n")
        try:
            self._knit_pass_context.execute_statements(statements)
        except (AssertionError, Knit_Script_Exception, Knitting_Machine_Exception) as e:
            self._knit_pass_context.knitout.extend(cut_active_carriers(self._knit_pass_context.machine_state))
            if len(self._knit_pass_context.knitout) > 0:
                with open(f"error.k", "w") as out:
                    out.writelines([str(k) for k in self._knit_pass_context.knitout])
                    if isinstance(e, Knitting_Machine_Exception) or isinstance(e, Knit_Script_Exception):
                        error_comments = [Knitout_Comment_Line(e.message)]
                        out.writelines([str(ec) for ec in error_comments])
                compile_knitout(f"error.k", f"error.dat")
            raise e
        return self._knit_pass_context.knitout

    def knit_script_evaluate_expression(self, exp) -> Any:
        """
        :param exp: expression to evaluate
        :return: evaluation result
        """
        return exp.evaluate(self._knit_pass_context)
