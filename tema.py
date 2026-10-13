"""Colores, fuentes y medidas de la interfaz.

Para cambiar el aspecto de la calculadora basta con editar este archivo.
"""

FUENTE = "Segoe UI"

FONDO = "#1E1E2E"
PANTALLA = "#11111B"
TEXTO = "#CDD6F4"
TEXTO_SECUNDARIO = "#7F849C"
TEXTO_ERROR = "#F38BA8"

# Cada tipo de botón tiene un color para reposo, para el cursor encima
# y para cuando se presiona.
COLORES_BOTON = {
    "numero": {
        "normal": "#313244", "hover": "#3E3F55", "pulsado": "#4B4D66",
        "texto": "#CDD6F4",
    },
    "funcion": {
        "normal": "#45475A", "hover": "#55576D", "pulsado": "#63657E",
        "texto": "#89B4FA",
    },
    "operador": {
        "normal": "#FAB387", "hover": "#FBC4A0", "pulsado": "#E8A070",
        "texto": "#1E1E2E",
    },
    "igual": {
        "normal": "#A6E3A1", "hover": "#B9EFB4", "pulsado": "#8FCB8A",
        "texto": "#1E1E2E",
    },
}

RADIO_BOTON = 18
ESPACIO = 8
