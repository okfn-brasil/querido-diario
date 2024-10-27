from datetime import date

from gazette.spiders.base.barcodigital import BaseBarcoDigitalSpider


class toPonteAltaDoTocantins(BaseBarcoDigitalSpider):
    name = "to_ponte_alta_do_tocantins"
    TERRITORY_ID = "1717909"
    allowed_domains = ["api-pontealtadotocantins.barcodigital.com.br"]
    base_url = "https://api-pontealtadotocantins.barcodigital.com.br"

    start_date = date(year=2018, month=5, day=9)
