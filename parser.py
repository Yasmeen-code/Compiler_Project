from tokens import NUMBER, PLUS, MINUS, MUL, DIV, GE, LE, LT, NE, INCREMENT, DECREMENT, LPAREN, RPAREN, LBRACE, RBRACE, ID, ASSIGN, END, COMMA, IF, ELSE, ELIF, FOR, DO, PRINT, INPUT, EOF

class TreeNode:
    def __init__(self, name, value=None):
        self.name = name
        self.value = value
        self.children = []
    
    def add(self, child):
        self.children.append(child)
    
    def print_tree(self, level=0):
        indent = "  " * level
        if self.value:
            result = f"{indent}{self.name}: {self.value}\n"
        else:
            result = f"{indent}{self.name}\n"
        
        for child in self.children:
            if isinstance(child, TreeNode):
                result += child.print_tree(level + 1)
            else:
                result += f"{indent}  {child}\n"
        return result

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[0]
        self.errors = []
    
    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.pos += 1
            if self.pos < len(self.tokens):
                self.current_token = self.tokens[self.pos]
        else:
            self.errors.append(f"Expected {token_type}, found {self.current_token.type}")
            self.pos += 1
            if self.pos < len(self.tokens):
                self.current_token = self.tokens[self.pos]
    
    def parse(self):
        tree = self.program()
        return tree, self.errors
    
    def program(self):
        node = TreeNode("Program")
        stmt_list = self.statement_list()
        node.add(stmt_list)
        return node
    
    def statement_list(self):
        node = TreeNode("StatementList")
        
        while self.current_token.type in (ID, NUMBER, LPAREN, IF, FOR, PRINT, INPUT):
            stmt = self.statement()
            node.add(stmt)
        
        return node
    
    def statement(self):
        node = TreeNode("Statement")
        
        if self.current_token.type == IF:
            node.add(TreeNode("Keyword", "if"))
            self.eat(IF)
            
            self.eat(LPAREN)
            
            cond_list = self.condition_list()
            node.add(cond_list)
            
            self.eat(RPAREN)
            
            if self.current_token.type == END:
                node.add(TreeNode("End", "end"))
                self.eat(END)
            else:
                self.errors.append("Expected 'end' after if condition")
            
            body = self.block()
            node.add(body)
            
            while self.current_token.type in (ELSE, ELIF):
                if self.current_token.type == ELIF:
                    elif_node = TreeNode("Elif")
                    self.eat(ELIF)
                    
                    self.eat(LPAREN)
                    cond = self.condition_list()
                    elif_node.add(cond)
                    self.eat(RPAREN)
                    
                    if self.current_token.type == END:
                        elif_node.add(TreeNode("End", "end"))
                        self.eat(END)
                    
                    elif_body = self.block()
                    elif_node.add(elif_body)
                    node.add(elif_node)
                
                elif self.current_token.type == ELSE:
                    else_node = TreeNode("Else")
                    self.eat(ELSE)
                    
                    if self.current_token.type == END:
                        else_node.add(TreeNode("End", "end"))
                        self.eat(END)
                    
                    else_body = self.block()
                    else_node.add(else_body)
                    node.add(else_node)
            
            if self.current_token.type == END:
                node.add(TreeNode("End", "end"))
                self.eat(END)
        
        elif self.current_token.type == FOR:
            node.add(TreeNode("Keyword", "for"))
            self.eat(FOR)
            
            self.eat(LPAREN)
            
            init = self.for_init()
            node.add(init)
            
            self.eat(COMMA)
            
            cond = self.condition()
            node.add(cond)
            
            self.eat(COMMA)
            
            update = self.for_update()
            node.add(update)
            
            self.eat(RPAREN)
            
            if self.current_token.type == END:
                node.add(TreeNode("End", "end"))
                self.eat(END)
            
            body = self.block()
            node.add(body)
            
            if self.current_token.type == END:
                node.add(TreeNode("End", "end"))
                self.eat(END)
        
        elif self.current_token.type == PRINT:
            node.add(TreeNode("Keyword", "print"))
            self.eat(PRINT)
            
            self.eat(LPAREN)
            
            if self.current_token.type == ID:
                node.add(TreeNode("Identifier", self.current_token.value))
                self.eat(ID)
            else:
                self.errors.append("Expected identifier in print")
            
            self.eat(RPAREN)
            
            if self.current_token.type == END:
                node.add(TreeNode("End", "end"))
                self.eat(END)
            else:
                self.errors.append("Expected 'end' after print")
        
        elif self.current_token.type == INPUT:
            node.add(TreeNode("Keyword", "input"))
            self.eat(INPUT)
            
            self.eat(LPAREN)
            
            if self.current_token.type == ID:
                node.add(TreeNode("Identifier", self.current_token.value))
                self.eat(ID)
            else:
                self.errors.append("Expected identifier in input")
            
            self.eat(RPAREN)
            
            if self.current_token.type == END:
                node.add(TreeNode("End", "end"))
                self.eat(END)
            else:
                self.errors.append("Expected 'end' after input")
        
        elif self.current_token.type == ID:
            id_node = TreeNode("Identifier", self.current_token.value)
            node.add(id_node)
            self.eat(ID)
            
            self.eat(ASSIGN)
            
            expr = self.expression()
            node.add(expr)
            
            if self.current_token.type == END:
                node.add(TreeNode("End", "end"))
                self.eat(END)
            else:
                self.errors.append("Expected 'end' after statement")
        
        else:
            expr = self.expression()
            node.add(expr)
            
            if self.current_token.type == END:
                node.add(TreeNode("End", "end"))
                self.eat(END)
            else:
                self.errors.append("Expected 'end' after statement")
        
        return node
    
    def block(self):
        node = TreeNode("Block")
        
        if self.current_token.type == LBRACE:
            self.eat(LBRACE)
            stmt_list = self.statement_list()
            node.add(stmt_list)
            self.eat(RBRACE)
        
        elif self.current_token.type == DO:
            self.eat(DO)
            stmt_list = self.statement_list()
            node.add(stmt_list)
            if self.current_token.type == END:
                self.eat(END)
        
        else:
            stmt = self.statement()
            node.add(stmt)
        
        return node
    
    def for_init(self):
        node = TreeNode("ForInit")
        
        if self.current_token.type == ID:
            node.add(TreeNode("Identifier", self.current_token.value))
            self.eat(ID)
        
        self.eat(ASSIGN)
        
        expr = self.expression()
        node.add(expr)
        
        return node
    
    def for_update(self):
        node = TreeNode("ForUpdate")
        
        if self.current_token.type == ID:
            node.add(TreeNode("Identifier", self.current_token.value))
            self.eat(ID)
            
            if self.current_token.type == INCREMENT:
                node.add(TreeNode("Operator", "++"))
                self.eat(INCREMENT)
            elif self.current_token.type == DECREMENT:
                node.add(TreeNode("Operator", "--"))
                self.eat(DECREMENT)
            else:
                self.errors.append("Expected ++ or -- in for update")
        
        return node
    
    def condition_list(self):
        node = TreeNode("ConditionList")
        
        cond = self.condition()
        node.add(cond)
        
        while self.current_token.type == COMMA:
            self.eat(COMMA)
            cond = self.condition()
            node.add(cond)
        
        return node
    
    def condition(self):
        node = TreeNode("Condition")
        
        if self.current_token.type != ID:
            self.errors.append("Expected identifier in condition")
            return node
        
        id_node = TreeNode("Identifier", self.current_token.value)
        node.add(id_node)
        self.eat(ID)
        
        if self.current_token.type == ASSIGN:
            node.add(TreeNode("Operator", "="))
            self.eat(ASSIGN)
            expr = self.expression()
            node.add(expr)
        
        elif self.current_token.type == GE:
            node.add(TreeNode("Operator", ">="))
            self.eat(GE)
            expr = self.expression()
            node.add(expr)
        
        elif self.current_token.type == LE:
            node.add(TreeNode("Operator", "<="))
            self.eat(LE)
            expr = self.expression()
            node.add(expr)
        
        elif self.current_token.type == LT:
            node.add(TreeNode("Operator", "<"))
            self.eat(LT)
            expr = self.expression()
            node.add(expr)
        
        elif self.current_token.type == NE:
            node.add(TreeNode("Operator", "!="))
            self.eat(NE)
            expr = self.expression()
            node.add(expr)
        
        elif self.current_token.type == INCREMENT:
            node.add(TreeNode("Operator", "++"))
            self.eat(INCREMENT)
        
        elif self.current_token.type == DECREMENT:
            node.add(TreeNode("Operator", "--"))
            self.eat(DECREMENT)
        
        else:
            self.errors.append(f"Invalid condition operator: {self.current_token.type}")
        
        return node
    
    def expression(self):
        node = TreeNode("Expression")
        
        term = self.term()
        node.add(term)
        
        while self.current_token.type in (PLUS, MINUS):
            op_node = TreeNode("Operator", self.current_token.value)
            node.add(op_node)
            
            if self.current_token.type == PLUS:
                self.eat(PLUS)
            else:
                self.eat(MINUS)
            
            term = self.term()
            node.add(term)
        
        return node
    
    def term(self):
        node = TreeNode("Term")
        
        factor = self.factor()
        node.add(factor)
        
        while self.current_token.type in (MUL, DIV):
            op_node = TreeNode("Operator", self.current_token.value)
            node.add(op_node)
            
            if self.current_token.type == MUL:
                self.eat(MUL)
            else:
                self.eat(DIV)
            
            factor = self.factor()
            node.add(factor)
        
        return node
    
    def factor(self):
        node = TreeNode("Factor")
        
        if self.current_token.type == NUMBER:
            num_node = TreeNode("Number", self.current_token.value)
            node.add(num_node)
            self.eat(NUMBER)
        
        elif self.current_token.type == ID:
            id_node = TreeNode("Identifier", self.current_token.value)
            node.add(id_node)
            self.eat(ID)
        
        elif self.current_token.type == LPAREN:
            node.add(TreeNode("LParen", "("))
            self.eat(LPAREN)
            
            expr = self.expression()
            node.add(expr)
            
            self.eat(RPAREN)
            node.add(TreeNode("RParen", ")"))
        
        else:
            self.errors.append(f"Unexpected {self.current_token.type}")
            self.eat(self.current_token.type)
        
        return node
