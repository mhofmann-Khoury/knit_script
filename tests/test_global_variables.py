
from knit_script.knit_script_interpreter.Knit_Script_Interpreter import Knit_Script_Interpreter


class Test_Globals:
    parser = Knit_Script_Interpreter(debug_grammar=False, debug_parser=False, debug_parser_layout=False)

    def test_global_in_sub_Scope(self):
        program = r"""
                    def set_c():{
                        global c = 1;
                    }
                    try: {print c;}
                    catch KeyError as e:{
                        print e;
                    }
                    set_c();
                    print f"c={c}";
                """
        knitout, knit_graph = self.parser.write_knitout(program, f"global_test.k", pattern_is_file=False)