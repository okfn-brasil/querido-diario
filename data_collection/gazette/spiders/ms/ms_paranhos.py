from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class MsParanhosSpider(BaseDospSpider):
    TERRITORY_ID = "5006358"
    name = "ms_paranhos"
    start_urls = ["https://www.imprensaoficialmunicipal.com.br/paranhos"]
    start_date = date(2023, 7, 13)
