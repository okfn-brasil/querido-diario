from datetime import date

from gazette.spiders.base.imprensa_oficial import BaseImprensaOficialSpider


class BaPeDeSerraSpider(BaseImprensaOficialSpider):
    name = "ba_pe_de_serra"
    allowed_domains = ["pmpedeserraba.imprensaoficial.org"]
    start_date = date(2017, 1, 1)
    url_base = "http://pmpedeserraba.imprensaoficial.org/{}"
    TERRITORY_ID = "2924058"
