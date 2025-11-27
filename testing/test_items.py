# tests/test_item_extractor.py
import os
import sys
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(ROOT, "src"))

from items import Extract_Restructure

class Testitems(unittest.TestCase):
    def test_stream_until_stop(self):
        """
        Test that this will get all the text from a starting tag
        until hitting a stopping point (Item 7A, 8, or 9).
        """
        # Add your test code here
        pass
    
    def test_find_real_item7(self):
        """
        Test that the correct starting point for Item 7 is identified
        in a sample 10-K HTML file.
        """
        # Add your test code here
        pass
    
    def test_find_real_item8(self):
        """
        Test that the correct starting point for Item 8 is identified
        in a sample 10-K HTML file.
        """
        # Add your test code here
        pass
    
    def test_extract_items(self):
        """
        Test that both Item 7 and Item 8 are extracted correctly
        from a sample 10-K HTML file.
        """
        # Add your test code here
        pass
    

