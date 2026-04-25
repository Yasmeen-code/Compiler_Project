NUMBER = 'NUMBER'
PLUS = 'PLUS'
MINUS = 'MINUS'
MUL = 'MUL'
DIV = 'DIV'
GE = 'GE'
LE = 'LE'
LT = 'LT'
NE = 'NE'
INCREMENT = 'INCR'
DECREMENT = 'DECR'
LPAREN = 'LPAREN'
RPAREN = 'RPAREN'
LBRACE = 'LBRACE'
RBRACE = 'RBRACE'
ID = 'ID'
ASSIGN = 'ASSIGN'
END = 'END'
COMMA = 'COMMA'
IF = 'IF'
ELSE = 'ELSE'
ELIF = 'ELIF'
FOR = 'FOR'
DO = 'DO'
PRINT = 'PRINT'
INPUT = 'INPUT'
EOF = 'EOF'

KEYWORDS = {
    'end': END,
    'if': IF,
    'else': ELSE,
    'elif': ELIF,
    'for': FOR,
    'do': DO,
    'print': PRINT,
    'input': INPUT
}

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value
    
    def __str__(self):
        return f"Token({self.type}, {self.value})"
