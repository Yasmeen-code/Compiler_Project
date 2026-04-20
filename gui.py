# gui.py
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

from lexer import Lexer
from parser import Parser


class CompilerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Compiler Project 2026")
        self.root.geometry("900x700")
        
        # Input Frame
        input_frame = tk.LabelFrame(root, text="Source Code", padx=10, pady=10)
        input_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.code_input = tk.Text(input_frame, height=6, width=80, font=('Courier', 11))
        self.code_input.pack(fill=tk.X)
        
        # Example code
        example = """x = 5 + 3 end
if ( x = 0 , y >= 10 , z ++ ) end
print ( result ) end 
if ( x = 0 ) end
    print ( zero ) end
else end
    print ( not_zero ) end
end
for ( i = 0 , i < 10 , i ++ ) end
    print ( i ) end
end
if ( x = 0 ) end
    y = 1 end
elif ( x = 1 ) end
    y = 2 end
else end
    y = 3 end
end"""
        self.code_input.insert("1.0", example)
        
        # Button
        tk.Button(root, text="Compile", command=self.compile, 
                 font=('Arial', 12), bg='#4CAF50', fg='white', 
                 width=20, height=2).pack(pady=10)
        
        # Results Frame
        results_frame = tk.Frame(root)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Left: Tokens Table
        token_frame = tk.LabelFrame(results_frame, text="Lexical Analysis (Tokens)", width=400)
        token_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        columns = ('Token Value', 'Token Type')
        self.token_tree = ttk.Treeview(token_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.token_tree.heading(col, text=col)
            self.token_tree.column(col, width=150)
        
        scrollbar = ttk.Scrollbar(token_frame, orient=tk.VERTICAL, command=self.token_tree.yview)
        self.token_tree.configure(yscrollcommand=scrollbar.set)
        
        self.token_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Right: Parse Tree
        tree_frame = tk.LabelFrame(results_frame, text="Parse Tree / Errors", width=400)
        tree_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        self.tree_text = scrolledtext.ScrolledText(tree_frame, wrap=tk.WORD, font=('Courier', 10))
        self.tree_text.pack(fill=tk.BOTH, expand=True)
    
    def compile(self):
        # Clear previous results
        for item in self.token_tree.get_children():
            self.token_tree.delete(item)
        self.tree_text.delete("1.0", tk.END)
        
        code = self.code_input.get("1.0", tk.END).strip()
        if not code:
            messagebox.showwarning("Warning", "Please enter some code!")
            return
        
        try:
            # Phase 1: Lexical Analysis
            lexer = Lexer(code)
            tokens = lexer.get_all_tokens()
            
            # Fill token table
            for token in tokens:
                self.token_tree.insert('', tk.END, values=(token.value, token.type))
            
            # Phase 2: Syntax Analysis
            parser = Parser(tokens)
            tree, errors = parser.parse()
            
            # Display parse tree
            self.tree_text.insert(tk.END, "=== PARSE TREE ===\n\n")
            self.tree_text.insert(tk.END, tree.print_tree())
            
            # Display errors if any
            if errors:
                self.tree_text.insert(tk.END, "\n\n=== ERRORS ===\n")
                for err in errors:
                    self.tree_text.insert(tk.END, f"- {err}\n")
            else:
                self.tree_text.insert(tk.END, "\n\n✓ No syntax errors!")
            
        except Exception as e:
            self.tree_text.insert(tk.END, f"Error: {str(e)}")


def main():
    root = tk.Tk()
    app = CompilerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()