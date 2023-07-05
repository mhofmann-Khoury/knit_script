import os
from unittest import TestCase

from knit_script.knit_script_interpreter.Knit_Script_Interpreter import Knit_Script_Interpreter
from knit_script.knitout_compilers.compile_knitout import knitout_to_dat


class Test_Examples(TestCase):
    sample_directory = f"{os.getcwd()}{os.path.sep}examples{os.path.sep}"
    parser = Knit_Script_Interpreter(debug_grammar=False, debug_parser=False, debug_parser_layout=False)

    def test_swatch(self):
        name = f"{self.sample_directory}kp_textures"
        knitout, knit_graph = self.parser.write_knitout(f"{name}.ks", f"{name}.k", pattern_is_file=True)
        knitout_to_dat(f"{name}.k", f"{name}.dat")

    def test_kp_tube_hard(self):
        name = f"{self.sample_directory}kp_tube_the_hard_way"
        knitout, knit_graph = self.parser.write_knitout(f"{name}.ks", f"{name}.k", pattern_is_file=True)
        knitout_to_dat(f"{name}.k", f"{name}.dat")

    def test_layer_tube(self):
        name = f"{self.sample_directory}split_tube"
        knitout, knit_graph = self.parser.write_knitout(f"{name}.ks", f"{name}.k", pattern_is_file=True)
        knitout_to_dat(f"{name}.k", f"{name}.dat")

    def test_bind_off(self):
        name = f"{self.sample_directory}bo_test"
        knitout, knit_graph = self.parser.write_knitout(f"{name}.ks", f"{name}.k", pattern_is_file=True)
        knitout_to_dat(f"{name}.k", f"{name}.dat")
