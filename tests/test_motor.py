import unittest

from motor import Calculadora


def teclear(calc, secuencia):
    """Simula pulsar una secuencia de teclas, por ejemplo '2+3='."""
    for tecla in secuencia:
        if tecla in "0123456789":
            calc.ingresar_digito(tecla)
        elif tecla == ".":
            calc.ingresar_decimal()
        elif tecla in "+-*/":
            calc.aplicar_operador(tecla)
        elif tecla == "=":
            calc.igual()
        elif tecla == "%":
            calc.porcentaje()
        elif tecla == "±":
            calc.cambiar_signo()
        elif tecla == "⌫":
            calc.borrar()
        elif tecla == "C":
            calc.limpiar()
    return calc.pantalla


class TestMotor(unittest.TestCase):

    def setUp(self):
        self.calc = Calculadora()

    def test_suma_simple(self):
        self.assertEqual(teclear(self.calc, "2+3="), "5")

    def test_decimales_sin_error_de_punto_flotante(self):
        self.assertEqual(teclear(self.calc, "0.1+0.2="), "0.3")

    def test_operaciones_encadenadas_de_izquierda_a_derecha(self):
        self.assertEqual(teclear(self.calc, "2+3*4="), "20")

    def test_division(self):
        self.assertEqual(teclear(self.calc, "1/4="), "0.25")

    def test_resultado_con_muchos_decimales_se_redondea(self):
        self.assertEqual(teclear(self.calc, "1/3="), "0.3333333333")

    def test_division_entre_cero_muestra_error(self):
        self.assertEqual(teclear(self.calc, "5/0="),
                         "No se puede dividir entre cero")
        self.assertTrue(self.calc.hay_error)

    def test_la_tecla_C_se_recupera_tras_un_error(self):
        teclear(self.calc, "5/0=")
        self.assertEqual(teclear(self.calc, "C"), "0")
        self.assertFalse(self.calc.hay_error)

    def test_desbordamiento(self):
        self.assertEqual(teclear(self.calc, "999999999999*999999999999="),
                         "Desbordamiento")

    def test_cambio_de_signo(self):
        self.assertEqual(teclear(self.calc, "7±"), "-7")
        self.assertEqual(teclear(self.calc, "±"), "7")

    def test_porcentaje(self):
        self.assertEqual(teclear(self.calc, "50%"), "0.5")

    def test_porcentaje_dentro_de_una_suma(self):
        self.assertEqual(teclear(self.calc, "2+50%="), "2.5")

    def test_solo_un_decimal(self):
        self.assertEqual(teclear(self.calc, "1.2.3"), "1.23")

    def test_borrar(self):
        self.assertEqual(teclear(self.calc, "123⌫"), "12")
        self.assertEqual(teclear(self.calc, "⌫⌫⌫"), "0")

    def test_igual_sin_operador_no_cambia_el_numero(self):
        self.assertEqual(teclear(self.calc, "5="), "5")

    def test_digito_tras_resultado_empieza_una_entrada_nueva(self):
        self.assertEqual(teclear(self.calc, "2+3=7"), "7")

    def test_expresion_pendiente(self):
        teclear(self.calc, "12+")
        self.assertEqual(self.calc.expresion, "12 +")

    def test_limite_de_digitos_de_entrada(self):
        teclear(self.calc, "1234567890123456")
        self.assertEqual(self.calc.pantalla, "123456789012")


if __name__ == "__main__":
    unittest.main()
