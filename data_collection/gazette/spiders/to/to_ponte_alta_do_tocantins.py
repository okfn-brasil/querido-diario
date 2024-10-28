from datetime import date

from gazette.spiders.base.barcodigital import BaseBarcoDigitalSpider


class ToPonteAltaDoTocantins(BaseBarcoDigitalSpider):
    name = "to_ponte_alta_do_tocantins"
    TERRITORY_ID = "1717909"
    allowed_domains = ["api-ponte.barcodigital.com.br"]
    base_url = "https://api-ponte.barcodigital.com.br"

    start_date = date(2021, 4, 30)
