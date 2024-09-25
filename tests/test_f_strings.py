from unittest import TestCase

from knit_script.knit_script_interpreter.Knit_Script_Interpreter import Knit_Script_Interpreter
from knit_script.knit_script_interpreter.statements.Statement import Expression_Statement


class Test_KnitScript_Parser(TestCase):
    parser = Knit_Script_Interpreter(debug_grammar=False, debug_parser=False, debug_parser_layout=False)

    @staticmethod
    def _interpret(program: str, program_is_file: bool = False):
        interpreter = Knit_Script_Interpreter(debug_grammar=False, debug_parser=False, debug_parser_layout=False)
        print(f"Testing: \n{program}")
        knitout_lines = interpreter._interpret_knit_script(program, program_is_file)
        print(f"Output Knitout:")
        print(knitout_lines)
        return knitout_lines

    def _parse_program(self, program: str):
        print(f"Testing:\n{program}")
        statements = self.parser.parse(program)
        for statement in statements:
            if isinstance(statement, Expression_Statement):
                print(f"Expression Statement <{statement}> of value {statement.expression} of type {statement.expression.__class__.__name__}")
            else:
                print(f"<{statement}> of type {statement.__class__.__name__}")
        return statements

    def test_parse_f_string_with_space(self):
        program = r""" f"before string {2+2} after string {2+3}: after string no space."; """
        statements = self._parse_program(program)
        assert len(statements) == 1
        for expression in statements[0].expression.expressions:
            evaluation = expression.evaluate(None)
            print(evaluation)

    def test_parse_string_with_space(self):
        program = r""" "\n\t: string"; """
        statements = self._parse_program(program)
        assert len(statements) == 1

    def test_interpret_string_with_space(self):
        program = r""" print " :\n\t: string"; """
        knitout_lines = self._interpret(program)

    def test_interpret_f_string_with_space(self):
        program = r""" print f"before string {2+2} after string {2+3}: after string no space."; """
        knitout_lines = self._interpret(program)
        program = r""" print f" before string {2+2} after string {2+3}: after string no space."; """
        knitout_lines = self._interpret(program)
        program = r""" print f" before string {2+2}     after string {2+3}  after string two space."; """
        knitout_lines = self._interpret(program)
        program = r""" print f" before string {2+2} after string {2+3}\n: after string with new line"; """
        knitout_lines = self._interpret(program)
