import unittest
from unittest.mock import patch, MagicMock
from io import BytesIO
from flask import Flask
from werkzeug.datastructures import FileStorage
from datetime import datetime

from app.services.event_service import EventService

class TestEventService(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config["TEAM_PHOTOS_FOLDER"] = "/fake/path"
        self.event_service = EventService()
        self.event_service.event_repository = MagicMock()

    @patch("app.services.event_service.uuid.uuid4", return_value="mock-uuid")
    @patch("werkzeug.datastructures.FileStorage.save")  # Mock ici
    def test_create_event_success(self, mock_save, mock_uuid):
        event_data = {
            "event_date": "2024-12-01",
            "start_time": "10:00:00",
            "end_time": "12:00:00"
        }

        fake_file = FileStorage(
            stream=BytesIO(b"fake image data"),
            filename="photo.png",
            content_type="image/png"
        )

        mock_added_event = {"id": 1, "name": "Test Event"}
        self.event_service.event_repository.add_event.return_value = mock_added_event

        with self.app.app_context():
            result = self.event_service.create_event(event_data, fake_file)
            self.assertEqual(result, mock_added_event)

    @patch("werkzeug.datastructures.FileStorage.save")  # Mock ici aussi
    def test_create_event_with_invalid_date_format(self, mock_save):
        event_data = {
            "event_date": "01-12-2024",  # format invalide
            "start_time": "10:00:00",
            "end_time": "12:00:00"
        }

        fake_file = FileStorage(
            stream=BytesIO(b"fake image"),
            filename="photo.jpg",
            content_type="image/jpeg"
        )

        with self.app.app_context():
            with self.assertRaises(ValueError):
                self.event_service.create_event(event_data, fake_file)


if __name__ == '__main__':
    unittest.main()
