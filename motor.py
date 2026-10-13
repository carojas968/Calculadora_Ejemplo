"""Lógica de la calculadora, sin dependencias de la interfaz gráfica."""

from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

MAX_DIGITOS_ENTRADA = 12    # dígitos que el usuario puede teclear
MAX_DIGITOS_PANTALLA = 16   # dígitos máximos que se muestran en pantalla
PRECISION_RESULTADO = Decimal("1e-10")
OPERADORES = ("+", "-", "*", "/")


class ErrorCalculo(Exception):
    """Operación que no se puede realizar, por ejemplo dividir entre cero."""


class Calculadora:
    """Guarda el estado de la calculadora y reacciona a cada tecla pulsada."""

    def __init__(self):
        self.limpiar()

    @property
    def pantalla(self):
        """Número o mensaje de error que se debe mostrar."""
        return self._error if self.hay_error else self._entrada

    @property
    def expresion(self):
        """Operación pendiente, por ejemplo '12 +'. Vacía si no hay ninguna."""
        if self._operador is None:
            return ""
        return f"{_formatear(self._acumulado)} {self._operador}"

    @property
    def hay_error(self):
        return self._error is not None

    def limpiar(self):
        self._entrada = "0"
        self._acumulado = None
        self._operador = None
        self._nueva_entrada = False
        self._error = None

    def ingresar_digito(self, digito):
        if len(digito) != 1 or digito not in "0123456789":
            raise ValueError(f"Dígito no válido: {digito!r}")
        if self.hay_error:
            return
        if self._nueva_entrada:
            self._entrada = digito
            self._nueva_entrada = False
        elif self._entrada == "0":
            self._entrada = digito
        elif self._cifras() < MAX_DIGITOS_ENTRADA:
            self._entrada += digito

    def ingresar_decimal(self):
        if self.hay_error:
            return
        if self._nueva_entrada:
            self._entrada = "0."
            self._nueva_entrada = False
        elif "." not in self._entrada:
            self._entrada += "."

    def aplicar_operador(self, operador):
        if operador not in OPERADORES:
            raise ValueError(f"Operador no válido: {operador!r}")

        def operar():
            if self._operador is not None and not self._nueva_entrada:
                self._acumulado = _calcular(self._acumulado, self._operador, self._valor())
            else:
                self._acumulado = self._valor()
            self._operador = operador
            self._nueva_entrada = True
            self._entrada = _formatear(self._acumulado)

        self._ejecutar(operar)

    def igual(self):
        def resolver():
            if self._operador is None:
                return
            resultado = _calcular(self._acumulado, self._operador, self._valor())
            self._entrada = _formatear(resultado)
            self._acumulado = None
            self._operador = None
            self._nueva_entrada = True

        self._ejecutar(resolver)

    def cambiar_signo(self):
        def invertir():
            if self._entrada == "0":
                return
            if self._entrada.startswith("-"):
                self._entrada = self._entrada[1:]
            else:
                self._entrada = "-" + self._entrada
            if self._operador is not None:
                self._nueva_entrada = False

        self._ejecutar(invertir)

    def porcentaje(self):
        def calcular():
            self._entrada = _formatear(self._valor() / 100)
            if self._operador is not None:
                self._nueva_entrada = False

        self._ejecutar(calcular)

    def borrar(self):
        if self.hay_error:
            self.limpiar()
            return
        if self._nueva_entrada:
            return
        self._entrada = self._entrada[:-1]
        if self._entrada in ("", "-"):
            self._entrada = "0"

    def _ejecutar(self, operacion):
        """Ejecuta una operación y guarda su mensaje de error si falla."""
        if self.hay_error:
            return
        try:
            operacion()
        except ErrorCalculo as error:
            self._error = str(error)

    def _valor(self):
        return Decimal(self._entrada)

    def _cifras(self):
        return len(self._entrada.replace("-", "").replace(".", ""))


def _calcular(izquierda, operador, derecha):
    if operador == "+":
        return izquierda + derecha
    if operador == "-":
        return izquierda - derecha
    if operador == "*":
        return izquierda * derecha
    if derecha == 0:
        raise ErrorCalculo("No se puede dividir entre cero")
    return izquierda / derecha


def _formatear(valor):
    """Convierte un Decimal en texto legible, redondeado a 10 decimales."""
    try:
        valor = valor.quantize(PRECISION_RESULTADO, rounding=ROUND_HALF_UP)
    except InvalidOperation:
        raise ErrorCalculo("Desbordamiento")
    if valor == 0:
        return "0"
    texto = format(valor.normalize(), "f")
    if len(texto.replace("-", "").replace(".", "")) > MAX_DIGITOS_PANTALLA:
        raise ErrorCalculo("Desbordamiento")
    return texto
