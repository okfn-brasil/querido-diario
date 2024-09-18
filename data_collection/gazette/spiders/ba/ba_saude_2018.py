from datetime import date

from gazette.spiders.base.imprensa_oficial import ImprensaOficialSpider


class BaSaudeSpider(ImprensaOficialSpider):
    name = "ba_saude_2018"
    allowed_domains = ["pmsaudeba.imprensaoficial.org"]
    start_date = date(2018, 2, 1)
    end_date = date(2019, 4, 12)
    city_domain = "http://pmsaudeba.imprensaoficial.org"
    TERRITORY_ID = "2929800"
