# tests/test_clean_name.py
import sys
sys.path.append('/Users/bruce/OneDrive/Desktop/School/URAP/Code/src')  # Adjust the path as necessary to import from src
import unittest
from Extract_File import Extractor

class TestExtractor(unittest.TestCase):

    def test_clean_name(self):
        name = "Microsoft Corporation"
        cleaned = Extractor.clean_name(name)
        self.assertEqual(cleaned, "microsoft")
if __name__ == '__main__':
    unittest.main()