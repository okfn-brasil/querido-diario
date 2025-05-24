from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class RsCamaquaSpider(BaseInstarSpider):
    TERRITORY_ID = "4303509"
    name = "rs_camaqua"
    base_url = "https://www.camaqua.rs.gov.br/portal/diario-oficial"
    start_date = date(2019, 7, 25)
    end_date = date(2023, 7, 19)
