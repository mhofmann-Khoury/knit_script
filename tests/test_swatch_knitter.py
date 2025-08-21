from unittest import TestCase

from knit_graphs.Knit_Graph import Knit_Graph
from knitout_interpreter.knitout_execution import Knitout_Executer
from knitout_interpreter.knitout_operations.Knitout_Line import Knitout_Comment_Line
from knitout_interpreter.run_knitout import run_knitout
from resources.load_test_resources import load_test_resource

from knit_script.interpret_knit_script import knit_script_to_knitout


class Test_Swatch_Knitter(TestCase):

    def _compare_swatch_knitter_result(self, k_file: str, swatch: Knit_Graph):
        swatch_instructions, _, __ = run_knitout(k_file)
        swatch_executer = Knitout_Executer(swatch_instructions)
        swatch_instructions = [i for i in swatch_executer.executed_instructions if not isinstance(i, Knitout_Comment_Line)]

        program = load_test_resource("swatch_knitter.ks")
        courses = swatch.get_courses()
        swatch_from_kg_file = f"{k_file.split('.')[0]}_from_kg.k"
        _swatch_from_kg, _machine_from_kg = knit_script_to_knitout(program, swatch_from_kg_file, pattern_is_filename=True,
                                                                   swatch=swatch, courses=courses)
        swatch_from_kg_instructions, _, __ = run_knitout(swatch_from_kg_file)
        swatch_from_kg_executer = Knitout_Executer(swatch_from_kg_instructions)
        swatch_from_kg_instructions = [i for i in swatch_from_kg_executer.executed_instructions if not isinstance(i, Knitout_Comment_Line)]

        i = 0
        for i_from_swatch, i_from_kg_swatch in zip(swatch_instructions, swatch_from_kg_instructions):
            self.assertEqual(str(i_from_swatch), str(i_from_kg_swatch), f"instructions {i}: {i_from_swatch} != {i_from_kg_swatch}")
            i += 1
        self.assertEqual(len(swatch_instructions), len(swatch_from_kg_instructions))

    def test_jersey(self):
        program = load_test_resource("jersey_swatch.ks")
        swatch_k_file = 'jersey.k'
        jersey_swatch, _machine = knit_script_to_knitout(program, swatch_k_file, pattern_is_filename=True,
                                                         height=4, width=4)
        self._compare_swatch_knitter_result(swatch_k_file, jersey_swatch)

    def test_rib(self):
        program = load_test_resource("rib_swatch.ks")
        swatch_k_file = 'rib.k'
        swatch, _machine = knit_script_to_knitout(program, swatch_k_file, pattern_is_filename=True,
                                                  height=4, width=4)
        self._compare_swatch_knitter_result(swatch_k_file, swatch)

    def test_seed(self):
        program = load_test_resource("seed_swatch.ks")
        swatch_k_file = 'seed.k'
        swatch, _machine = knit_script_to_knitout(program, swatch_k_file, pattern_is_filename=True,
                                                  height=4, width=4)
        self._compare_swatch_knitter_result(swatch_k_file, swatch)

    def test_lace_mesh(self):
        program = load_test_resource("lace_mesh.ks")
        swatch_k_file = 'lace.k'
        swatch, _machine = knit_script_to_knitout(program, swatch_k_file, pattern_is_filename=True,
                                                  height=4, width=6)
        self._compare_swatch_knitter_result(swatch_k_file, swatch)
