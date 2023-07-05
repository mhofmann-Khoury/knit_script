from unittest import TestCase

from knit_script.knitout_interpreter.Knitout_Parser import Knitout_Parser


def _print_parse(parser, pattern, is_file: bool = False):
    v, header, instructions, codes_by_line, comments = parser.parse(pattern, pattern_is_file=is_file)
    print(f"Version == {v}")
    print(str(header))
    print(str(instructions))
    print(str(codes_by_line))
    print(str(comments))


class TestKnitout_Parser(TestCase):

    def test_magic(self):
        parser = Knitout_Parser(debug_grammar=True, debug_parser=True)
        pattern = r"""
        ;!knitout-2
        ;;Machine: SWG091N2 
        ;;Position: Center 
        ;;Gauge: 15 
        ;;Width: 250 
        ;;Carriers: 1 2 3 4 5 6 7 8 9 10 
        ;;Yarn-5: 50-50 Rust ; 
        inhook  1
        """
        _print_parse(parser, pattern)

    def test_header(self):
        parser = Knitout_Parser(debug_grammar=True, debug_parser=True)
        pattern = r"""
        ;!knitout-2
        ;;Machine: SWG091N2 
        ;;Position: Center 
        ;;Gauge: 15 
        ;;Width: 250 
        ;;Carriers: 1 2 3 4 5 6 7 8 9 10 
        ;;Yarn-5: 50-50 Rust 
        inhook  1
        """
        _print_parse(parser, pattern)
        # ;;Width: 250
        # ;;Carriers: 1 2 3 4 5 6 7 8 9 10
        # ;;Yarn-5: 50-50 Rust

    def test_instructions(self):
        parser = Knitout_Parser(True, True)
        pattern = r"""
        ;!knitout-2
        ;;Machine: SWG091N2
        ;;Position: Center
        ;;Gauge: 15
        inhook  1
        tuck - b39 1 ; comment
        tuck - b37 1
        tuck - b35 1
                """

        _print_parse(parser, pattern)

    def test_comments(self):
        parser = Knitout_Parser(False, False)
        pattern = r"""
        ;!knitout-2
        ;;Machine: SWG091N2
        ;;Position: Center ; header comment
        inhook  1 ; inline comment
        ; solo comment
                """
        _print_parse(parser, pattern)

    def test_sample(self):
        parser = Knitout_Parser(False, False, False)
        pattern = r"""
                ;!knitout-2
        ;;Machine: SWG091N2 ; header comment
        ;;Position: Center 
        ;;Gauge: 15 
        ;;Width: 250 
        ;;Carriers: 1 2 3 4 5 6 7 8 9 10 
        ;;Yarn-5: 50-50 Rust 
                inhook 5; stuff
                
                tuck - f10 5
                tuck - f8 5
                tuck - f6 5
                tuck - f4 5; also stuff
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
                knit - f6 5; another stuff
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
        _print_parse(parser, pattern)
