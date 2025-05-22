from datetime import date

from gazette.spiders.base.barcodigital import BaseBarcoDigitalSpider


class ToLagoaDoTocatinsSpider(BaseBarcoDigitalSpider):
    name = "to_lagoa_do_tocantins"
    TERRITORY_ID = "1711951"
    allowed_domains = ["api-lagoadotocantins.barcodigital.com.br"]
    base_url = "https://api-lagoadotocantins.barcodigital.com.br"

    start_date = date(year=2018, month=5, day=1)
