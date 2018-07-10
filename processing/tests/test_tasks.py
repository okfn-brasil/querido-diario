import glob
from unittest import TestCase
from unittest.mock import call, patch

from freezegun import freeze_time

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

    @patch('tasks.subprocess.Popen')
    def test_run_spider(self, popen):
        tasks.run_spider('rs_porto_alegre')
        popen.assert_called_with(['scrapy', 'crawl', 'rs_porto_alegre'], cwd='data_collection')

    @freeze_time('2018-01-08')
    @patch('tasks.subprocess.Popen')
    def test_run_spider_using_week_timerange(self, popen):
        tasks.run_spider('rs_porto_alegre', timerange='past_week')
        command = ['scrapy', 'crawl', 'rs_porto_alegre', '-a', 'start_date=2018-01-01']
        popen.assert_called_with(command, cwd='data_collection')

    @patch('tasks.subprocess.Popen')
    def test_run_spiders(self, popen):
        tasks.run_spiders()
        spiders = '/mnt/code/data_collection/gazette/spiders/*.py'
        spider_calls = []
        for module in sorted(glob.glob(spiders)):
            name = module.split('/')[-1].split('.')[0]
            if name not in ['__init__', 'base']:
                new_call = call(['scrapy', 'crawl', name], cwd='data_collection')
                spider_calls.append(new_call)
        self.assertEqual(popen.mock_calls, spider_calls)

    @freeze_time('2018-01-08')
    @patch('tasks.subprocess.Popen')
    def test_run_spiders_using_week_timerange(self, popen):
        tasks.run_spiders(['rs_porto_alegre'], timerange='past_week')
        command = ['scrapy', 'crawl', 'rs_porto_alegre', '-a', 'start_date=2018-01-01']
        popen.assert_called_with(command, cwd='data_collection')

    @patch('tasks.subprocess.Popen')
    def test_run_spiders_using_unsupported_timerange(self, popen):
        with self.assertRaises(ValueError):
            tasks.run_spiders(['rs_porto_alegre'], timerange='past_month')
