from unittest import TestCase

from knitout_interpreter.knitout_operations.needle_instructions import Tuck_Instruction
from resources.interpret_test_ks import count_lines, interpret_test_ks


class TestFunctions(TestCase):
    def test_simple_function(self):
        program = r"""
        def f():{
            in Leftward direction:{
                tuck Front_Needles[0:4];
            }
            releasehook;
        }
        with Carrier as c1:{ assert f() is None;}
        """
        klines, _, __ = interpret_test_ks(program)
        assert count_lines(klines, include_types={Tuck_Instruction}) == 4

    def test_parameter_function(self):
        program = r"""
                def f(w):{
                    in Leftward direction:{
                        tuck Front_Needles[0:w];
                    }
                    releasehook;
                }
                with Carrier as c1:{ f(4);}
                """
        klines, _, __ = interpret_test_ks(program)
        assert count_lines(klines, include_types={Tuck_Instruction}) == 4

    def test_default_parameter_function(self):
        program = r"""
                def f(w=4):{
                    in Leftward direction:{
                        tuck Front_Needles[0:w];
                    }
                    releasehook;
                }
                with Carrier as c1:{
                    f();
                    f(6);
                }
                """
        klines, _, __ = interpret_test_ks(program)
        assert count_lines(klines, include_types={Tuck_Instruction}) == 10

    def test_multiple_parameter_function(self):
        program = r"""
                def f(w,h):{
                    for _ in range(h):{
                        in reverse direction:{
                            tuck Front_Needles[0:w];
                        }
                        releasehook;
                    }
                }
                with Carrier as c1:{ f(2,2);}
                """
        klines, _, __ = interpret_test_ks(program)
        assert count_lines(klines, include_types={Tuck_Instruction}) == 4

    def test_function_parameter_scope(self):
        program = r"""
        p = "dog";
        print f"before define f: {p}";
        def f():{
            p = "cat";
            print f"in f: {p}";
        }
        print f"after define f: {p}";
        f();
        print f"after f: {p}";
        """
        interpret_test_ks(program)

    def test_function_def_parameter_scope_clears(self):
        program = r"""
        def f():{
            p = "cat";
            print f"in f: {p}";
        }
        print f"{p} should raise Name error";
        f();
        """
        try:
            interpret_test_ks(program)
        except NameError as _e:
            pass

    def test_function_parameter_scope_clears(self):
        program = r"""
        def f():{
            p = "cat";
            print f"in f: {p}";
        }
        f();
        print f"{p} should raise Name error";
        """
        try:
            interpret_test_ks(program)
        except NameError as _e:
            pass

    def test_function_returns(self):
        program = r"""
        def f():{
            in Leftward direction:{
                tuck Front_Needles[0:4];
            }
            releasehook;
            return Front_Needles[5];
        }
        with Carrier as c1:{ assert f()== f5;}
        """
        klines, _, __ = interpret_test_ks(program)
        assert count_lines(klines, include_types={Tuck_Instruction}) == 4
