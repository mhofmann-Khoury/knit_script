"""Interpreter processes knit script into knitout instructions"""
from inspect import stack
from typing import List, Tuple, Any, Optional

from knit_script.knit_graphs.Knit_Graph import Knit_Graph
from knit_script.knit_script_interpreter.Knit_Script_Parser import Knit_Script_Parser
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knit_script_interpreter.knit_script_errors.Knit_Script_Error import Knit_Script_Error


class Knit_Script_Interpreter:
    """
        A class to manage parsing a knit script file with parglare
    """

    def __init__(self, debug_grammar: bool = False, debug_parser: bool = False, debug_parser_layout: bool = False,
                 context: Optional[Knit_Script_Context] = None):
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

    def _reset_context(self):
        """
        Resets the context of the knit_script_interpreter to a starting state with no set variables or operations on the machine
        """
        header = self._knit_pass_context.header
        self._knit_pass_context = Knit_Script_Context(parser=self._parser)
        self._knit_pass_context.header = header  # resets machine state as well

    def parse(self, pattern: str, pattern_is_file: bool = False) -> Tuple[list, list]:
        """
        Executes the parsing code for the parglare parser
        :param pattern: either a file or the knit script  string to be parsed
        :param pattern_is_file: if true, assumes that the pattern is parsed from a file
        :return:
        """
        return self._parser.parse(pattern, pattern_is_file)

    def write_knitout(self, pattern: str, out_file_name: str, pattern_is_file: bool = False, reset_context: bool = True) -> Tuple[List[str], Knit_Graph]:
        """
        Writes pattern knitout instructions to the out file
        Parameters
        ----------
        pattern: pattern or pattern file name to turn to knitout
        out_file_name: the output file name
        pattern_is_file: true if the pattern is a file name
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
        self._interpret_knit_script(pattern, pattern_is_file)
        self._knit_pass_context.knitout.extend(self._knit_pass_context.machine_state.yarn_manager.cut_all_yarns())
        with open(out_file_name, "w") as out:
            out.writelines(self._knit_pass_context.knitout)
        knitgraph = self._knit_pass_context.machine_state.knit_graph
        knitout = self._knit_pass_context.knitout
        if reset_context:
            self._reset_context()
        return knitout, knitgraph

    def _interpret_knit_script(self, pattern, pattern_is_file):
        header, statements = self.parse(pattern, pattern_is_file)
        on_file = ""
        if pattern_is_file:
            on_file = f"on {pattern}"
        print(f"\n###################Start Knit Script Interpreter {on_file}###################\n")
        try:
            self._knit_pass_context.execute_header(header)
            self._knit_pass_context.execute_statements(statements)
        except AssertionError as e:
            raise Knit_Script_Error(str(e))

    def knit_script_evaluate_expression(self, exp) -> Any:
        """
        :param exp: expression to evaluate
        :return: evaluation result
        """
        return exp.evaluate(self._knit_pass_context)
