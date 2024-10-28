from datetime import date

from gazette.spiders.base.barcodigital import BaseBarcoDigitalSpider


class toBrejinhoDeNazare(BaseBarcoDigitalSpider):
    name = "to_brejinho_de_nazare"
    TERRITORY_ID = "1703701"
    allowed_domains = ["api-nazare.barcodigital.com.br"]
    base_url = "https://api-nazare.barcodigital.com.br"

    start_date = date(year=2017, month=3, day=7)
