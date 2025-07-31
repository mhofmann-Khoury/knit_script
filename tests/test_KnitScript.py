from __future__ import annotations
import unittest

from knit_script.knit_script_interpreter.Knit_Script_Interpreter import Knit_Script_Interpreter


class Test_KnitScript(unittest.TestCase):

    @staticmethod
    def _interpret(program: str, program_is_file: bool = False):
        interpreter = Knit_Script_Interpreter(debug_grammar=False, debug_parser=False, debug_parser_layout=False)
        print(f"Testing: \n{program}")
        knitout_lines = interpreter._interpret_knit_script(program, program_is_file)
        print(f"Output Knitout:")
        print(knitout_lines)
        return knitout_lines

    @staticmethod
    def _knit_file(program_file_name: str = "test_KS_code.ks",
                   out_k_name: str = "test_KS_code.k", out_dat_name: str = "test_KS_code.dat",
                   **kwargs):
        pass
        # knit_script_to_knitout_to_dat(program_file_name, out_k_name, out_dat_name, True, **kwargs)

    def test_Conditional_Branching(self):
        program = """
        if True: {print "Success 1";}
        else: {assert False, "Failure 1";}
        if False: {print "Failure 2.1";  assert False;}
        elif True: {print "Success 2";}
        else: {print "Failure 2.2";  assert False;}
        if False: {print "Failure 3";  assert False;}
        else: {print "Success 3";}
        """
        _knitout_lines = self._interpret(program)

    def test_comparisons(self):
        program = """
        assert 1 == 1;
        assert 1 <= 1;
        assert 1 >= 1;
        assert 1 != 2;
        assert not (1 > 1);
        assert not (1 < 1);
        assert 1 < 2;
        assert 1 <= 2;
        assert 1 < 3.1;
        assert 4 > 1;
        assert 5.1 > 1;
        assert 2 == 1+1;
        assert 1+1 == 2;
        assert 2 is not 1;
        assert 1 in [1, 2];
        assert 3 not in [1, 2];
        assert 1-1 == 0;
        assert 1*1 == 1;
        assert 1/1 == 1;
        assert 1^1 == 1;
        assert 1%1 == 0;
        """
        _knitout_lines = self._interpret(program)

    def test_try_catch(self):
        program = """
        try:{
            assert True;
            print "Success 1";
        } catch:{
            assert False, "Failure 1";
        }
                """
        knitout_lines = self._interpret(program)
        program = """  try: {assert False; assert False, "Failure 2";} catch: { print "Success 2";}"""
        _knitout_lines = self._interpret(program)

    def test_functions(self):
        program = """
        def func():{
            print "No Args, No return";
        }
        func();
        """
        _knitout_lines = self._interpret(program)
        program = """
        def func(a=1):{
            assert a == 1, "Failure 1";
            print f"Default arg a={a}, No return";
        }
        func();
        """
        _knitout_lines = self._interpret(program)
        program = """
                def func(a=1):{
                    assert a == 2, "Failure 2";
                    print f"Set Default arg a={a}, No return";
                }
                func(2);
                """
        _knitout_lines = self._interpret(program)
        program = """
                def func(a):{
                    assert a == 3, "Failure 3";
                    print f"No Default arg a={a}, No return";
                }
                func(3);
                """
        _knitout_lines = self._interpret(program)
        program = """
        def func(a):{
            assert a == 4, "Failure 4";
            return a;
        }
        a = func(4);
        assert a == 4, f"Failure a=={a}";
        print f"Return arg {a}";
        """
        _knitout_lines = self._interpret(program)
        program = """
        def func(a, b):{
            assert a == 5, "Failure 5";
            assert b == 6, "Failure 6";
            return a + b;
        }
        ab = func(5,6);
        assert ab == 11, f"Failure ab=={ab}";
        print f"Return sum of args {ab}";
        """
        _knitout_lines = self._interpret(program)
        program = """
        def func(a=5, b=6):{
            assert a == 5, "Failure 5";
            assert b == 6, "Failure 6";
            return a + b;
        }
        ab = func();
        assert ab == 11, f"Failure ab=={ab}";
        print f"Return sum of default args {ab}";
        """
        _knitout_lines = self._interpret(program)
        program = """
        def func(a=5, b=6):{
            assert a == 5, "Failure 5";
            assert b == 7, "Failure 6";
            return a + b;
        }
        ab = func(b=7);
        assert ab == 12, f"Failure ab=={ab}";
        print f"Return sum of default args {ab}";
        """
        _knitout_lines = self._interpret(program)
        program = """
        def func(a=5, b=6):{
            assert a == 7, "Failure 5";
            assert b == 6, "Failure 6";
            return a + b;
        }
        ab = func(7);
        assert ab == 13, f"Failure ab=={ab}";
        print f"Return sum of default args {ab}";
        """
        _knitout_lines = self._interpret(program)

    def test_iteration_blocks(self):
        program = """
            x= 0;
            while x < 10:{
                print x;
                assert x < 10, f"X exceeds 10: {x}";
                x = x+1;
            }
        """
        _knitout_lines = self._interpret(program)
        program = """
        for x in range(0,10):{
            print x;
            assert x < 10, f"X exceeds 10: {x}";
        }
        """
        _knitout_lines = self._interpret(program)

        program = """
        for x in ["cat", "dog", "bird"]:{
            print x;
        }
        """
        _knitout_lines = self._interpret(program)
        program = """
                for i, x in enumerate(["cat", "dog", "bird"]):{
                    print f"{i}: {x}";
                }
                """
        _knitout_lines = self._interpret(program)

    def test_set_carrier(self):
        program = """
        with Carrier as c1:{
            in reverse direction:{
                knit f1;
            }
            print c1.position;
            in reverse direction:{
                knit b6;
            }
            print c1.position;
            print Carrier.positions(machine.carrier_system);
        }"""
        _knitout_lines = self._interpret(program)
    def test_index_and_slicing(self):
        program = """
        assert [0,1,2][0] == 0;
        assert [0,1,2][1] == 1;
        assert [0,1,2][2] == 2;
        assert [0,1,2][0:1] == [0];
        assert [0,1,2][0:2] == [0,1];
        assert [0,1,2][:1] == [0];
        assert [0,1,2][:2] == [0,1];
        assert [0,1,2][1:3] == [1,2];
        assert [0,1,2][:-1] == [0,1], [0,1,2][:-1];
        assert [0,1,2][0::2] == [0,2], [0,1,2][0::2];
        assert [0,1,2][::2] == [0,2], [0,1,2][::2];
        assert [0,1,2][:-1:2] == [0], [0,1,2][:-1:2];
        """
        _knitout_lines = self._interpret(program)

    def test_basic_knitting(self):
        self._knit_file(width=20, c=1, cb=2)

    def test_gauged_knitting(self):
        self._knit_file("test_gauged_ks_code.ks",
                        "test_gauged_ks_code.k",
                        "test_gauged_ks_code.dat",
                        width=24, c=1)
