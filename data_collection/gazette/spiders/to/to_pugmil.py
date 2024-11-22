from datetime import date

from gazette.spiders.base.barcodigital import BaseBarcoDigitalSpider


class ToPugmil(BaseBarcoDigitalSpider):
    name = "to_pugmil"
    TERRITORY_ID = "1718451"
    allowed_domains = ["api-pugmil.barcodigital.com.br"]
    base_url = "https://api-pugmil.barcodigital.com.br"

    start_date = date(2017, 9, 29)
