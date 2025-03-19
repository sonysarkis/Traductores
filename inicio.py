import tkinter as tk
import subprocess

class PantallaInicio:
    def __init__(self, root):
        self.root = root
        self.root.title("Pantalla de Inicio")
        self.root.geometry("400x300")

        tk.Label(self.root, text="Analizador Léxico y Sintáctico", font=("Arial", 14, "bold")).pack(pady=20)
        tk.Label(self.root, text="Desarrollado por Sony Gómez y Enrique González", font=("Arial", 10)).pack(pady=5)

        btn_lexico = tk.Button(self.root, text="Ir al Analizador Léxico", command=self.abrir_lexico)
        btn_lexico.pack(pady=10)
        
        btn_sintactico = tk.Button(self.root, text="Ir al Analizador Sintáctico", command=self.abrir_sintactico)
        btn_sintactico.pack(pady=10)
    
    def abrir_lexico(self):
        subprocess.run(["python", "1erafasecomp.py"])
    
    def abrir_sintactico(self):
        subprocess.run(["python", "sintactico.py"])

if __name__ == "__main__":
    root = tk.Tk()
    app = PantallaInicio(root)
    root.mainloop()
