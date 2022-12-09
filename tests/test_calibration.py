import os
from unittest import TestCase

from interpreter.Knit_Script_Interpreter import Knit_Script_Interpreter
from interpreter.dat_compiler.run_dat_compiler import knitout_to_dat


class Test_Calibration(TestCase):
    sample_directory = f"{os.getcwd()}{os.path.sep}calibration_knits{os.path.sep}"
    parser = Knit_Script_Interpreter(debug_grammar=False, debug_parser=False, debug_parser_layout=False)

    def test_gauge_stst(self):
        name = f"{self.sample_directory}calibration_stst"
        knitout, knit_graph = self.parser.write_knitout(f"{name}.ks", f"{name}.k", pattern_is_file=True)
        knitout_to_dat(f"{name}.k", f"{name}.dat")

    def test_stst(self):
        name = f"{self.sample_directory}stst"
        knitout, knit_graph = self.parser.write_knitout(f"{name}.ks", f"{name}.k", pattern_is_file=True)
        knitout_to_dat(f"{name}.k", f"{name}.dat")