import re


class PrFozDoIguacu:
    HEADER_REGEX = r'Ano[\s\w]+Diário Oficial Nº [\w\s.]+Página \d+ de \d+'
    END_OF_PAGE_REGEX = r'\n{3,}\s+www.pmfi.pr.gov.br\n'

    def __init__(self, text):
        self.text = text

    def _remove_page_footer(self):
        return re.sub(self.END_OF_PAGE_REGEX, '', self.text)

    def pages(self):
        return re.split(self.HEADER_REGEX, self._remove_page_footer())

    def text_sections(self):
        return re.split(r'\n{3,}', self._source_text())

    def bidding_exemption_sections(self):
        # TODO Aplly patterns to separate multiple bidding_exemptions in a section
        return [
            section
            for section in self.text_sections()
            if 'dispensa de licitação' in section.lower()
        ]

    def _source_text(self):
        return '\n'.join([
            page
            for page in self.pages()
        ])
