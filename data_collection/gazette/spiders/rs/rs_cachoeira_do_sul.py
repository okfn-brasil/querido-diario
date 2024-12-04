from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class RsCachoeiraDoSulSpider(BaseInstarSpider):
    TERRITORY_ID = "4303004"
    name = "rs_cachoeira_do_sul"
    allowed_domains = ["cachoeiradosul.rs.gov.br"]
    base_url = "https://www.cachoeiradosul.rs.gov.br/portal/diario-oficial"
    start_date = date(2021, 10, 27)
