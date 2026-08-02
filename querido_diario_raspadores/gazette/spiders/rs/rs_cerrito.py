from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class RsCerritoSpider(BaseInstarSpider):
    TERRITORY_ID = "4305124"
    name = "rs_cerrito"
    base_url = "https://www.cerrito.rs.gov.br/portal/diario-oficial"
    start_date = date(2019, 9, 9)
