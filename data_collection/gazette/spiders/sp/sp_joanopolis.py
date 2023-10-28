from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpJoanopolisSpider(BaseInstarSpider):
    TERRITORY_ID = "3525508"
    name = "sp_joanopolis"
    allowed_domains = ["joanopolis.sp.gov.br"]
    base_url = "https://www.joanopolis.sp.gov.br/portal/diario-oficial"
    start_date = date(2013, 1, 30)
