from datetime import date

from gazette.spiders.base.govweb import BaseGovWebSpider


class ToTocantiniaSpider(BaseGovWebSpider):
    TERRITORY_ID = "1721109"
    name = "to_tocantinia"
    base_url = "https://www.tocantinia.to.gov.br"
    start_date = date(2017, 3, 21)
