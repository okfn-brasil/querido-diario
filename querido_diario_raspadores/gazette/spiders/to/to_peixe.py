from datetime import date

from gazette.spiders.base.govweb import BaseGovWebSpider


class ToPeixeSpider(BaseGovWebSpider):
    TERRITORY_ID = "1716604"
    name = "to_peixe"
    base_url = "https://www.peixe.to.gov.br"
    start_date = date(2022, 3, 30)
