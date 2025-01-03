from datetime import date

from gazette.spiders.base.atende_v2 import BaseAtendeV2Spider


class PrCampoMouraoSpider(BaseAtendeV2Spider):
    TERRITORY_ID = "4104303"
    name = "pr_campo_mourao"
    city_subdomain = "campomourao"
    start_date = date(2012, 2, 3)
