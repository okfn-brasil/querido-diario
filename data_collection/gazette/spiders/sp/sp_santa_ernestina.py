from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpSantaErnestinaSpider(BaseInstarSpider):
    TERRITORY_ID = "3546504"
    name = "sp_santa_ernestina"
    allowed_domains = ["santaernestina.sp.gov.br"]
    base_url = "https://www.santaernestina.sp.gov.br/portal/diario-oficial"
    start_date = date(2019, 8, 19)
