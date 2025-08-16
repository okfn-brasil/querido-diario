from datetime import date

from gazette.spiders.base.brtransparencia import BaseBrTransparenciaSpider


class BaIbicoaraSpider(BaseBrTransparenciaSpider):
    name = "ba_ibicoara"
    TERRITORY_ID = "2912202"
    allowed_domains = ["www.camaraibicoara.ba.gov.br", "api.brtransparencia.com.br"]
    start_urls = ["https://www.camaraibicoara.ba.gov.br/diario.html"]
    start_date = date(2020, 2, 1)
