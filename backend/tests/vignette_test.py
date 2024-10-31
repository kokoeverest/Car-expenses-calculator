import unittest
from services.scrapers.vignette import get_vignette_price


class VignettePageTest(unittest.TestCase):
    """These tests validate the correct extraction of the annual vignette car price"""

    def test_vignettePrice_correctlyExtracted(self):
        # Arrange & Act
        expected_price = get_vignette_price()
        # Assert
        self.assertIsInstance(expected_price, float)
