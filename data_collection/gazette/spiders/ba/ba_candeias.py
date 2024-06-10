from datetime import date

from gazette.spiders.base.brtransparencia import BaseBrTransparenciaSpider


class BaCandeiasSpider(BaseBrTransparenciaSpider):
    name = "ba_candeias"
    TERRITORY_ID = "2906501"
    allowed_domains = ["www.camaraibicoara.ba.gov.br"]
    start_urls = ["https://www.camaraibicoara.ba.gov.br/diario.html"]
    start_date = date(2022, 12, 29)
    br_tranparencia_entity = "63147391-dcb2-4d6c-9c5a-c4483a9d8306"
    br_tranparencia_code = "CODE_ENT_CM207"
