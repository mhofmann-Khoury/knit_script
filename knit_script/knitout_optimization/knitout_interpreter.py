from knit_script.knitout_optimization.knitout_parser import Knitout_Parser


class Knit_Script_Interpreter:
    """
        A class to manage parsing a knit script file with parglare
    """

    def __init__(self, debug_grammar: bool = False, debug_parser: bool = False, debug_parser_layout: bool = False):
        """
        Instantiate
        :param debug_grammar: Will provide full parglare output for grammar states
        :param debug_parser: Will provide full parglare output for parsed file shift reduce status
        :param debug_parser_layout: Will provide layout information from parser
        """
        self._parser: Knitout_Parser = Knitout_Parser(debug_grammar, debug_parser, debug_parser_layout)
