from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class SpItapiraSpider(BaseDospSpider):
    TERRITORY_ID = "3522604"
    name = "sp_itapira"
    start_urls = ["https://www.imprensaoficialmunicipal.com.br/itapira"]
    start_date = date(2011, 9, 16)
