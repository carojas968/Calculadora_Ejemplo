"""Ventana, pantalla y botones de la calculadora."""

import tkinter as tk

import tema
from motor import Calculadora

# (texto del botón, tecla que envía, tipo de botón, columnas que ocupa)
DISENO = [
    [("C", "C", "funcion", 1), ("±", "±", "funcion", 1),
     ("%", "%", "funcion", 1), ("÷", "/", "operador", 1)],
    [("7", "7", "numero", 1), ("8", "8", "numero", 1),
     ("9", "9", "numero", 1), ("×", "*", "operador", 1)],
    [("4", "4", "numero", 1), ("5", "5", "numero", 1),
     ("6", "6", "numero", 1), ("−", "-", "operador", 1)],
    [("1", "1", "numero", 1), ("2", "2", "numero", 1),
     ("3", "3", "numero", 1), ("+", "+", "operador", 1)],
    [("0", "0", "numero", 2), (".", ".", "numero", 1),
     ("=", "=", "igual", 1)],
]

# Se muestran con símbolos matemáticos, pero el motor usa * y /
SIMBOLOS = {"*": "×", "/": "÷", "-": "−"}

TECLAS_VALIDAS = set("0123456789.+-*/=%C±⌫")

# Teclas del teclado que no son el carácter que escriben
MAPA_TECLADO = {
    "Return": "=", "KP_Enter": "=", "equal": "=",
    "BackSpace": "⌫", "Escape": "C", "Delete": "C",
    "period": ".", "KP_Decimal": ".", "comma": ".",
    "KP_Add": "+", "KP_Subtract": "-", "KP_Multiply": "*",
    "KP_Divide": "/", "x": "*", "X": "*", "c": "C",
}


class BotonRedondeado(tk.Canvas):
    """Botón con esquinas redondeadas que cambia de color al pasar el cursor."""

    def __init__(self, padre, texto, tipo, comando):
        super().__init__(padre, bd=0, highlightthickness=0,
                         bg=tema.FONDO, cursor="hand2")
        self.texto = texto
        self.colores = tema.COLORES_BOTON[tipo]
        self.comando = comando
        self._estado = "normal"

        self.bind("<Configure>", lambda evento: self._dibujar())
        self.bind("<Enter>", lambda evento: self._cambiar_estado("hover"))
        self.bind("<Leave>", lambda evento: self._cambiar_estado("normal"))
        self.bind("<ButtonPress-1>", lambda evento: self._cambiar_estado("pulsado"))
        self.bind("<ButtonRelease-1>", self._al_soltar)

    def _cambiar_estado(self, estado):
        self._estado = estado
        self._dibujar()

    def _al_soltar(self, evento):
        # Solo se ejecuta si el cursor sigue sobre el botón
        if self._estado == "pulsado":
            self._cambiar_estado("hover")
            self.comando()

    def _dibujar(self):
        self.delete("all")
        ancho, alto = self.winfo_width(), self.winfo_height()
        if ancho < 2 or alto < 2:
            return
        radio = min(tema.RADIO_BOTON, ancho // 2, alto // 2)
        self._rectangulo_redondeado(2, 2, ancho - 2, alto - 2, radio,
                                    self.colores[self._estado])
        tamano = max(12, min(26, alto // 3))
        self.create_text(ancho // 2, alto // 2, text=self.texto,
                         fill=self.colores["texto"],
                         font=(tema.FUENTE, tamano, "bold"))

    def _rectangulo_redondeado(self, x1, y1, x2, y2, r, color):
        puntos = [
            x1 + r, y1, x2 - r, y1, x2, y1, x2, y1 + r,
            x2, y2 - r, x2, y2, x2 - r, y2, x1 + r, y2,
            x1, y2, x1, y2 - r, x1, y1 + r, x1, y1,
        ]
        self.create_polygon(puntos, smooth=True, fill=color, outline=color)


class Aplicacion(tk.Tk):
    """Ventana principal de la calculadora."""

    def __init__(self):
        super().__init__()
        self.title("Calculadora")
        self.configure(bg=tema.FONDO)
        self.geometry("380x580")
        self.minsize(320, 480)

        self.calc = Calculadora()
        self._crear_pantalla()
        self._crear_botones()
        self.bind("<Key>", self._al_teclear)
        self.actualizar_pantalla()

    def _crear_pantalla(self):
        marco = tk.Frame(self, bg=tema.PANTALLA)
        marco.pack(fill="x", padx=tema.ESPACIO * 2, pady=(tema.ESPACIO * 2, tema.ESPACIO))

        self.lbl_expresion = tk.Label(marco, anchor="e", bg=tema.PANTALLA,
                                      fg=tema.TEXTO_SECUNDARIO,
                                      font=(tema.FUENTE, 13))
        self.lbl_expresion.pack(fill="x", padx=16, pady=(14, 0))

        self.lbl_resultado = tk.Label(marco, anchor="e", bg=tema.PANTALLA,
                                      fg=tema.TEXTO)
        self.lbl_resultado.pack(fill="x", padx=16, pady=(0, 16))

    def _crear_botones(self):
        cuadricula = tk.Frame(self, bg=tema.FONDO)
        cuadricula.pack(fill="both", expand=True,
                        padx=tema.ESPACIO * 2, pady=(0, tema.ESPACIO * 2))

        for columna in range(4):
            cuadricula.columnconfigure(columna, weight=1, uniform="columna")

        for fila_numero, fila in enumerate(DISENO):
            cuadricula.rowconfigure(fila_numero, weight=1, uniform="fila")
            columna = 0
            for texto, tecla, tipo, columnas in fila:
                boton = BotonRedondeado(
                    cuadricula, texto, tipo,
                    comando=lambda tecla=tecla: self.pulsar(tecla),
                )
                boton.grid(row=fila_numero, column=columna, columnspan=columnas,
                           sticky="nsew", padx=tema.ESPACIO // 2,
                           pady=tema.ESPACIO // 2)
                columna += columnas

    def _al_teclear(self, evento):
        tecla = MAPA_TECLADO.get(evento.keysym, evento.char)
        self.pulsar(tecla)

    def pulsar(self, tecla):
        if tecla not in TECLAS_VALIDAS:
            return
        if tecla in "0123456789":
            self.calc.ingresar_digito(tecla)
        elif tecla == ".":
            self.calc.ingresar_decimal()
        elif tecla in ("+", "-", "*", "/"):
            self.calc.aplicar_operador(tecla)
        elif tecla == "=":
            self.calc.igual()
        elif tecla == "C":
            self.calc.limpiar()
        elif tecla == "±":
            self.calc.cambiar_signo()
        elif tecla == "%":
            self.calc.porcentaje()
        elif tecla == "⌫":
            self.calc.borrar()
        self.actualizar_pantalla()

    def actualizar_pantalla(self):
        expresion = self.calc.expresion
        for original, simbolo in SIMBOLOS.items():
            expresion = expresion.replace(original, simbolo)
        self.lbl_expresion.config(text=expresion)

        texto = self.calc.pantalla
        # Reduce el tamaño de la letra cuando el número es largo
        if len(texto) <= 8:
            tamano = 44
        elif len(texto) <= 12:
            tamano = 34
        else:
            tamano = 26
        color = tema.TEXTO_ERROR if self.calc.hay_error else tema.TEXTO
        self.lbl_resultado.config(text=texto, fg=color,
                                  font=(tema.FUENTE, tamano, "bold"))
