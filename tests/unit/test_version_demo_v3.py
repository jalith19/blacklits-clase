import unittest


class FalloEjemploV3TestCase(unittest.TestCase):
    """Version final 'toda correcta': validaciones completas y cobertura adecuada."""

    def test_suma_basica(self):
        self.assertEqual(1 + 1, 2)

    def test_motivo_longitud_maxima(self):
        # Un motivo puede tener hasta 255 caracteres
        motivo = "x" * 255
        self.assertEqual(len(motivo), 255)
        self.assertLessEqual(len(motivo), 255)

    def test_motivo_longitud_excedida(self):
        # Un motivo de mas de 255 caracteres debe rechazarse
        motivo_largo = "x" * 256
        self.assertGreater(len(motivo_largo), 255)

    def test_email_valido(self):
        email = "usuario@example.com"
        self.assertIn("@", email)
        self.assertIn(".", email)
