from datetime import date

from gazette.spiders.base.imprensa_oficial import BaseImprensaOficialSpider


class BaXiqueXiqueSpider(BaseImprensaOficialSpider):
    name = "ba_xique_xique"
    allowed_domains = ["pmxiquexiqueba.imprensaoficial.org"]
    start_date = date(2017, 1, 1)
    url_base = "http://pmxiquexiqueba.imprensaoficial.org/{}"
    TERRITORY_ID = "2933604"
