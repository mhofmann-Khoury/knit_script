from unittest import TestCase

from knit_script.knitout_optimization.Knitout_Interpreter import Knitout_Interpreter


class TestKnitout_Interpreter(TestCase):
    def test_header(self):
        interpreter = Knitout_Interpreter(True, True)
        pattern = r"""
        ;!knitout-2
        ;;Machine: SWG091N2
        ;;Position: Center
        ;;Gauge: 15
        ;;Width: 250
        ;;Carriers: 1 2 3 4 5 6 7 8 9 10
        ;;Yarn-5: 50-50 Rust
        """
        interpreter.write_trimmed_knitout(pattern, out_file="test.k", pattern_is_file=False)

    def test_instructions(self):
        interpreter = Knitout_Interpreter(True, True)
        pattern = r"""
        ;!knitout-2
        inhook  1 ;
        tuck - b39 1 ; comment
        tuck - b37 1 ; 
        tuck - b35 1 ; 
                """

        interpreter.write_trimmed_knitout(pattern, out_file="test.k", pattern_is_file=False)

    def test_comments(self):
        interpreter = Knitout_Interpreter(True, True)
        pattern = r"""
        ;!knitout-2
        ;;Machine: SWG091N2
        ;;Position: Center ; header comment
        inhook  1 ; inline comment
        ; solo comment
                """
        interpreter.write_trimmed_knitout(pattern, out_file="test.k", pattern_is_file=False)

    def test_sample(self):
        interpreter = Knitout_Interpreter(True, True)
        pattern = r"""
                ;!knitout-2
                ;;Machine: SWG091N2
                ;;Gauge: 15
                ;;Yarn-5: 50-50 Rust
                ;;Carriers: 1 2 3 4 5 6 7 8 9 10
                ;;Position: Right

                inhook 5

                tuck - f10 5
                tuck - f8 5
                tuck - f6 5
                tuck - f4 5
                tuck - f2 5
                tuck + f1 5
                tuck + f3 5
                tuck + f5 5
                tuck + f7 5
                tuck + f9 5

                releasehook 5

                knit - f10 5
                knit - f9 5
                knit - f8 5
                knit - f7 5
                knit - f6 5
                knit - f5 5
                knit - f4 5
                knit - f3 5
                knit - f2 5
                knit - f1 5

                knit + f1 5
                knit + f2 5
                knit + f3 5
                knit + f4 5
                knit + f5 5
                knit + f6 5
                knit + f7 5
                knit + f8 5
                knit + f9 5
                knit + f10 5

                outhook 5
                        """
        interpreter.write_trimmed_knitout(pattern, out_file="test.k", pattern_is_file=False)
