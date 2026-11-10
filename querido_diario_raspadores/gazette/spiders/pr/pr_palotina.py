from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class PrPalotinaSpider(BaseInstarSpider):
    TERRITORY_ID = "4117909"
    name = "pr_palotina"
    base_url = "https://www.palotina.siteparaprefeituras.com.br/portal/diario-oficial"
    start_date = date(2012, 2, 2)
