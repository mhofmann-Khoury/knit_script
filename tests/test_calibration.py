"""Sample knitscript from calibration directory"""
import os
from unittest import TestCase

from knit_script.knit_script_interpreter.Knit_Script_Interpreter import Knit_Script_Interpreter
from knit_script.knitout_compilers.compile_knitout import knitout_to_dat
from test_resource_access import get_test_resource


class Test_Calibration(TestCase):
    sample_directory = f"{os.getcwd()}{os.path.sep}calibration_knits{os.path.sep}"
    parser = Knit_Script_Interpreter(debug_grammar=False, debug_parser=False, debug_parser_layout=False)

    def test_gauge_stst(self):
        name = "calibration_stst"
        resource = get_test_resource(f"{name}.ks", "calibration_knits")
        name = resource[:-3]
        knitout, knit_graph = self.parser.write_knitout(resource, f"{name}.k", pattern_is_file=True)
        knitout_to_dat(f"{name}.k", f"{name}.dat")

    def test_stst(self):
        name = f"{self.sample_directory}stst"
        knitout, knit_graph = self.parser.write_knitout(f"{name}.ks", f"{name}.k", pattern_is_file=True)
        knitout_to_dat(f"{name}.k", f"{name}.dat")

    def test_platting(self):
        name = f"{self.sample_directory}plating"
        knitout, knit_graph = self.parser.write_knitout(f"{name}.ks", f"{name}.k", pattern_is_file=True)
        knitout_to_dat(f"{name}.k", f"{name}.dat")

    def test_carrier_swap(self):
        name = f"{self.sample_directory}carrier_play"
        knitout, knit_graph = self.parser.write_knitout(f"{name}.ks", f"{name}.k", pattern_is_file=True)
        knitout_to_dat(f"{name}.k", f"{name}.dat")

