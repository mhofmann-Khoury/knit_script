"""Interpreter processes knit-script into knitout instructions"""
import os
from inspect import stack
from typing import Any

from knit_script.Knit_Errors.Knit_Script_Error import Knit_Script_Error
from knit_script.Knit_Errors.Knitout_Error import Knitout_Error
from knit_script.knit_graphs.Knit_Graph import Knit_Graph
from knit_script.knit_script_interpreter.Knit_Script_Parser import Knit_Script_Parser
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knitout_compilers.compile_knitout import knitout_to_dat
from knit_script.knitout_interpreter.Knitout_Interpreter import Knitout_Interpreter
from knit_script.knitout_interpreter.Knitout_Optimizer import Knitout_Optimizer
from knit_script.knitout_interpreter.knitout_structures.Knitout_Line import Knitout_Line, Comment_Line
from knit_script.knitting_machine.Machine_State import Machine_State
from knit_script.knitting_machine.machine_specification.Header_ID import Header_ID


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

    def set_header_value(self, header_id: Header_ID, value):
        """
        Set the value for the given header id
        :param header_id:
        :param value:
        """
        self._knit_pass_context.header.set_value(header_id, value)

    def get_header_value(self, header_id: Header_ID):
        """
        :param header_id:
        :return: the value keyed by the header id
        """
        return self._knit_pass_context.header.get_value(header_id)

    def _reset_context(self):
        """
        Resets the context of the knit_script_interpreter to a starting state with no set variables or operations on the machine
        """
        header = self._knit_pass_context.header
        self._knit_pass_context = Knit_Script_Context(parser=self._parser)
        self._knit_pass_context.header = header  # resets machine state as well

    def parse(self, pattern: str, pattern_is_file: bool = False) -> list:
        """
        Executes the parsing code for the parglare parser
        :param pattern: either a file or the knit script string to be parsed
        :param pattern_is_file: if true, assumes that the pattern is parsed from a file
        :return: list of statements parsed from file
        """
        return self._parser.parse(pattern, pattern_is_file)

    def write_knitout(self, pattern: str, out_file_name: str, pattern_is_file: bool = False, reset_context: bool = True, optimize=True, visualize_instruction_graph: bool = False,
                      clean_optimization: bool = True, header_values: dict[Header_ID: Any] | None = None, **python_variables) -> tuple[list[Knitout_Line], Knit_Graph, Machine_State]:
        """
        Writes pattern knitout instructions to the out file
        Parameters
        ----------
        pattern: pattern or pattern file name to turn to knitout
        out_file_name: the output file name
        pattern_is_file: true if the pattern is a file name
        :param header_values: Values to update the ehader too
        :param clean_optimization: If true, deletes intermediate files
        :param python_variables: values from python to load into the knit script scope
        :param visualize_instruction_graph: If true, generates a visualization of the graph written
        :param optimize:If true, optimizes the knitout output
        :param pattern_is_file: If true, interpret from file
        :param out_file_name: location to store knitout
        :param pattern: the pattern string or file name to interpret
        :param reset_context: If true, resets context at end of program
        """
        if header_values is not None:
            for hid, value in header_values.items():
                self.set_header_value(hid, value)
            self._reset_context()  # updates machine state all at once
        if pattern_is_file:
            self._knit_pass_context.ks_file = pattern
        else:
            caller_file = stack()[1].filename
            self._knit_pass_context.ks_file = caller_file
        self._add_variables(python_variables)
        self._interpret_knit_script(pattern, pattern_is_file)
        self._knit_pass_context.knitout.extend(self._knit_pass_context.machine_state.carrier_system.cut_all_yarns(self._knit_pass_context.machine_state))
        if optimize:
            try:
                knitout = self.optimize_knitout(f"_original_{out_file_name}", f"_organized_{out_file_name}",
                                                visualize=visualize_instruction_graph, clean_original=clean_optimization, clean_organized=clean_optimization)
            except Exception as e:
                raise e
                # knitout = self._knit_pass_context.knitout
        else:
            knitout = self._knit_pass_context.knitout
        with open(out_file_name, "w", encoding="utf-8", newline='\n') as out:
            out.writelines([str(k) for k in knitout])
        machine_state = self._knit_pass_context.machine_state
        knitgraph = machine_state.knit_graph
        if reset_context:
            self._reset_context()
        return knitout, knitgraph, machine_state

    def optimize_knitout(self, original_out_name: str | None, organized_out_name: str | None, visualize: bool = False, clean_original: bool = True, clean_organized: bool = True) -> list[Knitout_Line]:
        """
        :param clean_organized:
        :param clean_original:
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
        optimized_knitout = optimizer.optimize(visualize=visualize)
        if clean_original:
            os.remove(original_out_name)
        if clean_organized:
            os.remove(organized_out_name)
        return optimized_knitout

    def _interpret_knit_script(self, pattern, pattern_is_file) -> list[Knitout_Line]:
        statements = self.parse(pattern, pattern_is_file)
        on_file = ""
        if pattern_is_file:
            on_file = f"on {pattern}"
        print(f"\n###################Start Knit Script Interpreter {on_file}###################\n")
        try:
            self._knit_pass_context.execute_statements(statements)
        except (AssertionError, Knit_Script_Error, Knitout_Error) as e:
            self._knit_pass_context.knitout.extend(self._knit_pass_context.machine_state.carrier_system.cut_all_yarns(self._knit_pass_context.machine_state))
            with open("error.k", "w") as out:
                out.writelines([str(k) for k in self._knit_pass_context.knitout])
                if isinstance(e, Knit_Script_Error) or isinstance(e, Knitout_Error):
                    error_comments = [Comment_Line(e.message)]
                    out.writelines([str(ec) for ec in error_comments])
            knitout_to_dat(f"error.k", f"error.dat")
            raise e
            # raise Knit_Script_Error(str(e))
        return self._knit_pass_context.knitout

    def knit_script_evaluate_expression(self, exp) -> Any:
        """
        :param exp: expression to evaluate
        :return: evaluation result
        """
        return exp.evaluate(self._knit_pass_context)
