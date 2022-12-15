from knit_script.knit_script_interpreter.Knit_Script_Interpreter import Knit_Script_Interpreter


class Test_Imports:
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
