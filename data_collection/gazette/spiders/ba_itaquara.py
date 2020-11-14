from datetime import date

from gazette.spiders.base import ImprensaOficialSpider


class BaItaquaraSpider(ImprensaOficialSpider):

    name = "ba_itaquara"
    allowed_domains = ["pmITAQUARABA.imprensaoficial.org", "itaquara.ba.gov.br"]
    start_date = date(2019, 1, 1)
    url_base = "http://itaquara.ba.gov.br/{}/"
    TERRITORY_ID = "2916708"
