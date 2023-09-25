import datetime as dt

from gazette.spiders.base.doem import DoemGazetteSpider


class PePetrolinaSpider(DoemGazetteSpider):
    TERRITORY_ID = "2611101"
    name = "pe_petrolina"
    start_date = dt.date(2014, 3, 6)
    state_city_url_part = "pe/petrolina"
