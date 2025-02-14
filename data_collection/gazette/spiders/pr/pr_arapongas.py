from datetime import date

from gazette.spiders.base.atende_v2 import BaseAtendeV2Spider


class PrArapongasSpider(BaseAtendeV2Spider):
    TERRITORY_ID = "4101507"
    name = "pr_arapongas"
    city_subdomain = "arapongas"
    start_date = date(2009, 2, 11)
