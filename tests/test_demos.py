"""Create research samples"""
import os
from unittest import TestCase

from knit_script.knit_script_interpreter.Knit_Script_Interpreter import Knit_Script_Interpreter
from knit_script.knitout_compilers.compile_knitout import knitout_to_dat


class Test_Paper_Samples(TestCase):
    sample_directory = f"{os.getcwd()}{os.path.sep}demos{os.path.sep}"
    parser = Knit_Script_Interpreter(debug_grammar=False, debug_parser=False, debug_parser_layout=False)

    def test_chain(self):
        name = f"{self.sample_directory}chains"
        knitout, knit_graph = self.parser.write_knitout(f"{name}.ks", f"{name}.k", pattern_is_file=True)
        knitout_to_dat(f"{name}.k", f"{name}.dat")

    def test_chain_mail(self):
        name = f"{self.sample_directory}chain_mail"
        knitout, knit_graph = self.parser.write_knitout(f"{name}.ks", f"{name}.k", pattern_is_file=True)
        knitout_to_dat(f"{name}.k", f"{name}.dat")

