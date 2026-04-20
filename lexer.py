# lexer.py
from tokens import Token, NUMBER, PLUS, MINUS, MUL, DIV, GE, LE, LT, NE, INCREMENT, DECREMENT, LPAREN, RPAREN, LBRACE, RBRACE, ID, ASSIGN, END, COMMA, IF, ELSE, ELIF, FOR, IN, TO, DO, PRINT, INPUT, EOF, KEYWORDS

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if text else None
    
    def advance(self):
        self.pos += 1
        if self.pos >= len(self.text):
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]
    
    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos >= len(self.text):
            return None
        return self.text[peek_pos]
    
    def skip_spaces(self):
        while self.current_char is not None and self.current_char in ' \t\n\r':
            self.advance()
    
    def read_number(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        
        if self.current_char == '.':
            result += self.current_char
            self.advance()
            while self.current_char is not None and self.current_char.isdigit():
                result += self.current_char
                self.advance()
        
        return Token(NUMBER, result)
    
    def read_word(self):
        result = ''
        while (self.current_char is not None and 
               (self.current_char.isalpha() or self.current_char.isdigit() or self.current_char == '_')):
            result += self.current_char
            self.advance()
        
        token_type = KEYWORDS.get(result.lower(), ID)
        return Token(token_type, result)
    
    def next_token(self):
        while self.current_char is not None:
            
            if self.current_char in ' \t\n\r':
                self.skip_spaces()
                continue
            
            if self.current_char.isdigit():
                return self.read_number()
            
            if self.current_char.isalpha():
                return self.read_word()
            
            # >=
            if self.current_char == '>':
                if self.peek() == '=':
                    self.advance()
                    self.advance()
                    return Token(GE, '>=')
                else:
                    self.advance()
                    return Token(LT, '>')  # نستخدم LT كـ greater than مؤقتاً أو نضيف GT
            
            # <=
            if self.current_char == '<':
                if self.peek() == '=':
                    self.advance()
                    self.advance()
                    return Token(LE, '<=')
                else:
                    self.advance()
                    return Token(LT, '<')
            
            # != أو <>
            if self.current_char == '!':
                if self.peek() == '=':
                    self.advance()
                    self.advance()
                    return Token(NE, '!=')
                else:
                    raise Exception(f"Error: Unknown character '!' (did you mean != ?)")
            
            if self.current_char == '<':
                if self.peek() == '>':
                    self.advance()
                    self.advance()
                    return Token(NE, '<>')
            
            # ++
            if self.current_char == '+':
                if self.peek() == '+':
                    self.advance()
                    self.advance()
                    return Token(INCREMENT, '++')
                else:
                    self.advance()
                    return Token(PLUS, '+')
            
            # --
            if self.current_char == '-':
                if self.peek() == '-':
                    self.advance()
                    self.advance()
                    return Token(DECREMENT, '--')
                else:
                    self.advance()
                    return Token(MINUS, '-')
            
            if self.current_char == '*':
                self.advance()
                return Token(MUL, '*')
            
            if self.current_char == '/':
                self.advance()
                return Token(DIV, '/')
            
            if self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(')
            
            if self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')
            
            if self.current_char == '{':
                self.advance()
                return Token(LBRACE, '{')
            
            if self.current_char == '}':
                self.advance()
                return Token(RBRACE, '}')
            
            if self.current_char == '=':
                self.advance()
                return Token(ASSIGN, '=')
            
            if self.current_char == ',':
                self.advance()
                return Token(COMMA, ',')
            
            raise Exception(f"Error: Unknown character '{self.current_char}'")
        
        return Token(EOF, None)
    
    def get_all_tokens(self):
        tokens = []
        while True:
            token = self.next_token()
            tokens.append(token)
            if token.type == EOF:
                break
        return tokens