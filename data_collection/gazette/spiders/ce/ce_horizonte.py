from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class CeHorizonteSpider(BaseDospSpider):
    PUBLIC_ENTITY_ID = "2305233"
    user_website = "https://imprensaoficialmunicipal.com.br/horizonte"
    name = "ce_horizonte"
    code = 687
    start_date = date(2023, 7, 3)
