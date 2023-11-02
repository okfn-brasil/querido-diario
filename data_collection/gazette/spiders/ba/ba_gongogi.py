from datetime import date

from gazette.spiders.base.imprensa_oficial import ImprensaOficialSpider


class BaGongogiSpider(ImprensaOficialSpider):
    name = "ba_gongogi"
    allowed_domains = ["pmgongogiba.imprensaoficial.org"]
    start_date = date(2020, 2, 1)
    end_date = date(2020, 12, 30)
    url_base = "http://pmgongogiba.imprensaoficial.org/{}"
    TERRITORY_ID = "2911501"
