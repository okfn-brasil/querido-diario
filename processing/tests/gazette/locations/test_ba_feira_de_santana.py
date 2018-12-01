import datetime
import json
import pytest

from gazette.locations.ba_feira_de_santana import BaFeiraDeSantana


class TestBaFeiraDeSantana:
    def test_bidding_exemptions_with_empty_text_is_empty(self):
        assert BaFeiraDeSantana("").bidding_exemptions() == []


class SampleGazetteScenario:
    ID_ATTRIBUTE = "NUMERO"
    # If the gazette PDF is "FOOBAR.pdf", the gazette ID is "FOOBAR"
    GAZETTE_ID = None

    @classmethod
    def setup_class(cls):
        assert cls.GAZETTE_ID is not None, "You must set the GAZETTE_ID constant"
        cls.TEXT = load_gazette(cls.GAZETTE_ID)
        cls.DATA = load_gazette_data(cls.GAZETTE_ID)

    def test_has_expected_count_of_bidding_exemptions(self):
        bidding_exemptions_ids = self.DATA["bidding_exemptions_ids"]
        expected_bidding_exemptions_count = len(bidding_exemptions_ids)

        bidding_exemptions = BaFeiraDeSantana(self.TEXT).bidding_exemptions()

        assert len(bidding_exemptions) == expected_bidding_exemptions_count

    def test_extracts_expected_bidding_exemptions_ids(self):
        expected_exemptions_ids = self.DATA["bidding_exemptions_ids"]

        bidding_exemptions = BaFeiraDeSantana(self.TEXT).bidding_exemptions()
        exemptions_ids = [
            exemption[self.ID_ATTRIBUTE]
            for exemption in bidding_exemptions
            if exemption[self.ID_ATTRIBUTE] is not None
        ]

        assert sorted(exemptions_ids) == sorted(expected_exemptions_ids)

    def test_bidding_exemptions(self):
        expected_bidding_exemptions = self.DATA["bidding_exemptions"]

        bidding_exemptions = BaFeiraDeSantana(self.TEXT).bidding_exemptions()

        for expected_exemption in expected_bidding_exemptions:
            exemption = [
                x
                for x in bidding_exemptions
                if x[self.ID_ATTRIBUTE] == expected_exemption[self.ID_ATTRIBUTE]
            ]
            msg = "Could not find bidding exemption '{}'"
            assert exemption, msg.format(expected_exemption[self.ID_ATTRIBUTE])
            exemption = {
                key: value for key, value in exemption[0].items() if value is not None
            }
            assert exemption == expected_exemption


class TestBaFeiraDeSantana12SO6Y982018(SampleGazetteScenario):
    GAZETTE_ID = "12SO6Y982018"

    def test_parsing_value_and_date_together(self):
        text = """Dispensa de Licitação Nº:671-2018-11D CONTRATANTE: PMFS/FUNDO MUNICIPAL DE SAÚDE DE FEIRA DE SANTANA,
OBJETO:Pagamento dos boletos do conselho regional de técnico em radiologia CONTRATADA: CONSELHO REGIONAL
DE TÉCNICOS EM RADIOLOGIA 8º RG VALOR(R$)R$ 182,4302/082018"""

        parser = BaFeiraDeSantana("")
        bidding_exemption = parser._parse_bidding_exemption(text)

        assert bidding_exemption["DATA"] == datetime.date(2018, 8, 2)
        assert bidding_exemption["VALOR"] == 182.43

    def test_parsing_value_multiline(self):
        text = """Dispensa de Licitação Nº: 647-2018-11D CONTRATANTE: PMFS/FUNDO MUNICIPAL DE SAÚDE DE FEIRA DE SANTANA,
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
        expected_section = """ Nº:671-2018-11D CONTRATANTE: PMFS/FUNDO MUNICIPAL DE SAÚDE DE FEIRA DE SANTANA,
OBJETO:Pagamento dos boletos do conselho regional de técnico em radiologia CONTRATADA: CONSELHO REGIONAL
DE TÉCNICOS EM RADIOLOGIA 8º RG VALOR(R$)R$ 182,43 02/08/2018"""

        parser = BaFeiraDeSantana(text)
        exemption_sections = parser._bidding_exemption_sections()

        assert exemption_sections[0] == expected_section


class TestBaFeiraDeSantana1CN1G31852018(SampleGazetteScenario):
    GAZETTE_ID = "1CN1G31852018"


@pytest.mark.skip()
class TestBaFeiraDeSantana1CQN162852018(SampleGazetteScenario):
    GAZETTE_ID = "1CQN162852018"


class TestBaFeiraDeSantana1GVUJB392018(SampleGazetteScenario):
    GAZETTE_ID = "1GVUJB392018"


@pytest.mark.skip()
class TestBaFeiraDeSantana1IMOPN1242018(SampleGazetteScenario):
    GAZETTE_ID = "1IMOPN1242018"


class TestBaFeiraDeSantana1L509N1332018(SampleGazetteScenario):
    GAZETTE_ID = "1L509N1332018"


@pytest.mark.skip()
class TestBaFeiraDeSantana1P2CXM1042018(SampleGazetteScenario):
    GAZETTE_ID = "1P2CXM1042018"


class TestBaFeiraDeSantana1TCJ74132018(SampleGazetteScenario):
    GAZETTE_ID = "1TCJ74132018"


@pytest.mark.skip()
class TestBaFeiraDeSantana1VQS3J252018(SampleGazetteScenario):
    GAZETTE_ID = "1VQS3J252018"


class TestBaFeiraDeSantana1X7HTY12112018(SampleGazetteScenario):
    GAZETTE_ID = "1X7HTY12112018"


class TestBaFeiraDeSantana1YTABV622018(SampleGazetteScenario):
    GAZETTE_ID = "1YTABV622018"


def load_gazette(gazette_id):
    path = "tests/gazette/fixtures/ba_feira_de_santana/{}.txt".format(gazette_id)
    with open(path) as fp:
        return fp.read()


def load_gazette_data(gazette_id):
    path = "tests/gazette/fixtures/ba_feira_de_santana/{}.json".format(gazette_id)
    with open(path) as fp:
        data = json.load(fp)
        for exemption in data["bidding_exemptions"]:
            exemption["DATA"] = datetime.datetime.strptime(
                exemption["DATA"], "%d/%m/%Y"
            ).date()
        return data
