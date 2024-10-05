from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class MtCotriguacuSpider(BaseInstarSpider):
    TERRITORY_ID = "5103379"
    name = "mt_cotriguacu"
    allowed_domains = ["cotriguacu.mt.gov.br"]
    base_url = "https://www.cotriguacu.mt.gov.br/portal/diario-oficial"
    start_date = date(2023, 11, 17)
