"""Punto de entrada de la calculadora. Ejecutar con: python main.py"""

import ctypes

from interfaz import Aplicacion


def activar_escalado_windows():
    """Evita que la ventana se vea borrosa con escalado de pantalla en Windows."""
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except (AttributeError, OSError):
        pass


if __name__ == "__main__":
    activar_escalado_windows()
    Aplicacion().mainloop()
