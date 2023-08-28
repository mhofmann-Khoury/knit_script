"""Errors associated with knit script parsing"""

from parglare import ParseError, Terminal

from knit_script.Knit_Errors.Knit_Script_Error import Knit_Script_Error


class Knit_Script_Parse_Error(Knit_Script_Error):
    """
        General error reporting for knit script parser errors
    """

    def __init__(self, parse_error: ParseError):
        self.parse_error = parse_error
        super().__init__(self.parse_message())

    @property
    def parse_error_str(self) -> str:
        """
        :return: Error string from parent parsing error
        """
        return self.parse_error.args[0]

    def _split_parse_error(self) -> tuple[str, str]:
        before_expected = self.parse_error_str.split('=>')[0]
        quote_split = before_expected.split("\"")
        quote = quote_split[1]
        split_quote = quote.split("**>")
        return split_quote[0], split_quote[1]

    def _is_incomplete_line(self) -> bool:
        return len(self.parse_error.tokens_ahead) == 0

    def _next_tokens(self) -> list[str]:
        return [token.value for token in self.parse_error.tokens_ahead]

    def _expected_terminals(self) -> list[str]:
        return [t.name for t in self.parse_error.symbols_expected if isinstance(t, Terminal)]

    def _block_next(self) -> bool:
        return "{" in self._next_tokens() and ":" in self._expected_terminals()

    def _missing_rh_paren(self) -> bool:
        return ")" in self._expected_terminals()

    def parse_message(self):
        """
        :return: Message to report to exception
        """
        before, after = self._split_parse_error()
        details = ""
        if self._is_incomplete_line():
            details = "Statement is incomplete. May be missing a semi-colon"
        elif self._block_next():
            details = "Predicate and code block may need a colon to separate them."
        elif self._missing_rh_paren():
            details = "May be missing ')'"
        details += "\n"
        return f'Knit Script Parsing Error at line {self.parse_error.location.line} between "{before}" and "{after}"\n{details}'
