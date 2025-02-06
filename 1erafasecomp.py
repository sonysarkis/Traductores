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
    file_path = filedialog.askopenfilename(filetypes=[("Java Files", "*.java")])  # Abrir diálogo para seleccionar un archivo
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
    for lexeme, token_type in tokens:  # Recorrer la lista de tokens generados
        result_area.insert(tk.END, f"{lexeme} → {token_type}\n")  # Mostrar cada token en una nueva línea
    result_area.config(state=tk.DISABLED)  # Deshabilitar el área de resultados para que no se pueda modificar manualmente

#  interfaz gráfica
root = tk.Tk()  # ventana principal
root.title("Analizador Léxico - Java")  
# Área de entrada de código
text_area = scrolledtext.ScrolledText(root, width=60, height=15)  # Crear un área de texto con barra de desplazamiento
text_area.pack(pady=10)  # Agregar el área de texto con un margen vertical

# Botones para analizar y cargar archivo
button_frame = tk.Frame(root)  # Crear un contenedor para los botones
button_frame.pack()  # Agregar el contenedor a la ventana principal

analyze_button = tk.Button(button_frame, text="Analizar Código", command=analyze_code)  # Botón para analizar código ingresado
analyze_button.grid(row=0, column=0, padx=5)  #  botón con un margen horizontal

load_button = tk.Button(button_frame, text="Cargar Archivo", command=load_file)  # Botón para cargar un archivo .java
load_button.grid(row=0, column=1, padx=5)  #  botón con un margen horizontal

# Área de resultados
result_area = scrolledtext.ScrolledText(root, width=60, height=15, state=tk.DISABLED)  # Crear un área de texto para mostrar los tokens
result_area.pack(pady=10)  #  margen vertical

# Ejecutar la interfaz
tk.mainloop()  # Iniciar el bucle principal de la interfaz gráfica
