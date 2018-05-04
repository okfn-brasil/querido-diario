import re


class PrFozDoIguacu:
    HEADER_REGEX = r'Ano[\s\w]+Diário Oficial Nº [\w\s.]+Página \d+ de \d+'
    END_OF_PAGE_REGEX = r'\n{3,}\s+www.pmfi.pr.gov.br\n'
    BIDDING_EXEMPTIONS_PATTERNS = [
        r'PROCESSO([\w\W]+?)fundamento no (?P<law>.+), para(?P<object>[\w\W]+?)da seguinte empresa e valor:\n\s+CONTRATANTE: (?P<contractor>[\w\W]+?)CONTRATADA: (?P<contracted>[\w\W]+?)CNPJ([\w\W]+?)Valor: R\$ (?P<value>[\d\.,]+)([\w\W]+?)'r'Data: (?P<date>\d{2}/\d{2}/\d{4})',
    ]

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
        patterns = [re.compile(pattern) for pattern in self.BIDDING_EXEMPTIONS_PATTERNS]
        return [
            binding
            for pattern in patterns
            for binding in pattern.findall(self._source_text())
        ]

    def _source_text(self):
        return '\n'.join([
            page
            for page in self.pages()
        ])
