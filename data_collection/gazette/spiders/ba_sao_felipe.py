from datetime import date

from gazette.spiders.base.imprensa_oficial import ImprensaOficialSpider


class BaSaoFelipeSpider(ImprensaOficialSpider):

    name = "ba_sao_felipe"
    allowed_domains = ["pmsaofelipeba.imprensaoficial.org"]
    start_date = date(2020, 1, 1)
    end_date = date(2021, 4, 22)
    url_base = "http://pmsaofelipeba.imprensaoficial.org/{}"
    TERRITORY_ID = "2929107"
