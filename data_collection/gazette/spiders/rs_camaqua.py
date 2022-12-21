import datetime
from gazette.spiders.base.instar import BaseInstarSpider


class RsCamaquaSpider(BaseInstarSpider):
    TERRITORY_ID = "4303509"
    name = "rs_camaqua"
    allowed_domains = ["camaqua.rs.gov.br"]
    base_url = "https://www.camaqua.rs.gov.br/portal/diario-oficial"
    start_date = datetime.date(2019, 7, 25)
