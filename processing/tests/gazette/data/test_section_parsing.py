from unittest import TestCase
from unittest.mock import MagicMock, PropertyMock, patch

from gazette.data.section_parsing import SectionParsing


class TestSectionParsing(TestCase):

    def setUp(self):
        session = MagicMock()
        self.subject = SectionParsing(session)

    @patch.object(SectionParsing, 'update_bidding_exemptions')
    def test_update_calls_update_bidding_exemptions(self, update_bidding_exemptions):
        gazettes = [
            MagicMock(municipality_id='4314902'), MagicMock(municipality_id='4314902')
        ]
        self.subject.update(gazettes)
        update_bidding_exemptions.assert_called()

    def test_update_changes_is_parsed_to_true(self):
        gazettes = [
            MagicMock(is_parsed=False, municipality_id='4314902'),
            MagicMock(is_parsed=False, municipality_id='4314902'),
        ]
        self.subject.update(gazettes)
        for gazette in gazettes:
            self.assertEqual(True, gazette.is_parsed)

    def test_update_doesnt_change_is_parsed_when_has_no_parser(self):
        gazettes = [
            MagicMock(is_parsed=False, municipality_id='4314902'),
            MagicMock(is_parsed=False, municipality_id='42'),
        ]
        self.subject.update(gazettes)
        self.assertEqual(True, gazettes[0].is_parsed)
        self.assertEqual(False, gazettes[1].is_parsed)

    def test_update_doesnt_raise_exception_with_municipality_wo_parser(self):
        gazettes = [MagicMock(municipality_id='42')]
        self.subject.update(gazettes)

    def test_update_bidding_exemptions_adds_new_exemptions_to_session(self):
        gazette = MagicMock(
            is_parsed=False, municipality_id='4314902', bidding_exemptions=[]
        )
        parser = MagicMock()
        exceptions = [{'data': {'key': 'value'}, 'source_text': 'key: value'}]
        parser.bidding_exemptions.return_value = exceptions
        self.subject.update_bidding_exemptions(gazette, parser)
        self.assertEqual(exceptions[0]['data'], gazette.bidding_exemptions[0].data)
        self.assertEqual(
            exceptions[0]['source_text'], gazette.bidding_exemptions[0].source_text
        )
