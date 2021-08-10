from datetime import date

from gazette.spiders.base.imprensa_oficial import ImprensaOficialSpider


class BaVeraCruzSpider(ImprensaOficialSpider):

    name = "ba_vera_cruz"
    allowed_domains = ["pmveracruzba.imprensaoficial.org"]
    start_date = date(2017, 4, 1)
    end_date = date.today()
    url_base = "http://pmveracruzba.imprensaoficial.org/{}"
    TERRITORY_ID = "2933208"
