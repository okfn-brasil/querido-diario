from datetime import date

from gazette.spiders.base.govweb import BaseGovWebSpider


class ToMuricilandiaSpider(BaseGovWebSpider):
    TERRITORY_ID = "1713957"
    name = "to_muricilandia"
    base_url = "https://www.muricilandia.to.gov.br"
    start_date = date(2019, 7, 2)
