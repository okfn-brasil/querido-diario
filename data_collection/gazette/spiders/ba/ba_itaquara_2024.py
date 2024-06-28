from datetime import date

from gazette.spiders.base.brtransparencia import BaseBrTransparenciaSpider


class BaItaquaraSpider(BaseBrTransparenciaSpider):
    name = "ba_itaquara_2024"
    TERRITORY_ID = "2916708"
    allowed_domains = ["www.itaquara.ba.gov.br"]
    start_urls = ["https://www.itaquara.ba.gov.br/diario.html"]
    start_date = date(2019, 1, 1)
    br_tranparencia_entity = "1557447a-9381-44ad-9c0f-016868769479"
    br_tranparencia_code = "CODE_ENT_PM003"
