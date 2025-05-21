import unittest
from unittest.mock import patch, MagicMock
from io import BytesIO
from flask import Flask
from werkzeug.datastructures import FileStorage
from datetime import datetime, timedelta
from sqlalchemy import text
import os

from app import create_app
from app.services.event_service import EventService
from app.models import Event, User, Sport
from config import db


class TestEventService(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/test_db'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app.config['TEAM_PHOTOS_FOLDER'] = '/tmp/test_uploads'
        self.app_context = self.app.app_context()
        self.app_context.push()

        # Create all tables
        db.create_all()

        self.event_service = EventService()

        # Create test user
        self.test_user = User(
            username='testuser',
            email='test@example.com',
            password='testpass',
            firstname='Test',
            familyname='User',
            date_of_birth=datetime.now() - timedelta(days=365 * 30),
            phone='1234567890',
            city='Test City',
            consent=True
        )
        db.session.add(self.test_user)

        # Create test sport
        self.test_sport = Sport(
            sport_nom='Test Sport',
            stat_solo=True
        )
        db.session.add(self.test_sport)
        db.session.commit()

    def tearDown(self):
        """Clean up after each test."""
        db.session.remove()
        with db.engine.connect() as conn:
            conn.execute(text("DROP TABLE IF EXISTS events CASCADE"))
            conn.execute(text("DROP TABLE IF EXISTS event_invitations CASCADE"))
            conn.execute(text("DROP TABLE IF EXISTS event_participants CASCADE"))
            conn.execute(text("DROP TABLE IF EXISTS sports CASCADE"))
            conn.execute(text("DROP TABLE IF EXISTS users CASCADE"))
            conn.commit()
        self.app_context.pop()

    # @patch('app.repositories.event_repository.EventRepository')
    # def test_create_event_success(self, mock_repo_class):
    #     # Create a mock Event object
    #     mock_event = MagicMock()
    #     mock_event.id = 1
    #     mock_event.event_name = "Test Event"
    #     mock_event.event_description = "Test Description"
    #     mock_event.event_ville = "Test City"
    #     mock_event.event_max_utilisateur = 10
    #     mock_event.date_limite_inscription = datetime.now() + timedelta(days=7)
    #     mock_event.event_date = datetime.now() + timedelta(days=1)
    #     mock_event.start_time = datetime.now().time()
    #     mock_event.end_time = (datetime.now() + timedelta(hours=2)).time()
    #     mock_event.event_image = "test_image.jpg"
    #     mock_event.sport_id = 1
    #     mock_event.user_id = 1

    #     # Configure the mock repository
    #     mock_repo = MagicMock()
    #     mock_repo_class.return_value = mock_repo
    #     mock_repo.add_event.return_value = mock_event

    #     # Create test data
    #     event_data = {
    #         'event_name': 'Test Event',
    #         'event_description': 'Test Description',
    #         'event_ville': 'Test City',
    #         'event_max_utilisateur': 10,
    #         'date_limite_inscription': (datetime.now() + timedelta(days=7)).isoformat(),
    #         'event_date': (datetime.now() + timedelta(days=1)).isoformat(),
    #         'start_time': datetime.now().time().isoformat(),
    #         'end_time': (datetime.now() + timedelta(hours=2)).time().isoformat(),
    #         'sport_id': 1,
    #         'user_id': 1
    #     }

    #     # Create a fake file
    #     fake_file = FileStorage(
    #         stream=BytesIO(b"fake image data"),
    #         filename="test_image.jpg",
    #         content_type="image/jpeg"
    #     )

    #     # Create upload directory
    #     os.makedirs('/tmp/test_uploads', exist_ok=True)

    #     # Call the service method
    #     result = self.event_service.create_event(event_data, fake_file)

    #     # Verify the result
    #     self.assertEqual(result.id, 1)
    #     self.assertEqual(result.event_name, "Test Event")
    #     self.assertEqual(result.event_description, "Test Description")
    #     self.assertEqual(result.event_ville, "Test City")
    #     self.assertEqual(result.event_max_utilisateur, 10)
    #     self.assertEqual(result.date_limite_inscription, (datetime.now() + timedelta(days=7)).isoformat())
    #     self.assertEqual(result.event_date, (datetime.now() + timedelta(days=1)).isoformat())
    #     self.assertEqual(result.start_time, datetime.now().time())
    #     self.assertEqual(result.end_time, (datetime.now() + timedelta(hours=2)).time())
    #     self.assertEqual(result.event_image, "test_image.jpg")
    #     self.assertEqual(result.sport_id, 1)
    #     self.assertEqual(result.user_id, 1)
    #     mock_repo.add_event.assert_called_once()

    #     # Clean up
    #     import shutil
    #     shutil.rmtree('/tmp/test_uploads', ignore_errors=True)

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
