# tests/test_get_cik.py
import os
import sys
import unittest
from unittest.mock import patch

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(ROOT, "src"))

from Extract_File import Extractor  # <- match your actual module name

class TestExtractor(unittest.TestCase):

    @patch.object(Extractor, 'fetch_html')
    def test_fetch_10k(self, mock_fetch_html):
        # Arrange
        mock_fetch_html.return_value = "<html>Mocked HTML content</html>"
        extractor = Extractor("AAPL", 2020)

        # Act
        result = extractor.fetch_10k()

        # Assert
        self.assertIn("Mocked HTML content", result)