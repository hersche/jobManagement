import random
import unittest
from cryptClass import *

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.mod = scm.getMod("3")
        self.cm = cm(self.mod, "Password")
    def test_name(self):
        self.assertEqual(self.mod.__name__[14:], "DES3")
    def test_enDecryptText(self):
        encrypted = self.cm.encrypt("Test")
        decrypted =self.cm.decrypt(encrypted)
        self.assertEqual("Test", decrypted)
    def test_enDecryptNr(self):
        encrypted = self.cm.encrypt(34)
        decrypted =self.cm.decrypt(encrypted)
        self.assertEqual(float(34), float(decrypted))


if __name__ == '__main__':
    unittest.main()