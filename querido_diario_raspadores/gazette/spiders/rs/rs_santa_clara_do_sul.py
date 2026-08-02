from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class RsSantaClaraDoSulSpider(BaseDospSpider):
    TERRITORY_ID = "4316758"
    name = "rs_santa_clara_do_sul"
    start_urls = ["https://www.imprensaoficialmunicipal.com.br/santa_clara_do_sul"]
    start_date = date(2017, 9, 5)
