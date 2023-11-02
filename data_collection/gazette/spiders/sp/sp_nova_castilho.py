from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpNovaCastilhoSpider(BaseInstarSpider):
    TERRITORY_ID = "3532868"
    name = "sp_nova_castilho"
    allowed_domains = ["novacastilho.sp.gov.br"]
    base_url = "https://www.novacastilho.sp.gov.br/portal/diario-oficial"
    start_date = date(2021, 1, 29)
