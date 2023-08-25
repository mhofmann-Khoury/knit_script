from knit_script.interpret import knit_script_to_knitout_to_dat
from knit_script.knitout_interpreter.Knitout_Interpreter import Knitout_Interpreter

interpreter = Knitout_Interpreter(False, False)


def _write_clean_instructions(name: str, optimize=True):
    knit_script_to_knitout_to_dat(f"{name}.ks", f"{name}.k", f"{name}.dat", pattern_is_filename=True, optimize=optimize)
    interpreter.write_trimmed_knitout(f"{name}.k", f'{name}_clean.k', pattern_is_file=True)


test_name = "sample"
_write_clean_instructions(test_name, optimize=True)

