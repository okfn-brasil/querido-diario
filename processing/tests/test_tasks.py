from unittest import TestCase
from unittest.mock import patch

import tasks


class TestTasks(TestCase):
    @patch("tasks.BiddingExemption")
    @patch("tasks.BiddingExemptionParsing")
    @patch("tasks.RowUpdate")
    def test_parse_bidding_exemptions(self, update, parsing, bidding_exemption):
        tasks.parse_bidding_exemptions()
        update.assert_called_with(bidding_exemption)
        update.return_value.assert_called_with(parsing)

    @patch("tasks.Gazette")
    @patch("tasks.RowUpdate")
    @patch("tasks.SectionParsing")
    @patch("tasks.parse_bidding_exemptions")
    def test_parse_sections(self, parse_exemptions, parsing, update, gazette):
        tasks.parse_sections()
        update.assert_called_with(gazette)
        update.return_value.assert_called_with(parsing)
        parse_exemptions.delay.assert_called_once()
