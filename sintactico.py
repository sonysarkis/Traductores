import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import javalang

class AnalizadorSintactico:
    def __init__(self, root):
        self.root = root
        self.root.title("Analizador Sintáctico")
        self.root.geometry("600x400")

        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=70, height=15)
        self.text_area.pack(pady=10)

        btn_frame = tk.Frame(self.root)
        btn_frame.pack()

        self.load_button = tk.Button(btn_frame, text="Cargar Archivo .java", command=self.cargar_archivo)
        self.load_button.pack(side=tk.LEFT, padx=5)

        self.analyze_button = tk.Button(btn_frame, text="Analizar Código", command=self.analizar_codigo)
        self.analyze_button.pack(side=tk.LEFT, padx=5)
    
    def cargar_archivo(self):
        file_path = filedialog.askopenfilename(filetypes=[("Archivos Java", "*.java")])
        if file_path:
            with open(file_path, "r", encoding="utf-8") as file:
                contenido = file.read()
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, contenido)

    def analizar_codigo(self):
        codigo = self.text_area.get(1.0, tk.END).strip()
        if not codigo:
            messagebox.showerror("Error", "El código está vacío")
            return
        
        try:
            javalang.parse.parse(codigo)
            messagebox.showinfo("Resultado del Análisis", "El código Java es sintácticamente correcto.")
        except javalang.parser.JavaSyntaxError as e:
            posicion = getattr(e, "at", None)
            if isinstance(posicion, tuple) and len(posicion) == 2:
                resultado = f"Error de sintaxis en línea {posicion[0]}, columna {posicion[1]}: {e}"
            else:
                resultado = f"Error de sintaxis: {e}"
            messagebox.showerror("Error de Sintaxis", resultado)
        except Exception as e:
            resultado = f"Error desconocido: {e}"
            messagebox.showerror("Error", resultado)

if __name__ == "__main__":
    root = tk.Tk()
    app = AnalizadorSintactico(root)
    root.mainloop()
