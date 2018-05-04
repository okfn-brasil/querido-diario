from unittest import TestCase

from gazette.locations.pr_foz_do_iguacu import PrFozDoIguacu


class TestPrFozDoIguacu(TestCase):

    def setUp(self):
        path = 'tests/gazette/fixtures/pr_foz_do_iguacu.txt'
        with open(path) as file:
            self.text = file.read()
        self.subject = PrFozDoIguacu(self.text)

    def test_pages(self):
        pages = self.subject.pages()
        self.assertEqual(96, len(pages))
        self.assertEqual(self.text[-3056:-75], pages[-1].strip())
