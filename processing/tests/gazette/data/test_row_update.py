from unittest import TestCase
from unittest.mock import MagicMock, patch

from gazette.data.row_update import RowUpdate


class TestRowUpdate(TestCase):
    def setUp(self):
        self.subject = RowUpdate(MagicMock)

    @patch.object(RowUpdate, "filtered_rows")
    @patch.object(RowUpdate, "session")
    def test_call_updates_using_executor(self, _, filtered_rows):
        executor = MagicMock()
        self.subject(executor)
        executor.return_value.update.assert_called_with(filtered_rows())

    @patch("gazette.data.row_update.create_tables")
    @patch("gazette.data.row_update.db_connect")
    @patch("gazette.data.row_update.sessionmaker")
    @patch("gazette.data.row_update.text")
    def test_call_commits_executor_changes(self, _text, sessionmaker, _db, _create):
        executor = MagicMock()
        self.subject(executor)
        sessionmaker.return_value.return_value.commit.assert_called_with()

    @patch("gazette.data.row_update.create_tables")
    @patch("gazette.data.row_update.db_connect")
    @patch("gazette.data.row_update.sessionmaker")
    @patch("gazette.data.row_update.text")
    def test_session_creates_tables(self, _text, _maker, _db, create_tables):
        self.subject.session()
        create_tables.assert_called()

    @patch("gazette.data.row_update.text")
    @patch.object(RowUpdate, "session")
    def test_filtered_rows_queries_following_condition(self, session, text):
        condition = text("column = 42")
        self.subject.filtered_rows(condition)
        session.return_value.query.return_value.filter.assert_called_with(condition)
