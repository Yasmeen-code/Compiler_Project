import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

from lexer import Lexer
from parser import Parser
from examples import examples, get_example_names


class CompilerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Compiler Project 2026")
        self.root.geometry("1000x750")
        
        examples_frame = tk.LabelFrame(root, text="Quick Examples", padx=5, pady=5)
        examples_frame.pack(fill=tk.X, padx=10, pady=5)
        
        row_frame = tk.Frame(examples_frame)
        row_frame.pack(fill=tk.X)
        
        for i, name in enumerate(get_example_names()):
            short_name = name.replace("Example ", "Ex").replace("ERROR", "Err")
            btn = tk.Button(row_frame, text=short_name, 
                          command=lambda n=name: self.load_example(n),
                          font=('Arial', 8), width=12)
            btn.pack(side=tk.LEFT, padx=2, pady=2)
            
            if (i + 1) % 6 == 0:
                row_frame = tk.Frame(examples_frame)
                row_frame.pack(fill=tk.X)
        
        input_frame = tk.LabelFrame(root, text="Source Code", padx=10, pady=10)
        input_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.code_input = tk.Text(input_frame, height=8, width=80, font=('Courier', 11))
        self.code_input.pack(fill=tk.X)
        
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=5)
        
        tk.Button(btn_frame, text="Compile", command=self.compile, 
                 font=('Arial', 12), bg='#4CAF50', fg='white', 
                 width=15, height=2).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="Clear", command=self.clear, 
                 font=('Arial', 12), bg='#f44336', fg='white',
                 width=15, height=2).pack(side=tk.LEFT, padx=5)
        
        results_frame = tk.Frame(root)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
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
        
        tree_frame = tk.LabelFrame(results_frame, text="Parse Tree / Errors", width=400)
        tree_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        self.tree_text = scrolledtext.ScrolledText(tree_frame, wrap=tk.WORD, font=('Courier', 10))
        self.tree_text.pack(fill=tk.BOTH, expand=True)
    
    def load_example(self, name):
        self.code_input.delete("1.0", tk.END)
        self.code_input.insert("1.0", examples[name])
    
    def clear(self):
        self.code_input.delete("1.0", tk.END)
        for item in self.token_tree.get_children():
            self.token_tree.delete(item)
        self.tree_text.delete("1.0", tk.END)
    
    def compile(self):
        for item in self.token_tree.get_children():
            self.token_tree.delete(item)
        self.tree_text.delete("1.0", tk.END)
        
        code = self.code_input.get("1.0", tk.END).strip()
        if not code:
            messagebox.showwarning("Warning", "Please enter some code!")
            return
        
        try:
            lexer = Lexer(code)
            tokens = lexer.get_all_tokens()
            
            for token in tokens:
                self.token_tree.insert('', tk.END, values=(token.value, token.type))
            
            parser = Parser(tokens)
            tree, errors = parser.parse()
            
            self.tree_text.insert(tk.END, "=== PARSE TREE ===\n\n")
            self.tree_text.insert(tk.END, tree.print_tree())
            
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
