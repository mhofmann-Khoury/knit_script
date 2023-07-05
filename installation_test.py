from knit_script.knit_script_interpreter.Knit_Script_Interpreter import Knit_Script_Interpreter
from knit_script.knitout_compilers.compile_knitout import knitout_to_dat

parser = Knit_Script_Interpreter(debug_grammar=False, debug_parser=False, debug_parser_layout=False)
program = r"""
            import cast_ons;
            import stockinette;
            
            with Carrier as 1, width as 10, height as 10:{
                cast_ons.alt_tuck_cast_on(width);
                stockinette.stst(height);                
            }
        """
knitout, knit_graph = parser.write_knitout(program, f"stst_10.k", pattern_is_file=False)

knitout_to_dat(f"stst_10.k", f"stst_10.dat")