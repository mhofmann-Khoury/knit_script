import random
from unittest import TestCase

from resources.interpret_test_ks import interpret_test_ks


class TestFloat_Value(TestCase):
    def test_none(self):
        program = "assert None is None;"
        interpret_test_ks(program, print_k_lines=False)

    def test_floats(self):
        for _ in range(10):
            val = float(random.randrange(0, 100)) + random.random()
            program = f"assert isinstance({val}, float);"
            interpret_test_ks(program, print_k_lines=False)

    def test_ints(self):
        for _ in range(10):
            val = random.randrange(-100, 100)
            program = f"assert isinstance({val}, int);"
            interpret_test_ks(program, print_k_lines=False)
