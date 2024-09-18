from datetime import date

from gazette.spiders.base.imprensa_oficial import ImprensaOficialSpider


class BaParatingaSpider(ImprensaOficialSpider):
    name = "ba_paratinga"
    allowed_domains = ["pmparatingaba.imprensaoficial.org"]
    start_date = date(2018, 4, 1)
    city_domain = "http://pmparatingaba.imprensaoficial.org"
    TERRITORY_ID = "2923704"
