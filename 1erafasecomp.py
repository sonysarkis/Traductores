import re  # trabaja con expresiones regulares
import tkinter as tk  # crea interfaces gráficas
from tkinter import filedialog, scrolledtext  # Widgets específicos de Tkinter

# Definición de tokens para el lenguaje Java usando expresiones regulares
TOKEN_REGEX = [
    (r'\b(int|double|float|char|boolean|void|class|public|private|protected|static|final|new|try|catch|finally|throw|throws|extends|implements|import|package)\b', 'KEYWORD'),  # Palabras clave de Java
    (r'\b(if|else|while|for|do|switch|case|default|break|continue|return)\b', 'KEYWORD'),  # Condicionales y estructuras de control
    (r'\b(true|false|null)\b', 'LITERAL'),  # Literales booleanos y null
    (r'\".*?\"', 'STRING'),  # Cadenas de texto entre comillas dobles
    (r'//.*', 'COMMENT'),  # Comentarios de una línea
    (r'/\*[\s\S]*?\*/', 'COMMENT'),  # Comentarios multilínea
    (r'\b\d+\b', 'NUMBER'),  # Números enteros
    (r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', 'IDENTIFIER'),  # Identificadores (nombres de variables, clases, etc.)
    (r'[+\-*/=<>!&|%^~]', 'OPERATOR'),  # Operadores matemáticos y lógicos
    (r'[\(\){}\[\];,\.]', 'DELIMITER'),  # Delimitadores como paréntesis, llaves y punto y coma
    (r'\s+', None),  # Ignorar espacios en blanco
]

def lexer(code):
    """ Analiza el código y devuelve una lista de tokens encontrados. """
    tokens = []  # Lista para almacenar los tokens encontrados
    while code:
        match = None  # Variable para almacenar la coincidencia de un token
        for regex, token_type in TOKEN_REGEX:  # Recorrer todas las expresiones regulares definidas
            match = re.match(regex, code)  # Comparar el patrón con el inicio del código fuente
            if match:  # Si hay coincidencia, procesar el token encontrado
                lexeme = match.group(0)  # Obtener el texto del token
                if token_type:  # Verificar si el token tiene un tipo válido
                    tokens.append((lexeme, token_type))  # Agregar el token a la lista
                code = code[len(lexeme):]  # Avanzar en el código eliminando el token analizado
                break  # Salir del bucle una vez encontrado un token válido
        if not match:  # Si no hay coincidencia, marcar el carácter como desconocido
            tokens.append((code[0], 'UNKNOWN'))
            code = code[1:]  # Avanzar al siguiente carácter
    return tokens  # Retornar la lista de tokens analizados

def analyze_code():
    """ Analiza el código ingresado en el área de texto. """
    code = text_area.get("1.0", tk.END)  # Obtener el texto ingresado en la interfaz
    tokens = lexer(code)  # Ejecutar el analizador léxico
    display_tokens(tokens)  # Mostrar los resultados en la interfaz

def load_file():
    """ Permite cargar un archivo .java y analizar su contenido. """
    file_path = filedialog.askopenfilename(filetypes=[("Archivos Java", "*.java")])  # Abrir diálogo para seleccionar un archivo
    if file_path:  # Verificar si se seleccionó un archivo
        with open(file_path, "r", encoding="utf-8") as file:  # Abrir el archivo en modo lectura
            code = file.read()  # Leer el contenido del archivo
            text_area.delete("1.0", tk.END)  # Limpiar el área de texto
            text_area.insert(tk.END, code)  # Insertar el contenido del archivo en el área de texto
            tokens = lexer(code)  # Ejecutar el analizador léxico
            display_tokens(tokens)  # Mostrar los resultados en la interfaz

def display_tokens(tokens):
    """ Muestra los tokens en el área de resultados. """
    result_area.config(state=tk.NORMAL)  # Habilitar el área de resultados para modificar el contenido
    result_area.delete("1.0", tk.END)  # Limpiar el área de resultados antes de mostrar nuevos datos
    result_area.insert(tk.END, f"{'Lexema':<20} {'Tipo de Token':<15}\n")  # Encabezados de las columnas
    result_area.insert(tk.END, f"{'-'*20} {'-'*15}\n")  # Línea separadora
    for lexeme, token_type in tokens:  # Recorrer la lista de tokens generados
        result_area.insert(tk.END, f"{lexeme:<20} {token_type:<15}\n")  # Mostrar cada token en una nueva línea
    result_area.config(state=tk.DISABLED)  # Deshabilitar el área de resultados para que no se pueda modificar manualmente

# Configuración de la interfaz gráfica
root = tk.Tk()  # Crear la ventana principal
root.title("Analizador Léxico - Java")  # Título de la ventana

# Crear un marco principal para organizar los widgets
main_frame = tk.Frame(root)
main_frame.pack(padx=10, pady=10)

# Configurar el gestor de geometría grid para el marco principal
main_frame.grid_rowconfigure(0, weight=1)
main_frame.grid_columnconfigure(0, weight=1)
main_frame.grid_columnconfigure(1, weight=1)

# Área de entrada de código
text_area_label = tk.Label(main_frame, text="Código Fuente:")
text_area_label.grid(row=0, column=0, sticky='w')
text_area = scrolledtext.ScrolledText(main_frame, width=60, height=20)
text_area.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')

# Área de resultados
result_area_label = tk.Label(main_frame, text="Resultados del Análisis:")
result_area_label.grid(row=0, column=1, sticky='w')
result_area = scrolledtext.ScrolledText(main_frame, width=60, height=20, state=tk.DISABLED)
result_area.grid(row=1, column=1, padx=5, pady=5, sticky='nsew')

# Botones para analizar y cargar archivo
button_frame = tk.Frame(main_frame)
button_frame.grid(row=2, column=0, columnspan=2, pady=5)

analyze_button = tk.Button(button_frame, text="Analizar Código", command=analyze_code)
analyze_button.pack(side=tk.LEFT, padx=5)

load_button = tk.Button(button_frame, text="Cargar Archivo", command=load_file)
load_button.pack(side=tk.LEFT, padx=5)

# Ejecutar la aplicación
root.mainloop()

 
