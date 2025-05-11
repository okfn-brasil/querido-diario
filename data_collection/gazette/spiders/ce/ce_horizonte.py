from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class CeHorizonteSpider(BaseDospSpider):
    name = "ce_horizonte"
    PUBLIC_ENTITY_ID = "2305233"
    GAZETTES_PAGE_URL = "https://imprensaoficialmunicipal.com.br/horizonte"
    start_date = date(2023, 7, 3)
