from unittest import TestCase

from knit_script.knit_script_interpreter.Knit_Script_Interpreter import Knit_Script_Interpreter
from knit_script.knitout_interpreter.Knitout_Interpreter import Knitout_Interpreter
from knit_script.knitout_interpreter.Knitout_Optimizer import Knitout_Optimizer


class TestKnitout_Optimizer(TestCase):

    def test_optimize(self):
        interpreter = Knitout_Interpreter(False, False)
        pattern = r"""
                    ;!knitout-2
                    inhook 1
                    releasehook 1
                    tuck - f2 1
                    tuck - f1 1
                    knit + f1 1
                    knit + f2 1
                    knit - f2 1
                    knit - f1 1
                    outhook 1
                    """
        _knitout_instructions = interpreter.interpret_knitout(pattern, False, True)
        context = interpreter.context
        optimizer = Knitout_Optimizer(context, 1)
        optimizer.visualize()
        optimized_knitout = optimizer.optimize()
        print(optimized_knitout)

    def test_optimize_rib(self):
        interpreter = Knitout_Interpreter(False, False)
        pattern = r"""
                    ;!knitout-2
                    inhook 1
                    releasehook 1
                    tuck - f4 1
                    tuck - f3 1
                    tuck - f2 1
                    tuck - f1 1
                    knit + f1 1
                    knit + f2 1
                    knit + f3 1
                    knit + f4 1
                    xfer f3 b3
                    xfer f1 b1
                    knit - f4 1
                    knit - b3 1
                    knit - f2 1
                    knit - b1 1
                    outhook 1
                    """

        _knitout_instructions = interpreter.interpret_knitout(pattern, False, True)
        context = interpreter.context
        optimizer = Knitout_Optimizer(context, 1)
        optimizer.visualize()
        optimized_knitout = optimizer.optimize()
        print(optimized_knitout)

    def test_optimize_lace(self):
        interpreter = Knitout_Interpreter(False, False)
        pattern = r"""
                    ;!knitout-2
                    inhook 1
                    releasehook 1
                    knit + f1 1
                    knit + f2 1
                    knit + f3 1
                    knit + f4 1
                    rack 1
                    xfer f2 b1
                    rack 0
                    rack -1
                    xfer f3 b4
                    rack 0
                    xfer b4 f4
                    xfer b1 f1
                    knit - f4 1
                    knit - f1 1
                    outhook 1
                    """
        _knitout_instructions = interpreter.interpret_knitout(pattern, False, True)
        context = interpreter.context
        optimizer = Knitout_Optimizer(context, 1)
        optimizer.visualize()
        optimized_knitout = optimizer.optimize()
        print(optimized_knitout)

    def test_splits(self):
        interpreter = Knitout_Interpreter(False, False)
        pattern = r"""
                ;!knitout-2
                inhook 1
                releasehook 1
                tuck + f1 1
                tuck + f3 1
                tuck - f4 1
                tuck - f2 1
                knit + f1 1
                knit + f2 1
                knit + f3 1
                knit + f4 1
                knit - f4 1
                knit - f3 1
                knit - f2 1
                knit - f1 1
                split + f1 b1 1
                split + f2 b2 1
                split + f3 b3 1
                split + f4 b4 1
                outhook 1
                """
        _knitout_instructions = interpreter.interpret_knitout(pattern, False, True)
        context = interpreter.context
        optimizer = Knitout_Optimizer(context, 1)
        optimizer.visualize()
        optimized_knitout = optimizer.optimize()
        print(optimized_knitout)

    def test_inhook_placement(self):
        interpreter = Knitout_Interpreter(False, False)
        pattern = r"""
                        ;!knitout-2
                        inhook 1
                        releasehook 1
                        inhook 2
                        releasehook 2
                        tuck + f1 1
                        tuck + f2 1
                        tuck + f3 1
                        tuck + f4 1
                        knit + f1 2
                        knit + f2 2
                        knit + f3 2
                        knit + f4 2
                        knit - f4 1
                        knit - f3 1
                        knit - f2 1
                        knit - f1 1
                        knit - f4 2
                        knit - f3 2
                        knit - f2 2
                        knit - f1 2
                        outhook 1
                        outhook 2
                        """
        _knitout_instructions = interpreter.interpret_knitout(pattern, False, True)
        context = interpreter.context
        optimizer = Knitout_Optimizer(context, 1)
        optimizer.visualize()
        optimized_knitout = optimizer.optimize()
        print(optimized_knitout)

    def test_xfer_releasehook(self):
        interpreter = Knitout_Interpreter(False, False)
        pattern = r"""
                        ;!knitout-2
                        inhook 1
                        releasehook 1
                        tuck + f1 1
                        tuck + f2 1
                        tuck + f3 1
                        tuck + f4 1
                        xfer f1 b1
                        xfer f2 b2
                        xfer f3 b3
                        xfer f4 b4
                        knit - b4 1
                        knit - b3 1
                        knit - b2 1
                        knit - b1 1
                        knit + b1 1
                        knit + b2 1
                        knit + b3 1
                        knit + b4 1
                        outhook 1
                        """
        _knitout_instructions = interpreter.interpret_knitout(pattern, False, True)
        context = interpreter.context
        optimizer = Knitout_Optimizer(context, 5)
        optimizer.visualize()
        optimized_knitout = optimizer.optimize()
        print(optimized_knitout)

    def test_small_op_set(self):
        ks_interpreter = Knit_Script_Interpreter()
        program = r"""
        with Carrier as 1, s as 2, e as 6:{
            in reverse direction:{
                tuck Front_Needles[s:e];
            }
        }
        """
        knitout, _knit_graph, _machine_state = ks_interpreter.write_knitout(program, "small_op.k", pattern_is_file=False, optimize=False)
        print(knitout)
        knitout, _knit_graph, _machine_state = ks_interpreter.write_knitout(program, "small_op.k", pattern_is_file=False, optimize=True)
        print(knitout)