# tokens.py

NUMBER = 'NUMBER'
PLUS = 'PLUS'
MINUS = 'MINUS'
MUL = 'MUL'
DIV = 'DIV'
GE = 'GE'
LE = 'LE'            # جديد: <=
INCREMENT = 'INCR'
DECREMENT = 'DECR'
LT = 'LT'            # جديد: <
NE = 'NE'            # جديد: != أو <>
LPAREN = 'LPAREN'
RPAREN = 'RPAREN'
LBRACE = 'LBRACE'    # جديد: {
RBRACE = 'RBRACE'    # جديد: }
ID = 'ID'
ASSIGN = 'ASSIGN'
END = 'END'
COMMA = 'COMMA'
IF = 'IF'
ELSE = 'ELSE'        # جديد
ELIF = 'ELIF'        # جديد
FOR = 'FOR'          # جديد
IN = 'IN'            # جديد: for i in range
TO = 'TO'            # جديد: for i = 1 to 10
DO = 'DO'            # جديد: بديل لـ {
PRINT = 'PRINT'
INPUT = 'INPUT'      # جديد
EOF = 'EOF'

KEYWORDS = {
    'end': END,
    'if': IF,
    'else': ELSE,     # جديد
    'elif': ELIF,     # جديد
    'for': FOR,       # جديد
    'in': IN,         # جديد
    'to': TO,         # جديد
    'do': DO,         # جديد
    'print': PRINT,
    'input': INPUT    # جديد
}

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value
    
    def __str__(self):
        return f"Token({self.type}, {self.value})"