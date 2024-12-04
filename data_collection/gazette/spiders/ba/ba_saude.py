from datetime import date

from gazette.spiders.base.imprensa_oficial import BaseImprensaOficialSpider


class BaSaudeSpider(BaseImprensaOficialSpider):
    name = "ba_saude"
    allowed_domains = ["pmsaudeba.imprensaoficial.org"]
    start_date = date(2018, 2, 1)
    end_date = date(2019, 4, 12)
    url_base = "http://pmsaudeba.imprensaoficial.org/{}"
    TERRITORY_ID = "2929800"
