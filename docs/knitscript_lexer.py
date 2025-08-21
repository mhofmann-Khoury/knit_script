"""
Custom Pygments lexer for KnitScript syntax highlighting.
Save this as: docs/knitscript_lexer.py or docs/source/knitscript_lexer.py
"""

from pygments.lexer import RegexLexer, words
from pygments.token import (
    Comment,
    Error,
    Keyword,
    Name,
    Number,
    Operator,
    Punctuation,
    String,
    Text,
)

__all__ = ['KnitScriptLexer']


class KnitScriptLexer(RegexLexer):
    """A Pygments lexer for KnitScript syntax highlighting."""

    name = 'KnitScript'
    aliases = ['knitscript', 'ks']
    filenames = ['*.ks']
    mimetypes = ['text/x-knitscript']

    # KnitScript keywords
    keywords = (
        'def', 'if', 'else', 'elif', 'for', 'while', 'in', 'return',
        'try', 'catch', 'with', 'as', 'import', 'global', 'assert',
        'True', 'False', 'None', 'and', 'or', 'not', 'is', 'range'
    )

    # Machine-specific keywords
    machine_keywords = (
        'knit', 'tuck', 'miss', 'split', 'xfer', 'drop', 'cut', 'remove',
        'releasehook', 'pause', 'direction', 'rightward', 'leftward',
        'reverse', 'current', 'across', 'to', 'bed', 'sliders',
        'front', 'back', 'left', 'right', 'forward', 'backward',
        'push', 'swap', 'layer', 'sheet'
    )

    # Machine state variables
    machine_variables = (
        'Carrier', 'Gauge', 'Sheet', 'Racking', 'Front_Needles',
        'Back_Needles', 'Front_Loops', 'Back_Loops', 'Loops',
        'Front_Sliders', 'Back_Sliders', 'Needles', 'Sliders',
        'Front_Slider_Loops', 'Back_Slider_Loops', 'Slider_Loops'
    )

    tokens = {
        'root': [
            # Comments
            (r'//.*', Comment.Single),
            (r'/\*.*?\*/', Comment.Multiline),

            # Strings
            (r'"([^"\\]|\\.)*"', String.Double),
            (r"'([^'\\]|\\.)*'", String.Single),
            (r'f"([^"\\]|\\.)*"', String.Interpol),
            (r"f'([^'\\]|\\.)*'", String.Interpol),

            # Numbers
            (r'\d+\.\d+', Number.Float),
            (r'\d+', Number.Integer),

            # Machine state variables (highlighted specially)
            (words(machine_variables, suffix=r'\b'), Name.Builtin),

            # Machine keywords (highlighted as keywords)
            (words(machine_keywords, suffix=r'\b'), Keyword.Reserved),

            # Regular keywords
            (words(keywords, suffix=r'\b'), Keyword),

            # Needle identifiers (f1, b2, fs3, etc.)
            (r'[fb]s?\d+', Name.Variable),

            # Carrier identifiers (c1, c2, etc.)
            (r'c\d+', Name.Variable),

            # Sheet identifiers (s0, s1, etc.)
            (r's\d+', Name.Variable),

            # Operators
            (r'[+\-*/^%]', Operator),
            (r'[<>=!]=?', Operator),
            (r'[&|]', Operator),

            # Punctuation
            (r'[{}()\[\];:,.]', Punctuation),

            # Identifiers
            (r'[a-zA-Z_][a-zA-Z0-9_]*', Name),

            # Whitespace
            (r'\s+', Text),

            # Anything else
            (r'.', Error),
        ]
    }
