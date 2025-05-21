import unittest
from unittest.mock import patch, MagicMock, Mock
from datetime import datetime, date, time
from sqlalchemy.exc import IntegrityError
from sqlalchemy import text

from app import create_app
from app.models import Event, User
from app.associations.event_users import EventUsers
from app.repositories.event_repository import EventRepository
from config import db


class TestEventRepository(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/test_db'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app_context = self.app.app_context()
        self.app_context.push()

        # Create all tables
        db.create_all()

        self.event_repo = EventRepository()

        # Sample event data
        self.event_data = {
            "event_name": "Test Event",
            "event_description": "A test event description",
            "id_gestionnaire": 1,
            "id_sport": 2,
            "event_ville": "Paris",
            "event_date": date(2025, 6, 15),
            "event_max_utilisateur": 10,
            "is_private": False,
            "is_team_vs_team": False,
            "longitude": 2.3522,
            "latitude": 48.8566
        }

        # Sample event instance
        self.event = Event(
            id=1,
            event_name="Test Event",
            event_description="A test event description",
            id_gestionnaire=1,
            id_sport=2,
            event_ville="Paris",
            event_date=date(2025, 6, 15),
            event_max_utilisateur=10,
            is_private=False,
            is_team_vs_team=False,
            longitude=2.3522,
            latitude=48.8566
        )

        # Sample user
        self.user = User(
            id=1,
            username="testuser"
        )

        # Sample participation
        self.participation = EventUsers(
            user_id=1,
            event_id=1
        )

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

    @patch('app.repositories.event_repository.db.session')
    def test_add_event(self, mock_session):
        """Test adding a new event."""
        mock_session.add.return_value = None
        mock_session.commit.return_value = None
        mock_session.flush.return_value = None

        result = self.event_repo.add_event(self.event_data)

        # Verify the session methods were called
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
        mock_session.flush.assert_called_once()

        # Check that the result has the correct attributes
        for key, value in self.event_data.items():
            self.assertEqual(getattr(result, key), value)

    @patch('app.repositories.event_repository.Event.query')
    def test_get_events_by_user_id(self, mock_query):
        """Test getting events by user ID."""
        mock_query.filter_by.return_value.all.return_value = [self.event]

        result = self.event_repo.get_events_by_user_id(1)

        mock_query.filter_by.assert_called_once_with(id_gestionnaire=1)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], self.event)

    @patch('app.repositories.event_repository.db.session')
    def test_get_events_filtred(self, mock_session):
        """Test getting filtered events."""
        mock_filter = MagicMock()
        mock_query_result = [(self.event, "testuser")]

        mock_session.query.return_value.join.return_value.filter.return_value.all.return_value = mock_query_result

        result = self.event_repo.get_events_filtred(mock_filter)

        mock_session.query.assert_called_once()
        mock_session.query.return_value.join.assert_called_once()
        mock_session.query.return_value.join.return_value.filter.assert_called_once_with(mock_filter)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0], self.event)
        self.assertEqual(result[0][1], "testuser")

    @patch('app.repositories.event_repository.db.session')
    def test_get_events_sorted_by_distance_and_date(self, mock_session):
        """Test getting events sorted by distance and date."""
        mock_query_result = [(self.event, 5.0)]
        mock_query = MagicMock()
        mock_session.query.return_value = mock_query
        mock_query.filter_by.return_value = mock_query
        mock_query.order_by.return_value = mock_query
        mock_query.limit.return_value = mock_query
        mock_query.all.return_value = mock_query_result

        result = self.event_repo.get_events_sorted_by_distance_and_date(48.8566, 2.3522, return_all_events=True, user_id=1)
        self.assertEqual(result, mock_query_result)

    @patch('app.repositories.event_repository.db.session')
    def test_get_events_sorted_by_date(self, mock_session):
        """Test getting events sorted by date."""
        mock_session.query.return_value.order_by.return_value.limit.return_value.all.return_value = [self.event]

        result = self.event_repo.get_events_sorted_by_date()

        mock_session.query.assert_called_once()
        mock_session.query.return_value.order_by.assert_called_once()
        mock_session.query.return_value.order_by.return_value.limit.assert_called_once_with(4)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], self.event)

    @patch('app.repositories.event_repository.db.session')
    @patch('app.repositories.event_repository.Event.query', new_callable=MagicMock)
    def test_get_event_by_id(self, mock_query, mock_session):
        """Test getting an event by ID."""
        mock_query.get.return_value = self.event

        result = self.event_repo.get_event_by_id(1)

        mock_query.get.assert_called_once_with(1)
        self.assertEqual(result, self.event)

    @patch('app.repositories.event_repository.db.session')
    def test_update_event_success(self, mock_session):
        """Test successfully updating an event."""
        mock_session.commit.return_value = None

        # Should not raise an exception
        self.event_repo.update_event()

        mock_session.commit.assert_called_once()

    # @patch('app.repositories.event_repository.db.session')
    # def test_update_event_integrity_error(self, mock_session):
    #     """Test handling IntegrityError during event update."""
    #     mock_error = MagicMock()
    #     mock_error.orig = "Database error"
    #     mock_session.commit.side_effect = IntegrityError("statement", "params", mock_error)
    #     mock_session.rollback.return_value = None
    
    #     with self.assertRaises(IntegrityError) as context:
    #         self.event_repo.update_event()
    
    #     self.assertEqual(str(context.exception), "Database error")
    #     mock_session.commit.assert_called_once()
    #     mock_session.rollback.assert_called_once()

    @patch('app.repositories.event_repository.db.session')
    def test_update_event_generic_error(self, mock_session):
        """Test handling generic exception during event update."""
        mock_error = Exception("Generic error")
        mock_session.commit.side_effect = mock_error
        mock_session.rollback.return_value = None

        with self.assertRaises(Exception):
            self.event_repo.update_event()

        mock_session.commit.assert_called_once()
        mock_session.rollback.assert_called_once()

    @patch('app.repositories.event_repository.EventUsers.query')
    def test_is_user_alredy_participating_true(self, mock_query):
        """Test checking if a user is already participating in an event (true case)."""
        mock_query.filter_by.return_value.first.return_value = self.participation

        result = self.event_repo.is_user_alredy_participating(1, 1)

        mock_query.filter_by.assert_called_once_with(event_id=1, user_id=1)
        self.assertEqual(result, self.participation)

    @patch('app.repositories.event_repository.EventUsers.query')
    def test_is_user_alredy_participating_false(self, mock_query):
        """Test checking if a user is already participating in an event (false case)."""
        mock_query.filter_by.return_value.first.return_value = None

        result = self.event_repo.is_user_alredy_participating(1, 1)

        mock_query.filter_by.assert_called_once_with(event_id=1, user_id=1)
        self.assertIsNone(result)

    @patch('app.repositories.event_repository.db.session')
    @patch('app.repositories.event_repository.EventUsers')
    def test_add_user_to_event(self, mock_event_users, mock_session):
        """Test adding a user to an event."""
        mock_event_users.return_value = self.participation
        mock_session.add.return_value = None
        mock_session.commit.return_value = None

        self.event_repo.add_user_to_event(1, 1)

        mock_event_users.assert_called_once_with(user_id=1, event_id=1)
        mock_session.add.assert_called_once_with(self.participation)
        mock_session.commit.assert_called_once()

    @patch('app.repositories.event_repository.db.session')
    def test_delete_participation(self, mock_session):
        """Test deleting a participation."""
        mock_session.delete.return_value = None
        mock_session.commit.return_value = None

        self.event_repo.delete_participation(self.participation)

        mock_session.delete.assert_called_once_with(self.participation)
        mock_session.commit.assert_called_once()

    @patch('app.repositories.event_repository.db.session')
    def test_delete_event(self, mock_session):
        """Test deleting an event."""
        with patch.object(self.event_repo, 'get_event_by_id', return_value=self.event) as mock_get:
            mock_session.delete.return_value = None
            mock_session.commit.return_value = None

            self.event_repo.delete_event(1)

            mock_get.assert_called_once_with(1)
            mock_session.delete.assert_called_once_with(self.event)
            mock_session.commit.assert_called_once()


if __name__ == '__main__':
    unittest.main()