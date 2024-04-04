from datetime import date

from gazette.spiders.base.imprensa_oficial import ImprensaOficialSpider


class BaItaquaraSpider(ImprensaOficialSpider):
    name = "ba_itaquara"
    allowed_domains = ["pmitaquaraba.imprensaoficial.org"]
    start_date = date(2019, 1, 1)
    city_domain = "http://pmitaquaraba.imprensaoficial.org"
    TERRITORY_ID = "2916708"
