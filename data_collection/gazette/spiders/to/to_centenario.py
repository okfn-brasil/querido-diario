from datetime import date

from gazette.spiders.base.barcodigital import BaseBarcoDigitalSpider


class ToCentenario(BaseBarcoDigitalSpider):
    name = "to_centenario"
    TERRITORY_ID = "1704105"
    allowed_domains = ["api-centenario.barcodigital.com.br"]
    base_url = "https://api-centenario.barcodigital.com.br"

    start_date = date(2015, 9, 9)
