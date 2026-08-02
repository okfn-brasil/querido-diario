from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class PrCafezalDoSulSpider(BaseDospSpider):
    TERRITORY_ID = "4103479"
    name = "pr_cafezal_do_sul"
    start_urls = ["https://www.imprensaoficialmunicipal.com.br/cafezal_do_sul"]
    start_date = date(2016, 4, 14)
