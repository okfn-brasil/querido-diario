from datetime import date

from gazette.spiders.base.imprensa_oficial import ImprensaOficialSpider


class BaJaguarariSpider(ImprensaOficialSpider):

    name = "ba_jaguarari"
    allowed_domains = ["pmjaguarariba.imprensaoficial.org"]
    start_date = date(2019, 10, 1)
    end_date = date(2020, 12, 31)
    url_base = "http://pmjaguarariba.imprensaoficial.org/{}"
    TERRITORY_ID = "2917706"
