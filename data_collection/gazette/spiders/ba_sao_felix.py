from datetime import date

from gazette.spiders.base.imprensa_oficial import ImprensaOficialSpider


class BaSaoFelixSpider(ImprensaOficialSpider):

    name = "ba_sao_felix"
    allowed_domains = ["pmsaofelixba.imprensaoficial.org"]
    start_date = date(2017, 1, 1)
    end_date = date(2021, 2, 8)
    url_base = "http://pmsaofelixba.imprensaoficial.org/{}"
    TERRITORY_ID = "2929008"
