from unittest import TestCase, skip

from gazette.locations.go_goiania import GoGoiania


def subject_2():
    path = "tests/gazette/fixtures/go_goiania_2.txt"
    with open(path) as file:
        text = file.read()
    return GoGoiania(text)


class TestGoGoiania(TestCase):
    def setUp(self):
        path = "tests/gazette/fixtures/go_goiania.txt"
        with open(path) as file:
            self.text = file.read()
        self.subject = GoGoiania(self.text)

    def test_pages(self):
        pages = self.subject.pages()
        self.assertEqual(241, len(pages))
        expected_expressions = (
            "Criado pela Lei nº 1.552, de 21/08/1959",
            "Versão digital instituída pelo Decreto nº 3.987, de 14/08/2013",
            "Esta versão está assinada digitalmente, conforme MP nº 2.200-2",
            "E-mail contato: diariooficial@casacivil.goiania.go.gov.br",
            "PILOTO:88708985120",
        )
        for expected in expected_expressions:
            self.assertIn(expected, pages[0])

    def test_bidding_exemptions(self):
        exemptions = self.subject.bidding_exemptions()
        exemptions = [exemption for exemption in exemptions]
        expectation = [
            {
                "data": {
                    "PROCESSO": "320/2018.",
                    "LOCAL E DATA": "Goiânia, 07 de março de 2018.",
                    "OBJETO": "Trata o presente de Ato de Dispensa de Licitação prevista no artigo 24 inciso II da Lei nº 8.666 de 1993, tendo por objeto a aquisição de uniformes para atender o Projeto Guarda Mirim.",
                    "ÓRGÃO CONTRATANTE": "Agência da Guarda Civil Metropolitana de Goiânia – AGCMG, CNPJ nº 10.498.531/0001-00.",
                    "CONTRATADA": "Alvanir Batista Moreira - MEI, CNPJ nº 18.893.745/0001-92.",
                    "VALOR TOTAL": "R$ 7.999,80 (Sete mil, novecentos e noventa e nove reais e oitenta centavos).",
                },
                "source_text": "\n\n\n                                                                    Agência da Guarda Civil Metropolitana de Goiânia\n\n\n\n\n                                      EXTRATO DE ATO DE DISPENSA DE LICITAÇÃO\n\n\n\n\n         - PROCESSO: 320/2018.\n         - LOCAL E DATA: Goiânia, 07 de março de 2018.\n         - OBJETO: Trata o presente de Ato de Dispensa de Licitação prevista no artigo 24 inciso II da\n         Lei nº 8.666 de 1993, tendo por objeto a aquisição de uniformes para atender o Projeto Guarda\n         Mirim.\n         - ÓRGÃO CONTRATANTE: Agência da Guarda Civil Metropolitana de Goiânia – AGCMG,\n         CNPJ nº 10.498.531/0001-00.\n         - CONTRATADA: Alvanir Batista Moreira - MEI, CNPJ nº 18.893.745/0001-92.\n         - VALOR TOTAL: R$ 7.999,80 (Sete mil, novecentos e noventa e nove reais e oitenta centavos).\n\n\n\n\n                                                    JOSÉ EULÁLIO VIEIRA\n                                                Presidente-Comandante da AGCMG\n\n\n\n\nAv. Nazareno Roriz, nº 66 – Setor Castelo Branco – CEP: 74405-010\nFone: (62) 3524-8661 – Fax: (62) 3524-1947\nE-mail: presidenteagmg@hotmail.com\n\n\n      Prefeitura de Goiânia/ Sup. da Casa Civil e Articulação Política - Assinado Digitalmente: www.goiania.go.gov.br\n\x0c      DOM Eletrônico                              Edição Nº 6772, de 14 de março de 2018.             ",
            },
            {
                "data": {
                    "PROCESSO": "390/2018.",
                    "LOCAL E DATA": "Goiânia, 07 de março de 2018.",
                    "OBJETO": "Trata o presente de Ato de Dispensa de Licitação prevista no artigo 24 inciso II da Lei nº 8.666 de 1993, tendo por objeto aquisição de Certificado Digital PJ1, para atender a Comissão Municipal de Defesa Civil - COMDEC.",
                    "ÓRGÃO CONTRATANTE": "Agência da Guarda Civil Metropolitana de Goiânia – AGCMG, CNPJ nº 10.498.531/0001-00.",
                    "EMPRESA CONTRATADA": "SOLUTI – Soluções Em Negócios Inteligentes S/A, CNPJ nº 09.461.647/0001-95.",
                    "VALOR TOTAL": "R$ 210,00 (Duzentos e dez reais).",
                },
                "source_text": "\n\n\n                                                                    Agência da Guarda Civil Metropolitana de Goiânia\n\n\n\n\n                                      EXTRATO DE ATO DE DISPENSA DE LICITAÇÃO\n\n\n\n\n         - PROCESSO: 390/2018.\n         - LOCAL E DATA: Goiânia, 07 de março de 2018.\n         - OBJETO: Trata o presente de Ato de Dispensa de Licitação prevista no artigo 24 inciso II da\n         Lei nº 8.666 de 1993, tendo por objeto aquisição de Certificado Digital PJ1, para atender a\n         Comissão Municipal de Defesa Civil - COMDEC.\n         - ÓRGÃO CONTRATANTE: Agência da Guarda Civil Metropolitana de Goiânia – AGCMG,\n         CNPJ nº 10.498.531/0001-00.\n         - EMPRESA CONTRATADA: SOLUTI – Soluções Em Negócios Inteligentes S/A, CNPJ nº\n         09.461.647/0001-95.\n         - VALOR TOTAL: R$ 210,00 (Duzentos e dez reais).\n\n\n\n\n                                                    JOSÉ EULÁLIO VIEIRA\n                                                Presidente-Comandante da AGCMG\n\n\n\n\nAv. Nazareno Roriz, nº 66 – Setor Castelo Branco – CEP: 74405-010\nFone: (62) 3524-8661 – Fax: (62) 3524-1947\nE-mail: presidenteagmg@hotmail.com\n\n\n      Prefeitura de Goiânia/ Sup. da Casa Civil e Articulação Política - Assinado Digitalmente: www.goiania.go.gov.br\n\x0c      DOM Eletrônico                              Edição Nº 6772, de 14 de março de 2018.             ",
            },
            {
                "data": {
                    "PROCESSO": "388/2018.",
                    "LOCAL E DATA": "Goiânia, 07 de março de 2018.",
                    "OBJETO": "Trata o presente de Ato de Dispensa de Licitação prevista no artigo 24 inciso II da Lei nº 8.666 de 1993, tendo por objeto aquisição de Certificado Digital PJ1, para atender o Fundo Municipal da Guarda Civil Metropolitana - FMGCM.",
                    "ÓRGÃO CONTRATANTE": "Agência da Guarda Civil Metropolitana de Goiânia – AGCMG, CNPJ nº 10.498.531/0001-00.",
                    "EMPRESA CONTRATADA": "SOLUTI – Soluções Em Negócios Inteligentes S/A, CNPJ nº 09.461.647/0001-95.",
                    "VALOR TOTAL": "R$ 210,00 (Duzentos e dez reais).",
                },
                "source_text": "\n\n\n                                                                    Agência da Guarda Civil Metropolitana de Goiânia\n\n\n\n                                      EXTRATO DE ATO DE DISPENSA DE LICITAÇÃO\n\n\n\n\n         - PROCESSO: 388/2018.\n         - LOCAL E DATA: Goiânia, 07 de março de 2018.\n         - OBJETO: Trata o presente de Ato de Dispensa de Licitação prevista no artigo 24 inciso II da\n         Lei nº 8.666 de 1993, tendo por objeto aquisição de Certificado Digital PJ1, para atender o\n         Fundo Municipal da Guarda Civil Metropolitana - FMGCM.\n         - ÓRGÃO CONTRATANTE: Agência da Guarda Civil Metropolitana de Goiânia – AGCMG,\n         CNPJ nº 10.498.531/0001-00.\n         - EMPRESA CONTRATADA: SOLUTI – Soluções Em Negócios Inteligentes S/A, CNPJ nº\n         09.461.647/0001-95.\n         - VALOR TOTAL: R$ 210,00 (Duzentos e dez reais).\n\n\n\n\n                                                    JOSÉ EULÁLIO VIEIRA\n                                                Presidente-Comandante da AGCMG\n\n\n\n\nAv. Nazareno Roriz, nº 66 – Setor Castelo Branco – CEP: 74405-010\nFone: (62) 3524-8661 – Fax: (62) 3524-1947\nE-mail: presidenteagmg@hotmail.com\n\n\n      Prefeitura de Goiânia/ Sup. da Casa Civil e Articulação Política - Assinado Digitalmente: www.goiania.go.gov.br\n\x0cDOM Eletrônico                            Edição Nº 6772, de 14 de março de 2018.                 ",
            },
        ]
        self.assertEqual(expectation, exemptions)

    def test_bidding_exemptions_title_2(self):
        exemptions = subject_2().bidding_exemptions()
        exemptions = [exemption for exemption in exemptions]
        expectation = [
            {
                "data": {},
                "source_text": "\n\n\n\n\n                            TERMO DE DISPENSA DE LICITAÇÃO Nº 002/2018\n\n\n\n\n                    O DIRETOR FINANCEIRO DA CÂMARA MUNICIPAL DE GOIÂNIA, no\n uso de suas atribuições legais estabelecidas pela Portaria nº 219, de 14 de março de 2017, de acordo\n com o contido no Processo nº 2018/465 e com fundamento no artigo 24, XIII, da Lei Federal nº\n 8666, de 23 de junho de 1993.\n\n\n                    DECLARA             ser    DISPENSÁVEL               a    licitação   relativa   à   contratação   da\n UNIVERSIDADE FEDERAL DE GOIÁS – UFG, (CNPJ/MF: 01.567.601/0001-43), para\n realização do concurso público para provimento de cargos efetivos deste Poder Legislativo, no valor\n estimado de R$ 1.621.586,16 (Um milhão, seiscentos e vinte e um mil, quinhentos e oitenta e seis\n reais e dezesseis centavos).\n\n\n\n\n                    Câmara Municipal de Goiânia, aos 17 dias do mês de abril do ano de 2018.\n\n\n\n\n                                  FRADIQUE MACHADO DE MIRANDA DIAS\n                                            Diretor Financeiro\n\n\n\n\n Av.\xa0Goiás,\xa0nº\xa02001\xa0–\xa0Setor\xa0Norte\xa0Ferroviário\xa0–\xa0Goiânia‐GO\xa0CEP\xa074.063‐900\xa0\xa0\xa0\xa0\xa0\xa0\n Fone:\xa055\xa062\xa03524.4218|\xa0e‐mail:\xa0procuradoria@camaragyn.go.gov.br\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\n\nPrefeitura de Goiânia/ Sup. da Casa Civil e Articulação Política - Assinado Digitalmente: www.goiania.go.gov.br\n\x0cDOM Eletrônico                       Edição Nº 6797, de 20 de abril de 2018.                ",
            }
        ]
        self.assertEqual(expectation, exemptions)
