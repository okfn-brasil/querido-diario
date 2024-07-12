from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpPatrocinioPaulistaSpider(BaseInstarSpider):
    TERRITORY_ID = "3536307"
    name = "sp_patrocinio_paulista"
    allowed_domains = ["patrociniopaulista.sp.gov.br"]
    base_url = "https://www.patrociniopaulista.sp.gov.br/portal/diario-oficial"
    start_date = date(2017, 8, 18)
