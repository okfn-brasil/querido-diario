from gazette.locations.rs_porto_alegre import RsPortoAlegre


class TestRsPortoAlegre:
    def setup_method(self, _):
        path = "tests/gazette/fixtures/rs_porto_alegre.txt"
        with open(path) as file:
            self.text = file.read()
        self.subject = RsPortoAlegre(self.text)

    def test_pages(self):
        pages = self.subject.pages()
        assert 19 == len(pages)
        assert self.text[:3498] == pages[0].strip()

    def test_bidding_exemptions(self):
        exemptions = self.subject.bidding_exemptions()
        expectation = [
            {
                "data": {
                    "CONTRATANTE": "Município de Porto Alegre.",
                    "CONTRATADO": "Classul Indústria e Comércio de Placas e Brindes Ltda.",
                    "OBJETO": "Confecção de 50 medalhas Cidade de Porto Alegre.",
                    "VALOR": "R$ 5.535,00.",
                    "DOTAÇÃO ORÇAMENTÁRIA": "201-2524-339031050000-1",
                    "BASE LEGAL": "Artigo 24, inciso II, da Lei Federal 8.666/93.",
                },
                "source_text": "                                                 DISPENSA DE LICITAÇÃO\n     PROCESSO 001.0003845.15.0\n     CONTRATANTE: Município de Porto Alegre.\n     CONTRATADO: Classul Indústria e Comércio de Placas e Brindes Ltda.\n     OBJETO: Confecção de 50 medalhas Cidade de Porto Alegre.\n     VALOR: R$ 5.535,00.\n     DOTAÇÃO ORÇAMENTÁRIA: 201-2524-339031050000-1\n     BASE LEGAL: Artigo 24, inciso II, da Lei Federal 8.666/93.\n\n                                                  Porto Alegre, 27 de fevereiro de 2015.\n\n                                           URBANO SCHMITT, Secretário Municipal de Gestão.",
            },
            {
                "data": {
                    "CONTRATANTE": "Município de Porto Alegre.",
                    "CONTRATADO": "Classul Indústria e Comércio de Placas e Brindes Ltda.",
                    "OBJETO": "Gravação a laser em 21 medalhas Cidade de Porto Alegre.",
                    "VALOR": "R$ 735,00.",
                    "DOTAÇÃO ORÇAMENTÁRIA": "201-2524-339031050000-1",
                    "BASE LEGAL": "Artigo 24, inciso II, da Lei Federal 8.666/93",
                },
                "source_text": "                                                 DISPENSA DE LICITAÇÃO\n     PROCESSO 001.0003844.15.3\n     CONTRATANTE: Município de Porto Alegre.\n     CONTRATADO: Classul Indústria e Comércio de Placas e Brindes Ltda.\n     OBJETO: Gravação a laser em 21 medalhas Cidade de Porto Alegre.\n     VALOR: R$ 735,00.\n     DOTAÇÃO ORÇAMENTÁRIA: 201-2524-339031050000-1\n     BASE LEGAL: Artigo 24, inciso II, da Lei Federal 8.666/93\n\n                                                  Porto Alegre, 27 de fevereiro de 2015.\n\n                                           URBANO SCHMITT, Secretário Municipal de Gestão.",
            },
            {
                "data": {
                    "CONTRATANTE": "Município de Porto Alegre, através da Secretaria Municipal da Saúde.",
                    "CONTRATADO": "VIP ELEVADORES LTDA",
                    "OBJETO": "Conserto de componente eletrônico do armário de comando de elevador HMIPV, sem cobertura contratual.",
                    "VALOR": "R$ 11.232,00 (onze mil reais, duzentos e trinta e dois reais).",
                    "BASE LEGAL": "Artigo 24, inciso I, da Lei Federal 8.666/93",
                },
                "source_text": "                                               DISPENSA DE LICITAÇÃO\n     PROCESSO 001.037017.14.4\n     CONTRATANTE: Município de Porto Alegre, através da Secretaria Municipal da Saúde.\n     CONTRATADO: VIP ELEVADORES LTDA\n     OBJETO: Conserto de componente eletrônico do armário de comando de elevador HMIPV, sem cobertura contratual.\n     VALOR: R$ 11.232,00 (onze mil reais, duzentos e trinta e dois reais).\n     BASE LEGAL: Artigo 24, inciso I, da Lei Federal 8.666/93\n\n                                                Porto Alegre, 24 de fevereiro de 2015..\n\n                                  CARLOS HENRIQUE CASARTELLI, Secretário Municipal de Saúde.",
            },
        ]
        assert expectation == exemptions
