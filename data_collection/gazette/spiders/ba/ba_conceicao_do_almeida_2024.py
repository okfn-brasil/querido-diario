from datetime import date

from gazette.spiders.base.brtransparencia import BaseBrTransparenciaSpider


class BaConceicaoDoAlmeidaSpider(BaseBrTransparenciaSpider):
    name = "ba_conceicao_do_almeida_2024"
    TERRITORY_ID = "2908309"
    allowed_domains = ["www.conceicaodoalmeida.ba.gov.br"]
    start_urls = ["https://www.conceicaodoalmeida.ba.gov.br/diario.html"]
    start_date = date(2019, 5, 3)
    br_tranparencia_entity = "EF1662F7-9A2A-4FDB-ABAD-346211F97734"
    br_tranparencia_code = "CODE_ENT_001"
