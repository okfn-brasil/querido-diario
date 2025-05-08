from datetime import date

from gazette.spiders.base.imprensa_oficial import BaseImprensaOficialSpider


class BaSerrinhaSpider(BaseImprensaOficialSpider):
    name = "ba_serrinha"
    start_date = date(2020, 1, 1)
    url_base = "http://pmserrinhaba.imprensaoficial.org/{}"
    TERRITORY_ID = "2930501"
