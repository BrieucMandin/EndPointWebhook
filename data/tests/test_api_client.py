import requests

from unittest import TestCase
from unittest.mock import patch, Mock

from data.api_client import fetch_data

class FetchDataTests(TestCase):

    @patch("data.api_client.requests.get")
    def test_fetch_data_success(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"message": "ok"}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        result = fetch_data("http://fake-url.com/endpoint")
        mock_get.assert_called_once_with("http://fake-url.com/endpoint")
        mock_response.raise_for_status.assert_called_once()
        self.assertEqual(result, {"message": "ok"})

    @patch("data.api_client.requests.get")
    def test_fetch_data_http_error(self, mock_get):
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.HTTPError("Erreur 500")
        mock_get.return_value = mock_response

        with self.assertRaises(requests.HTTPError):
            fetch_data("http://fake-url.com/endpoint")
