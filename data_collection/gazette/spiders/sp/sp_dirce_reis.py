from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpDirceReisSpider(BaseInstarSpider):
    TERRITORY_ID = "3513850"
    name = "sp_dirce_reis"
    allowed_domains = ["dircereis.sp.gov.br"]
    base_url = "https://www.dircereis.sp.gov.br/portal/diario-oficial"
    start_date = date(2019, 10, 7)
