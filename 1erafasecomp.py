import re
import tkinter as tk
from tkinter import filedialog, scrolledtext

TOKEN_REGEX = [
    (r'\b(int|double|float|char|boolean|void|class|public|private|protected|static|final|new|try|catch|finally|throw|throws|extends|implements|import|package)\b', 'KEYWORD'),
    (r'\b(if|else|while|for|do|switch|case|default|break|continue|return)\b', 'KEYWORD'),
    (r'\b(true|false|null)\b', 'LITERAL'),
    (r'\".*?\"', 'STRING'),
    (r'//.*', 'COMMENT'),
    (r'/\*[\s\S]*?\*/', 'COMMENT'),
    (r'\b\d+\b', 'NUMBER'),
    (r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', 'IDENTIFIER'),
    (r'[+\-*/=<>!&|%^~]', 'OPERATOR'),
    (r'[\(\){}\[\];,\.]', 'DELIMITER'),
    (r'\s+', None),
]

def lexer(code):
    tokens = []
    while code:
        match = None
        for regex, token_type in TOKEN_REGEX:
            match = re.match(regex, code)
            if match:
                lexeme = match.group(0)
                if token_type:
                    tokens.append((token_type, lexeme))
                code = code[len(lexeme):]
                break
        if not match:
            tokens.append(('UNKNOWN', code[0]))
            code = code[1:]
    return tokens

def analyze_code():
    code = text_area.get("1.0", tk.END).strip()
    tokens = lexer(code)
    display_tokens(tokens)

def load_file():
    file_path = filedialog.askopenfilename(filetypes=[("Java Files", "*.java")])
    if file_path:
        with open(file_path, "r", encoding="utf-8") as file:
            code = file.read()
            text_area.delete("1.0", tk.END)
            text_area.insert(tk.END, code)
            tokens = lexer(code)
            display_tokens(tokens)

def display_tokens(tokens):
    result_area.config(state=tk.NORMAL)
    result_area.delete("1.0", tk.END)
    result_area.insert(tk.END, "Tipo de Token\t\tValores\n")
    result_area.insert(tk.END, "" * 30 + "\n")
    for token_type, lexeme in tokens:
        result_area.insert(tk.END, f"{token_type}\t\t{lexeme}\n")
    result_area.config(state=tk.DISABLED)

root = tk.Tk()
root.title("Analizador Léxico - Java")

text_area = scrolledtext.ScrolledText(root, width=60, height=15)
text_area.pack(pady=10)

button_frame = tk.Frame(root)
button_frame.pack()

analyze_button = tk.Button(button_frame, text="Analizar Código", command=analyze_code)
analyze_button.grid(row=0, column=0, padx=5)

load_button = tk.Button(button_frame, text="Cargar Archivo", command=load_file)
load_button.grid(row=0, column=1, padx=5)

result_area = scrolledtext.ScrolledText(root, width=60, height=15, state=tk.DISABLED)
result_area.pack(pady=10)

tk.mainloop()