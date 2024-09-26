from unittest import TestCase

from knit_script.knit_script_interpreter.Knit_Script_Interpreter import Knit_Script_Interpreter
from knit_script.knit_script_interpreter.statements.Statement import Expression_Statement


class Test_KnitScript_Parser(TestCase):
    parser = Knit_Script_Interpreter(debug_grammar=False, debug_parser=False, debug_parser_layout=False)

    def _parse_program(self, program: str):
        print(f"Testing:\n{program}")
        statements = self.parser.parse(program)
        for statement in statements:
            if isinstance(statement, Expression_Statement):
                print(f"Expression Statement <{statement}> of value {statement.expression} of type {statement.expression.__class__.__name__}")
            else:
                print(f"<{statement}> of type {statement.__class__.__name__}")
        return statements

    @staticmethod
    def _interpret(program: str, program_is_file: bool = False):
        interpreter = Knit_Script_Interpreter(debug_grammar=False, debug_parser=False, debug_parser_layout=False)
        print(f"Testing: \n{program}")
        knitout_lines = interpreter._interpret_knit_script(program, program_is_file)
        print(f"Output Knitout:")
        print(knitout_lines)
        return knitout_lines
    def test_slices_and_indexing(self):
        self._parse_program("indexable[i];")
        self._parse_program("sliceable[s:];")
        self._parse_program("sliceable[s:e];")
        self._parse_program("sliceable[s:e:sp];")
        self._parse_program("sliceable[s::sp];")
        self._parse_program("sliceable[:e:sp];")
        self._parse_program("sliceable[:e];")
        self._parse_program("sliceable[::sp];")

    def test_interpret_slicing_and_indexing(self):
        program = r"""slicable = [0, 1, 2, 3, 4, 5];
        s = 1;
        e = -1;
        sp = 2;
        print f"{s} = {slicable[s]}";
        print f"{s}->end = {slicable[s:]}";
        print f"{s}->{e} = {slicable[s:e]}";
        print f"{s}->{e}->{sp} = {slicable[s:e:sp]}";
        print f"{s}->end->{sp} = {slicable[s::sp]}";
        print f"start->{e}->{sp} = {slicable[:e:sp]}";
        print f"start->{e} = {slicable[:e]}";
        print f"start->end->{sp} = {slicable[::sp]}";"""
        _knitout_lines = self._interpret(program)
