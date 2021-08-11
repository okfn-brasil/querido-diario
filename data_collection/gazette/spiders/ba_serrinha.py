from datetime import date

from gazette.spiders.base.imprensa_oficial import ImprensaOficialSpider


class BaSerrinhaSpider(ImprensaOficialSpider):

    name = "ba_serrinha"
    allowed_domains = ["pmserrinhaba.imprensaoficial.org"]
    start_date = date(2020, 1, 1)
    end_date = date.today()
    url_base = "http://pmserrinhaba.imprensaoficial.org/{}"
    TERRITORY_ID = "2930501"
