from unittest import TestCase

from resources.interpret_test_ks import interpret_test_ks

from knit_script.debugger.knitscript_debugger import Knit_Script_Debugger


class TestKnit_Script_Debugger(TestCase):
    def test_take_step_in(self):
        debugger = Knit_Script_Debugger()
        debugger.step()
        program = r"""x= 10;
        if x < 100:{
            x = x + 1;
            assert True;
        }
        """
        interpret_test_ks(program, pattern_is_filename=False, ks_debugger=debugger, execute_knitout=False)
        self.assertEqual(4, len(debugger.machine_snapshots))
        for ln in range(1, 5):
            self.assertIn(ln, debugger.machine_snapshots)

    def test_take_step_over(self):
        debugger = Knit_Script_Debugger()
        debugger.step_over()
        program = r""" x= 10;
                if x < 100:{
                    x = x + 1;
                    assert True;
                }
                x = x + 2;
                """
        interpret_test_ks(program, pattern_is_filename=False, ks_debugger=debugger, execute_knitout=False)
        self.assertEqual(3, len(debugger.machine_snapshots))
        self.assertIn(1, debugger.machine_snapshots)
        self.assertIn(2, debugger.machine_snapshots)
        self.assertIn(6, debugger.machine_snapshots)

    def test_set_breakpoint(self):
        debugger = Knit_Script_Debugger()
        debugger.set_breakpoint(1)
        debugger.set_breakpoint(4)
        program = r"""x= 10;
                if x < 100:{
                    x = x + 1;
                    assert True;
                }
                """
        interpret_test_ks(program, pattern_is_filename=False, ks_debugger=debugger, execute_knitout=False)
        self.assertEqual(len(debugger.machine_snapshots), 2)
        self.assertIn(1, debugger.machine_snapshots)
        self.assertIn(4, debugger.machine_snapshots)

    def test_set_breakpoint_with_condition(self):
        debugger = Knit_Script_Debugger()
        scope_check = lambda d: "x" in d._context.variable_scope
        debugger.set_breakpoint(1, scope_check)
        debugger.set_breakpoint(2, scope_check)
        program = r"""x= 10;
                if x < 100:{
                    x = x + 1;
                    assert True;
                }
                """
        interpret_test_ks(program, pattern_is_filename=False, ks_debugger=debugger, execute_knitout=False)
        self.assertEqual(len(debugger.machine_snapshots), 1)
        self.assertIn(2, debugger.machine_snapshots)

    def test_clear_breakpoint(self):
        debugger = Knit_Script_Debugger()
        debugger.set_breakpoint(1)
        debugger.set_breakpoint(4)
        debugger.clear_breakpoint(1)
        program = r"""x= 10;
                        if x < 100:{
                            x = x + 1;
                            assert True;
                        }
                        """
        interpret_test_ks(program, pattern_is_filename=False, ks_debugger=debugger, execute_knitout=False)
        self.assertEqual(len(debugger.machine_snapshots), 1)
        self.assertIn(4, debugger.machine_snapshots)

    def test_enable_breakpoint(self):
        debugger = Knit_Script_Debugger()
        debugger.set_breakpoint(1)
        debugger.set_breakpoint(4)
        debugger.disable_breakpoint(1)
        debugger.enable_breakpoint(2)
        debugger.set_breakpoint(1)
        program = r"""x= 10;
                                        if x < 100:{
                                            x = x + 1;
                                            assert True;
                                        }
                                        """
        interpret_test_ks(program, pattern_is_filename=False, ks_debugger=debugger, execute_knitout=False)
        self.assertEqual(len(debugger.machine_snapshots), 3)
        self.assertIn(1, debugger.machine_snapshots)
        self.assertIn(2, debugger.machine_snapshots)
        self.assertIn(4, debugger.machine_snapshots)

    def test_disable_breakpoint(self):
        debugger = Knit_Script_Debugger()
        debugger.set_breakpoint(1)
        debugger.set_breakpoint(4)
        debugger.disable_breakpoint(1)
        program = r"""x= 10;
                                if x < 100:{
                                    x = x + 1;
                                    assert True;
                                }
                                """
        interpret_test_ks(program, pattern_is_filename=False, ks_debugger=debugger, execute_knitout=False)
        self.assertEqual(len(debugger.machine_snapshots), 1)
        self.assertIn(4, debugger.machine_snapshots)

    def test_stop_on_condition_errors(self):
        debugger = Knit_Script_Debugger()
        scope_check = lambda d: d._context.variable_scope["x"] == 10
        debugger.set_breakpoint(1, scope_check)
        debugger.set_breakpoint(2, scope_check)
        program = r"""x= 10;
                        if x < 100:{
                            x = x + 1;
                            assert True;
                        }
                        """
        interpret_test_ks(program, pattern_is_filename=False, ks_debugger=debugger, execute_knitout=False)
        self.assertEqual(len(debugger.machine_snapshots), 2)
        self.assertIn(1, debugger.machine_snapshots)
        self.assertIn(2, debugger.machine_snapshots)

    def test_take_step_out(self):
        debugger = Knit_Script_Debugger()
        debugger.set_breakpoint(5)
        debugger.set_breakpoint(8)
        debugger.step_out()
        program = r""" def func1():{
            return 1;
        }
        def func2(value=2):{
            return value;
        }
        def func3(val1, val2):{
            value = val1 + val2;
            return value;
        }
        v1 = func1();
        v2 = func2(10);
        v3 = func3(v1, v2);
        assert v3 == 11;
                        """
        interpret_test_ks(program, pattern_is_filename=False, ks_debugger=debugger, execute_knitout=False)
        self.assertEqual(len(debugger.machine_snapshots), 4)
        self.assertIn(5, debugger.machine_snapshots)
        self.assertIn(8, debugger.machine_snapshots)
        self.assertIn(13, debugger.machine_snapshots)
        self.assertIn(14, debugger.machine_snapshots)
