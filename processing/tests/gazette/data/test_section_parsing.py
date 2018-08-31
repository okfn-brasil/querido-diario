from unittest.mock import MagicMock, PropertyMock, patch

from gazette.data.section_parsing import SectionParsing


class TestSectionParsing:
    def setup_method(self, _):
        session = MagicMock()
        self.subject = SectionParsing(session)

    @patch.object(SectionParsing, "update_bidding_exemptions")
    def test_update_calls_update_bidding_exemptions(self, update_bidding_exemptions):
        gazettes = [
            MagicMock(territory_id="4314902"),
            MagicMock(territory_id="4314902"),
        ]
        self.subject.update(gazettes)
        update_bidding_exemptions.assert_called()

    def test_update_changes_is_parsed_to_true(self):
        gazettes = [
            MagicMock(is_parsed=False, territory_id="4314902"),
            MagicMock(is_parsed=False, territory_id="4314902"),
        ]
        self.subject.update(gazettes)
        for gazette in gazettes:
            assert gazette.is_parsed

    def test_update_doesnt_change_is_parsed_when_has_no_parser(self):
        gazettes = [
            MagicMock(is_parsed=False, territory_id="4314902"),
            MagicMock(is_parsed=False, territory_id="42"),
        ]
        self.subject.update(gazettes)
        assert gazettes[0].is_parsed
        assert not gazettes[1].is_parsed

    def test_update_doesnt_raise_exception_with_territory_wo_parser(self):
        gazettes = [MagicMock(territory_id="42")]
        self.subject.update(gazettes)

    def test_update_bidding_exemptions_adds_new_exemptions_to_session(self):
        gazette = MagicMock(
            is_parsed=False, territory_id="4314902", bidding_exemptions=[]
        )
        parser = MagicMock()
        exceptions = [{"data": {"key": "value"}, "source_text": "key: value"}]
        parser.bidding_exemptions.return_value = exceptions
        self.subject.update_bidding_exemptions(gazette, parser)
        assert exceptions[0]["data"] == gazette.bidding_exemptions[0].data
        assert exceptions[0]["source_text"] == gazette.bidding_exemptions[0].source_text
