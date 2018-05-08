from unittest import TestCase

from gazette.locations.pr_foz_do_iguacu import PrFozDoIguacu


class TestPrFozDoIguacu(TestCase):

    def setUp(self):
        path = 'tests/gazette/fixtures/pr_foz_do_iguacu.txt'
        self.text = self._get_text_from_file(path)
        self.subject = PrFozDoIguacu(self.text)

        multiple_patterns = 'tests/gazette/fixtures/pr_foz_do_iguacu_multiple_patterns.txt'
        self.patterns_subject = PrFozDoIguacu(self._get_text_from_file(multiple_patterns))

    @staticmethod
    def _get_text_from_file(path):
        with open(path) as file:
            text = file.read()
        return text

    def test_pages(self):
        pages = self.subject.pages()
        self.assertEqual(96, len(pages))
        self.assertEqual(self.text[-3056:-75], pages[-1].strip())

    def test_bidding_exemption_sections(self):
        exemptions = self.subject.bidding_exemption_sections()
        self.assertEqual(len(exemptions), 2)

    def test_patterns(self):
        exemptions = self.patterns_subject.bidding_exemption_sections()
        self.assertEqual(len(exemptions), 5)
