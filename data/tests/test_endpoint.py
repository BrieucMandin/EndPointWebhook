import unittest

from unittest.mock import patch

from data.endpoints import get_endpoint

class GetEndpointTestCase(unittest.TestCase):

    @patch("data.endpoints.settings")
    def test_get_endpoint_joueur(self, mock_settings):
        mock_settings.REMOTE_API_BASE_URL = "http://127.0.0.1:8000"
        result = get_endpoint("joueur", 42)
        expected = "http://127.0.0.1:8000/joueurs/42/"
        self.assertEqual(result, expected)

    @patch("data.endpoints.settings")
    def test_get_endpoint_entraineur(self, mock_settings):
        mock_settings.REMOTE_API_BASE_URL = "http://127.0.0.1:8000"
        result = get_endpoint("entraineur", 5)
        expected = "http://127.0.0.1:8000/entraineurs/5/"
        self.assertEqual(result, expected)

    @patch("data.endpoints.settings")
    def test_get_endpoint_equipe(self, mock_settings):
        mock_settings.REMOTE_API_BASE_URL = "http://127.0.0.1:8000"
        result = get_endpoint("equipe", 8)
        expected = "http://127.0.0.1:8000/equipes/8/"
        self.assertEqual(result, expected)

    @patch("data.endpoints.settings")
    def test_get_endpoint_type_inconnu(self, mock_settings):
        mock_settings.REMOTE_API_BASE_URL = "http://127.0.0.1:8000"
        result = get_endpoint("arbitre", 1)
        self.assertIsNone(result)

if __name__ == "__main__":
    unittest.main()
