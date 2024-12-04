from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class RsVeraCruzSpider(BaseInstarSpider):
    TERRITORY_ID = "4322707"
    name = "rs_vera_cruz"
    allowed_domains = ["veracruz.rs.gov.br"]
    base_url = "https://www.veracruz.rs.gov.br/portal/diario-oficial"
    start_date = date(2018, 5, 2)
