from unittest import TestCase
from unittest.mock import MagicMock, patch

from gazette.data.gazette_update import GazetteUpdate


class TestGazetteUpdate(TestCase):

    def setUp(self):
        self.subject = GazetteUpdate('4314902')

    @patch.object(GazetteUpdate, 'filtered_rows')
    @patch.object(GazetteUpdate, 'session')
    def test_call_updates_using_executor(self, _, filtered_rows):
        executor = MagicMock()
        self.subject(executor)
        executor.return_value.update.assert_called_with(filtered_rows())

    @patch('gazette.data.gazette_update.create_gazettes_table')
    @patch('gazette.data.gazette_update.db_connect')
    @patch('gazette.data.gazette_update.sessionmaker')
    @patch('gazette.data.gazette_update.text')
    def test_call_commits_executor_changes(self, _text, sessionmaker, _db, _create):
        executor = MagicMock()
        self.subject(executor)
        sessionmaker.return_value.return_value.commit.assert_called_with()

    @patch('gazette.data.gazette_update.create_gazettes_table')
    @patch('gazette.data.gazette_update.db_connect')
    @patch('gazette.data.gazette_update.sessionmaker')
    @patch('gazette.data.gazette_update.text')
    def test_session_creates_table(self, _text, _maker, _db, create_gazettes_table):
        self.subject.session()
        create_gazettes_table.assert_called()

    @patch('gazette.data.gazette_update.text')
    @patch.object(GazetteUpdate, 'session')
    def test_filtered_rows_queries_following_condition(self, session, text):
        condition = text('column = 42')
        self.subject.filtered_rows(condition)
        session.return_value.query.return_value.filter.assert_called_with(condition)
