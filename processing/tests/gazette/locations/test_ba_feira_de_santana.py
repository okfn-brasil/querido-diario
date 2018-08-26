import datetime
from unittest import TestCase

from gazette.locations.ba_feira_de_santana import BaFeiraDeSantana


class TestBaFeiraDeSantana(TestCase):
    def test_bidding_exemptions_with_empty_text_is_empty(self):
        assert BaFeiraDeSantana("").bidding_exemptions() == []

    def test_fixture_12SO6Y982018_has_19_bidding_exemptions(self):
        text = gazette_12SO6Y982018()
        expected_bidding_exemptions_count = 19

        bidding_exemptions = BaFeiraDeSantana(text).bidding_exemptions()

        assert len(bidding_exemptions) == expected_bidding_exemptions_count

    def test_fixture_12SO6Y982018_has_no_none_values(self):
        text = gazette_12SO6Y982018()

        bidding_exemptions = BaFeiraDeSantana(text).bidding_exemptions()

        for exemption in bidding_exemptions:
            values = exemption.values()
            assert None not in values, exemption

    def test_fixture_12SO6Y982018_extracts_exemptions_numbers(self):
        text = gazette_12SO6Y982018()
        expected_numbers = [
            "638-2018-11D",
            "639-2018-11D",
            "642-2018-11D",
            "646-2018-11D",
            "647-2018-11D",
            "648-2018-11D",
            "650-2018-11D",
            "651-2018-11D",
            "652-2018-11D",
            "653-2018-11D",
            "654-2018-11D",
            "655-2018-11D",
            "656-2018-11D",
            "657-2018-11D",
            "658-2018-11D",
            "659-2018-11D",
            "660-2018-11I",
            "661-2018-11D",
            "671-2018-11D",
        ]

        bidding_exemptions = BaFeiraDeSantana(text).bidding_exemptions()
        exemptions_numbers = [exemption["NUMERO"] for exemption in bidding_exemptions]

        assert sorted(exemptions_numbers) == sorted(
            expected_numbers
        ), exemptions_numbers

    def test_bidding_exemptions_fields_parsing(self):
        test_cases = [
            {
                "text": """Dispensa de Licitação Nº:638-2018-11DCONTRATANTE: PMFS/FUNDO MUNICIPAL DE SAÚDE DE FEIRA DE SANTANA,
OBJETO:Confecção de blocos de solicitação de exames e procedimentos para atender as necessidades da MAC e
Atenção Básica CONTRATADA: MASTER PAPELARIA EIRELLIVALOR(R$)R$ 9.600,00 01/08/2018""",
                "bidding_exemption": {
                    "NUMERO": "638-2018-11D",
                    "CONTRATANTE": "PMFS/FUNDO MUNICIPAL DE SAÚDE DE FEIRA DE SANTANA",
                    "OBJETO": "Confecção de blocos de solicitação de exames e procedimentos para atender as necessidades da MAC e Atenção Básica",
                    "CONTRATADA": "MASTER PAPELARIA EIRELLI",
                    "VALOR": 9600.00,
                    "DATA": datetime.date(2018, 8, 1),
                },
            },
            {
                "text": """Dispensa de Licitação Nº:671-2018-11D CONTRATANTE: PMFS/FUNDO MUNICIPAL DE SAÚDE DE FEIRA DE SANTANA,
OBJETO:Pagamento dos boletos do conselho regional de técnico em radiologia CONTRATADA: CONSELHO REGIONAL
DE TÉCNICOS EM RADIOLOGIA 8º RG VALOR(R$)R$ 182,43 02/082018""",
                "bidding_exemption": {
                    "NUMERO": "671-2018-11D",
                    "CONTRATANTE": "PMFS/FUNDO MUNICIPAL DE SAÚDE DE FEIRA DE SANTANA",
                    "OBJETO": "Pagamento dos boletos do conselho regional de técnico em radiologia",
                    "CONTRATADA": "CONSELHO REGIONAL DE TÉCNICOS EM RADIOLOGIA 8º RG",
                    "VALOR": 182.43,
                    "DATA": datetime.date(2018, 8, 2),
                },
            },
        ]

        parser = BaFeiraDeSantana("")

        for test_case in test_cases:
            text = test_case["text"]
            expected_bidding_exemption = test_case["bidding_exemption"]

            bidding_exemption = parser._parse_bidding_exemption(text)

            assert bidding_exemption == expected_bidding_exemption, bidding_exemption

    def test_parsing_value_and_date_together(self):
        text = """Dispensa de Licitação Nº:671-2018-11D CONTRATANTE: PMFS/FUNDO MUNICIPAL DE SAÚDE DE FEIRA DE SANTANA,
OBJETO:Pagamento dos boletos do conselho regional de técnico em radiologia CONTRATADA: CONSELHO REGIONAL
DE TÉCNICOS EM RADIOLOGIA 8º RG VALOR(R$)R$ 182,4302/082018"""

        parser = BaFeiraDeSantana("")
        bidding_exemption = parser._parse_bidding_exemption(text)

        assert bidding_exemption["DATA"] == datetime.date(2018, 8, 2)
        assert bidding_exemption["VALOR"] == 182.43

    def test_parsing_value_multiline(self):
        text = """
Dispensa de Licitação Nº: 647-2018-11D CONTRATANTE: PMFS/FUNDO MUNICIPAL DE SAÚDE DE FEIRA DE SANTANA,
OBJETO: Aquisição de medicamento para atender ao solicitado no mandado judicial Nº8000748-51.2018.8.05.0000 da
paciente Ivoneide Silva de Jesus Santos CONTRATADA: FABMED DISTRIBUIDORA HOSPITALAR LTDA –MEVALOR R$
8.022,00 02/08/2018"""

        parser = BaFeiraDeSantana("")
        bidding_exemption = parser._parse_bidding_exemption(text)

        assert bidding_exemption["VALOR"] == 8022.0

    def test_split_bidding_exemptions_sections(self):
        text = """Dispensa de Licitação Nº:671-2018-11D CONTRATANTE: PMFS/FUNDO MUNICIPAL DE SAÚDE DE FEIRA DE SANTANA,
OBJETO:Pagamento dos boletos do conselho regional de técnico em radiologia CONTRATADA: CONSELHO REGIONAL
DE TÉCNICOS EM RADIOLOGIA 8º RG VALOR(R$)R$ 182,43 02/08/2018



                                                  ANTONIO ROSA DE ASSIS
                                               PREGOEIRO/PRESIDENTE DA CPL"""

        expected_sections = [
            """ Nº:671-2018-11D CONTRATANTE: PMFS/FUNDO MUNICIPAL DE SAÚDE DE FEIRA DE SANTANA,
OBJETO:Pagamento dos boletos do conselho regional de técnico em radiologia CONTRATADA: CONSELHO REGIONAL
DE TÉCNICOS EM RADIOLOGIA 8º RG VALOR(R$)R$ 182,43 02/08/2018"""
        ]

        parser = BaFeiraDeSantana(text)
        exemption_sections = parser._bidding_exemption_sections()

        assert exemption_sections == expected_sections, exemption_sections


def gazette_12SO6Y982018():
    path = "tests/gazette/fixtures/ba_feira_de_santana_12SO6Y982018.txt"
    with open(path) as fp:
        return fp.read()
