from unittest import TestCase

from knit_script.knit_script_interpreter.Knit_Script_Interpreter import Knit_Script_Interpreter
from knit_script.knitout_compilers.compile_knitout import knitout_to_dat


class Test_Imports(TestCase):
    parser = Knit_Script_Interpreter(debug_grammar=False, debug_parser=False, debug_parser_layout=False)

    def test_python_import_with_alias(self):
        program = r"""
                    import knit_script.knitting_machine.machine_components.needles as needles;
                    cat = needles.Needle(True, 1);
                    print cat;
                """
        knitout, knit_graph = self.parser.write_knitout(program, f"import_test.k", pattern_is_file=False)
        program = r"""
                    import typing;
                    print typing.Optional;
                """
        knitout, knit_graph = self.parser.write_knitout(program, f"import_test.k", pattern_is_file=False)

    def test_python_import(self):
        program = r"""
                    import knit_script.knitting_machine.machine_components.needles;
                    cat = knit_script.knitting_machine.machine_components.needles.Needle(True, 1);
                    print cat;
                """
        knitout, knit_graph = self.parser.write_knitout(program, f"import_test.k", pattern_is_file=False)

    def test_ks_import_library(self):
        program = r"""
                    import cast_ons;
                    with Carrier as 1:{
                        cast_ons.cast_on(10);
                    }
                """
        knitout, knit_graph = self.parser.write_knitout(program, f"import_test.k", pattern_is_file=False)
        name = 'import_test'
        knitout_to_dat(f"{name}.k", f"{name}.dat")

    def test_ks_import_library_alias(self):
        program = r"""
                    import cast_ons as c;
                    with Carrier as 1:{
                        c.cast_on(10);
                    }
                """
        knitout, knit_graph = self.parser.write_knitout(program, f"import_test.k", pattern_is_file=False)
        name = 'import_test'
        knitout_to_dat(f"{name}.k", f"{name}.dat")

    def test_ks_import_local(self):
        program = r"""
                    import import_tests.cast_ons;
                    with Carrier as 1:{
                        import_tests.cast_ons.cast_on(10);
                    }
                """
        knitout, knit_graph = self.parser.write_knitout(program, f"import_test.k", pattern_is_file=False)
        name = 'import_test'
        knitout_to_dat(f"{name}.k", f"{name}.dat")

    def test_ks_import_local_alias(self):
        program = r"""
                    import import_tests.cast_ons as c;
                    with Carrier as 1:{
                        c.cast_on(10);
                    }
                """
        knitout, knit_graph = self.parser.write_knitout(program, f"import_test.k", pattern_is_file=False)
        name = 'import_test'
        knitout_to_dat(f"{name}.k", f"{name}.dat")
