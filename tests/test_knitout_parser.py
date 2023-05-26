from unittest import TestCase

from knit_script.knitout_optimization.knitout_parser import Knitout_Parser


class TestKnitout_Parser(TestCase):
    def test_header(self):
        parser = Knitout_Parser(True, True)
        pattern = r"""
        ;!knitout-2
        ;;Machine: SWG091N2
        ;;Position: Center
        ;;Gauge: 15
        ;;Width: 250
        ;;Carriers: 1 2 3 4 5 6 7 8 9 10
        ;;Yarn-5: 50-50 Rust
        """
        v, header, instructions = parser.parse(pattern, pattern_is_file=False)
        print(f"Version == {v}")
        print(str(header))
        print(str(instructions))

    def test_instructions(self):
        parser = Knitout_Parser(True, True)
        pattern = r"""
        ;!knitout-2
        inhook  1 ;
        tuck - b39 1 ; 
        tuck - b37 1 ; 
        tuck - b35 1 ; 
                """
        v, header, instructions = parser.parse(pattern, pattern_is_file=False)
        print(f"Version == {v}")
        print(str(header))
        print(str(instructions))

    def test_sample(self):
        parser = Knitout_Parser(True, True)
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
        v, header, instructions = parser.parse(pattern, pattern_is_file=False)
        print(f"Version == {v}")
        print(str(header))
        print(str(instructions))