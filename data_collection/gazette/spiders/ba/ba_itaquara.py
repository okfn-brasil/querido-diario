from datetime import date

from gazette.spiders.base.imprensa_oficial import BaseImprensaOficialSpider


class BaItaquaraSpider(BaseImprensaOficialSpider):
    name = "ba_itaquara"
    start_date = date(2019, 1, 1)
    url_base = "http://itaquara.ba.gov.br/{}"
    TERRITORY_ID = "2916708"
