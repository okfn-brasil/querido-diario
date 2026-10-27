from datetime import date

from gazette.spiders.base.govweb import BaseGovWebSpider


class ToTalismaSpider(BaseGovWebSpider):
    TERRITORY_ID = "1720978"
    name = "to_talisma"
    base_url = "https://www.talisma.to.gov.br"
    start_date = date(2020, 1, 2)
