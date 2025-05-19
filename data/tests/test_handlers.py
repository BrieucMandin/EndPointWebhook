from unittest import TestCase
from unittest.mock import patch

from data.handlers import process_webhook_payload


class ProcessWebhookPayloadTests(TestCase):

    @patch("data.handlers.delete_in_base")
    def test_process_delete_action(self, mock_delete):

        payload = {"type": "joueur", "action": "delete", "id": 42}

        process_webhook_payload(payload)

        mock_delete.assert_called_once_with(42, "joueur")

    @patch("data.handlers.update_or_create_object")
    @patch("data.handlers.fetch_data")
    @patch("data.handlers.get_endpoint")
    def test_process_update_action(self, mock_get_endpoint, mock_fetch_data, mock_update):

        payload = {"type": "entraineur", "action": "update", "id": 10}

        mock_get_endpoint.return_value = "https://fake.api/entraineurs/10"
        mock_fetch_data.return_value = {"id_En": 10, "nom": "Zidane", "experience": 12, "nationalite": "Française"}

        process_webhook_payload(payload)

        mock_get_endpoint.assert_called_once_with("entraineur", 10)
        mock_fetch_data.assert_called_once_with("https://fake.api/entraineurs/10")
        mock_update.assert_called_once_with(mock_fetch_data.return_value, "entraineur")

    def test_process_unknown_action(self):
        payload = {"type": "joueur", "action": "foo", "id": 1}

        # Ne lève pas d'exception, juste affiche un message
        try:
            process_webhook_payload(payload)
        except Exception as e:
            self.fail(f"process_webhook_payload raised an exception unexpectedly: {e}")
