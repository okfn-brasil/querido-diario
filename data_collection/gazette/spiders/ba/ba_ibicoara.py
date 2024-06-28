from datetime import date

from gazette.spiders.base.brtransparencia import BaseBrTransparenciaSpider


class BaIbicoaraSpider(BaseBrTransparenciaSpider):
    name = "ba_ibicoara"
    TERRITORY_ID = "2912202"
    allowed_domains = ["www.camaraibicoara.ba.gov.br"]
    start_urls = ["https://www.camaraibicoara.ba.gov.br/diario.html"]
    start_date = date(2020, 2, 1)
    br_tranparencia_entity = "691bea32-9b9f-40f8-ab18-31e079080a1a"
    br_tranparencia_code = "CODE_ENT_CM204"
