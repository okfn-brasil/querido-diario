from unittest import TestCase
from unittest.mock import MagicMock, PropertyMock, patch

from gazette.data.bidding_exemption_parsing import BiddingExemptionParsing


class TestBiddingExemptionParsing(TestCase):

    def setUp(self):
        session = MagicMock()
        self.subject = BiddingExemptionParsing(session)

    @patch.object(BiddingExemptionParsing, 'update_object')
    @patch.object(BiddingExemptionParsing, 'update_value')
    @patch.object(BiddingExemptionParsing, 'update_contracted_code')
    def test_update_calls_update_object(self, _code, _value, update):
        gazette = MagicMock(municipality_id='4314902')
        exemptions = [MagicMock(gazette=gazette), MagicMock(gazette=gazette)]
        self.subject.update(exemptions)
        update.assert_called()

    @patch.object(BiddingExemptionParsing, 'update_value')
    @patch.object(BiddingExemptionParsing, 'update_contracted_code')
    def test_update_calls_update_value(self, _code, update):
        gazette = MagicMock(municipality_id='4314902')
        exemptions = [MagicMock(gazette=gazette), MagicMock(gazette=gazette)]
        self.subject.update(exemptions)
        update.assert_called()

    @patch.object(BiddingExemptionParsing, 'update_value')
    @patch.object(BiddingExemptionParsing, 'update_contracted')
    @patch.object(BiddingExemptionParsing, 'update_contracted_code')
    def test_update_calls_update_contracted(self, _value, _code, update):
        gazette = MagicMock(municipality_id='4314902')
        exemptions = [MagicMock(gazette=gazette), MagicMock(gazette=gazette)]
        self.subject.update(exemptions)
        update.assert_called()

    @patch.object(BiddingExemptionParsing, 'update_value')
    @patch.object(BiddingExemptionParsing, 'update_contracted_code')
    def test_update_calls_update_contracted_code(self, _value, update):
        gazette = MagicMock(municipality_id='4314902')
        exemptions = [MagicMock(gazette=gazette), MagicMock(gazette=gazette)]
        self.subject.update(exemptions)
        update.assert_called()

    def test_update_changes_is_parsed_to_true(self):
        gazette = MagicMock(municipality_id='4314902')
        exemptions = [
            MagicMock(
                gazette=gazette,
                is_parsed=False,
                municipality_id='4314902',
                source_text='',
            ),
            MagicMock(
                gazette=gazette,
                is_parsed=False,
                municipality_id='4314902',
                source_text='',
            ),
        ]
        self.subject.update(exemptions)
        for exemption in exemptions:
            self.assertEqual(True, exemption.is_parsed)

    def test_update_object_using_label(self):
        object = 'Aquisição de 05 (cinco) cabos HDMI 2.0 com 10 metros cada.'
        exemption = MagicMock(data={'OBJETO': object})
        self.subject.update_object(exemption)
        self.assertEqual(object, exemption.object)

    def test_update_object_using_label_with_introduction_1(self):
        object = 'Trata o Presente de Ato de Dispensa de Licitação prevista no artigo 24 inciso II da Lei 8.666 de 1993 tendo por objeto a aquisição de serviços de dedetização, desratização e limpeza da caixa d’água das áreas I e II da AGCMG;'
        exemption = MagicMock(data={'OBJETO': object})
        self.subject.update_object(exemption)
        self.assertEqual(
            'serviços de dedetização, desratização e limpeza da caixa d’água das áreas I e II da AGCMG;',
            exemption.object,
        )

    def test_update_object_using_label_with_introduction_2(self):
        object = 'Trata o presente de Ato de Dispensa de Licitação prevista no artigo 24 inciso II da Lei nº 8.666 de 1993, tendo por objeto aquisição de Certificado Digital PJ1, para atender o Fundo Municipal da Guarda Civil Metropolitana - FMGCM.'
        exemption = MagicMock(data={'OBJETO': object})
        self.subject.update_object(exemption)
        self.assertEqual(
            'Certificado Digital PJ1, para atender o Fundo Municipal da Guarda Civil Metropolitana - FMGCM.',
            exemption.object,
        )

    def test_update_value_label_1(self):
        value = 'R$ 4.064,10 (Quatro mil, sessenta e quatro reais e dez centavos).'
        exemption = MagicMock(data={'VALOR TOTAL': value})
        self.subject.update_value(exemption)
        self.assertEqual(4064.1, exemption.value)

    def test_update_value_label_2(self):
        value = 'R$ 4.064,10 (Quatro mil, sessenta e quatro reais e dez centavos).'
        exemption = MagicMock(data={'ORÇAMENTO PREVISTO': value})
        self.subject.update_value(exemption)
        self.assertEqual(4064.1, exemption.value)

    def test_update_value_label_3(self):
        value = 'R$ 4.064,10 (Quatro mil, sessenta e quatro reais e dez centavos).'
        exemption = MagicMock(data={'PREÇO TOTAL': value})
        self.subject.update_value(exemption)
        self.assertEqual(4064.1, exemption.value)

    def test_update_value_specific_case_with_multiple_commas(self):
        exemption = MagicMock(
            data={'PREÇO TOTAL': 'R$ 660,00,00 (seiscentos e sessenta reais)'}
        )
        self.subject.update_value(exemption)
        self.assertEqual(660., exemption.value)

    def test_update_contracted_label_1(self):
        exemption = MagicMock(data={'CONTRATADO': 'Petrobras'})
        self.subject.update_contracted(exemption)
        self.assertEqual('Petrobras', exemption.contracted)

    def test_update_contracted_label_2(self):
        exemption = MagicMock(data={'EMPRESAS CONTRATADAS': 'Petrobras'})
        self.subject.update_contracted(exemption)
        self.assertEqual('Petrobras', exemption.contracted)

    def test_update_contracted_label_3(self):
        exemption = MagicMock(data={'EMPRESA BENEFICIADA': 'Petrobras'})
        self.subject.update_contracted(exemption)
        self.assertEqual('Petrobras', exemption.contracted)

    def test_update_contracted_label_4(self):
        exemption = MagicMock(data={'FORNECEDOR': 'Petrobras'})
        self.subject.update_contracted(exemption)
        self.assertEqual('Petrobras', exemption.contracted)

    def test_update_contracted_label_5(self):
        exemption = MagicMock(data={'LOCADOR': 'Petrobras'})
        self.subject.update_contracted(exemption)
        self.assertEqual('Petrobras', exemption.contracted)

    def test_update_contracted_code_from_contracted(self):
        exemption = MagicMock(contracted='BR GÁS LTDA-ME, CNPJ nº 08.926.037/0001-57.')
        self.subject.update_contracted_code(exemption)
        self.assertEqual('08926037000157', exemption.contracted_code)

    def test_update_contracted_code_from_source_text(self):
        exemption = MagicMock(
            contracted=None,
            source_text='- EMPRESAS CONTRATADAS: BR GÁS LTDA-ME, CNPJ nº 08.926.037/0001-57.\n- VALOR TOTAL: R$ 3.240,00 (Três mil, duzentos e quarenta reais).',
        )
        self.subject.update_contracted_code(exemption)
        self.assertEqual('08926037000157', exemption.contracted_code)

    def test_update_contracted_code_when_cnpj_is_not_present(self):
        exemption = MagicMock(
            contracted=None,
            contracted_code=None,
            source_text='- EMPRESAS CONTRATADAS: BR GÁS LTDA-ME.\n- VALOR TOTAL: R$ 3.240,00 (Três mil, duzentos e quarenta reais).',
        )
        self.subject.update_contracted_code(exemption)
        self.assertIsNone(exemption.contracted_code)

    def test_update_contracted_code_when_multiple_cnpjs_in_source_text(self):
        exemption = MagicMock(
            contracted=None,
            contracted_code=None,
            source_text='- ÓRGÃO CONTRATANTE: Agência da Guarda Civil Metropolitana de Goiânia – AGCMG,\n         CNPJ nº 57.494.031/0010-54.\n         - EMPRESAS CONTRATADAS: REDE EPI EQUIPAMENTOS DE SEGURANÇA EIRELI,\n         CNPJ nº 18.428.558/0001-38.',
        )
        self.subject.update_contracted_code(exemption)
        self.assertIsNone(exemption.contracted_code)
