# Calculadora

Calculadora de escritorio con interfaz gráfica, hecha en Python con `tkinter`.
Incluye operaciones básicas, porcentaje, cambio de signo, borrado y soporte de teclado.

## Requisitos

- Python 3.10 o superior (con `tkinter`, que viene incluido en la instalación estándar de Python para Windows).
- No necesita librerías externas.

## Cómo ejecutarla

Desde la carpeta del proyecto:

```bash
python main.py
```

## Uso

| Acción | Botón | Teclado |
|---|---|---|
| Números y punto decimal | `0`–`9`, `.` | `0`–`9`, `.` o `,` |
| Sumar, restar, multiplicar, dividir | `+`, `−`, `×`, `÷` | `+`, `-`, `*`, `/` |
| Calcular resultado | `=` | `Enter` o `=` |
| Porcentaje | `%` | `%` |
| Cambiar signo | `±` | — |
| Borrar último dígito | — | `Retroceso` (Backspace) |
| Borrar todo | `C` | `Esc`, `Supr` o `C` |

Las operaciones se evalúan **de izquierda a derecha**, sin respetar la precedencia de operadores.
Por ejemplo, `2 + 3 × 4 =` da `20`, no `14`.

### Límites

- Se pueden teclear hasta 12 dígitos.
- Los resultados se muestran con hasta 16 dígitos y se redondean a 10 decimales (`1 ÷ 3 = 0.3333333333`).
- Si el resultado es demasiado grande, muestra `Desbordamiento`.
- Dividir entre cero muestra un mensaje de error. Pulsa `C` para continuar.

## Estructura del proyecto

```
calculadora/
├── main.py          # Punto de entrada: arranca la ventana
├── motor.py         # Lógica de la calculadora (sin interfaz gráfica)
├── interfaz.py      # Ventana, pantalla, botones y teclado
├── tema.py          # Colores, fuente y medidas visuales
└── tests/
    └── test_motor.py  # Pruebas automáticas de la lógica
```

La separación es intencional: `motor.py` no depende de `tkinter`, así que se puede probar sin abrir la ventana.
Para cambiar el aspecto (colores, fuente, tamaños), basta con editar `tema.py`.

## Pruebas

Desde la carpeta del proyecto:

```bash
python -m unittest discover -s tests -t . -v
```

Actualmente hay 17 pruebas que cubren suma, división, errores, porcentaje, borrado y límites de dígitos.

## Mejoras pendientes

- Respetar la precedencia de operadores (`×` y `÷` antes que `+` y `−`).
- Añadir pruebas para la interfaz (`interfaz.py`) y para el teclado.
- Añadir un archivo `.gitignore` que excluya `__pycache__/`.
- Añadir un historial de operaciones.
