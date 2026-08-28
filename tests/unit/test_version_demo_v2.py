import unittest


@unittest.skip("Version demo intermedia desactivada; se mantiene la final V3")
class FalloEjemploV2TestCase(unittest.TestCase):
    """Version 'medianamente bien': el test corre pero la validacion es debil o incompleta."""

    def test_suma_basica(self):
        # Pasa, pero solo comprueba un valor y no cubre casos limite
        self.assertEqual(1 + 1, 2)

    def test_valida_motivo_solo_longitud(self):
        # Solo valida que no este vacio, pero no la longitud maxima (255)
        motivo = "spam"
        self.assertTrue(len(motivo) > 0)
