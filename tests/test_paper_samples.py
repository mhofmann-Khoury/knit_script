import os
from unittest import TestCase

from dat_compiler.run_dat_compiler import knitout_to_dat
from interpreter.kp_interpretor import Knit_Pass_Interpreter


class TestKnit_Pass_Interpreter(TestCase):
    sample_directory = f"{os.getcwd()}{os.path.sep}paper_samples{os.path.sep}"
    parser = Knit_Pass_Interpreter(debug_grammar=False, debug_parser=False, debug_parser_layout=False)

    def test_rib_round(self):
        name = f"{self.sample_directory}sheet_tube"
        knitout, knit_graph = self.parser.write_knitout(f"{name}.ks", f"{name}.k", pattern_is_file=True)
        knitout_to_dat(f"{name}.k", f"{name}.dat")

    def test_two_tube(self):
        name = f"{self.sample_directory}two_tube"
        knitout, knit_graph = self.parser.write_knitout(f"{name}.ks", f"{name}.k", pattern_is_file=True)
        knitout_to_dat(f"{name}.k", f"{name}.dat")

    def test_color_stripes(self):
        name = f"{self.sample_directory}color_stripes"
        knitout, knit_graph = self.parser.write_knitout(f"{name}.ks", f"{name}.k", pattern_is_file=True)
        knitout_to_dat(f"{name}.k", f"{name}.dat")

    def test_bad_floats(self):
        name = f"{self.sample_directory}bad_floats"
        knitout, knit_graph = self.parser.write_knitout(f"{name}.ks", f"{name}.k", pattern_is_file=True)
        knitout_to_dat(f"{name}.k", f"{name}.dat")

    # def test_jacquard_round(self):
    #     name = f"{self.sample_directory}jacquard_round"
    #     knitout = self.parser.write_knitout(f"{name}.ks", f"{name}.k", pattern_is_file=True)
    #     knitout_to_dat(f"{name}.k", f"{name}.dat")
    #     print(knitout)

    def test_jacquard_sheet(self):
        name = f"{self.sample_directory}birdseye_sheet"
        knitout, knit_graph = self.parser.write_knitout(f"{name}.ks", f"{name}.k", pattern_is_file=True)
        knitout_to_dat(f"{name}.k", f"{name}.dat")

    def test_birdseye_round(self):
        name = f"{self.sample_directory}birdseye_round"
        knitout, knit_graph = self.parser.write_knitout(f"{name}.ks", f"{name}.k", pattern_is_file=True)
        knitout_to_dat(f"{name}.k", f"{name}.dat")

