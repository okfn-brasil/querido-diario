from datetime import date

from gazette.spiders.base.imprensa_oficial import BaseImprensaOficialSpider


class BaGentioDoOuroSpider(BaseImprensaOficialSpider):
    name = "ba_gentio_do_ouro"
    start_date = date(2017, 2, 1)
    url_base = "http://pmgentiodoouroba.imprensaoficial.org/{}"
    TERRITORY_ID = "2911303"
