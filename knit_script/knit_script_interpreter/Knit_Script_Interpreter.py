"""Interpreter processes knit-script into knitout instructions"""
from inspect import stack
from typing import Tuple, Any, Optional

from knit_script.knit_graphs.Knit_Graph import Knit_Graph
from knit_script.knit_script_interpreter.Knit_Script_Parser import Knit_Script_Parser
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knitout_compilers.compile_knitout import knitout_to_dat
from knit_script.knitout_interpreter.Knitout_Interpreter import Knitout_Interpreter
from knit_script.knitout_interpreter.Knitout_Optimizer import Knitout_Optimizer
from knit_script.knitout_interpreter.Knitout_Topology_Graph import Knitout_Topology_Graph
from knit_script.knitout_interpreter.knitout_structures.Knitout_Line import Knitout_Line


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

    def write_knitout(self, pattern: str, out_file_name: str, pattern_is_file: bool = False, reset_context: bool = True,
                      optimize=True, visualize_instruction_graph: bool = False) -> tuple[list[Knitout_Line], Knit_Graph]:
        """
        Writes pattern knitout instructions to the out file
        Parameters
        ----------
        pattern: pattern or pattern file name to turn to knitout
        out_file_name: the output file name
        pattern_is_file: true if the pattern is a file name
        :param visualize_instruction_graph:
        :param optimize:
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
        self._knit_pass_context.knitout.extend(self._knit_pass_context.machine_state.carrier_system.cut_all_yarns(self._knit_pass_context.machine_state))
        if optimize:
            knitout = self.optimize_knitout(f"_original_{out_file_name}", f"_organized_{out_file_name}", visualize_instruction_graph)
        else:
            knitout = self._knit_pass_context.knitout
        with open(out_file_name, "w") as out:
            out.writelines([str(k) for k in knitout])
        knitgraph = self._knit_pass_context.machine_state.knit_graph
        if reset_context:
            self._reset_context()
        return knitout, knitgraph

    def optimize_knitout(self, original_out_name: Optional[str], organized_out_name: Optional[str], visualize: bool) -> list[Knitout_Line]:
        """
        :param visualize:
        :param original_out_name:
        :param organized_out_name:
        :return: knitout instructions with optimized order
        """
        temp_knitout = ""
        for k in self._knit_pass_context.knitout:
            temp_knitout += str(k)
        if original_out_name is not None:
            with open(original_out_name, 'w') as temp:
                temp.writelines([str(k) for k in self._knit_pass_context.knitout])
        knitout_interpreter = Knitout_Interpreter()
        organized_knitout = knitout_interpreter.interpret_knitout(temp_knitout, pattern_is_file=False)
        if organized_out_name is not None:
            with open(organized_out_name, 'w') as temp:
                temp.writelines([str(k) for k in organized_knitout])
        optimizer = Knitout_Optimizer(knitout_interpreter.context)
        if visualize:
            optimizer.visualize()
        optimized_knitout = optimizer.optimize()
        return optimized_knitout

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
            self._knit_pass_context.knitout.extend(self._knit_pass_context.machine_state.carrier_system.cut_all_yarns(self._knit_pass_context.machine_state))
            with open("error.k", "w") as out:
                out.writelines([str(k) for k in self._knit_pass_context.knitout])
            knitout_to_dat(f"error.k", f"error.dat")
            raise e
            # raise Knit_Script_Error(str(e))

    def knit_script_evaluate_expression(self, exp) -> Any:
        """
        :param exp: expression to evaluate
        :return: evaluation result
        """
        return exp.evaluate(self._knit_pass_context)
