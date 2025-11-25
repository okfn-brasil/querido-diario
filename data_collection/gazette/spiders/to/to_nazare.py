from datetime import date

from gazette.spiders.base.barcodigital import BaseBarcoDigitalSpider


class ToNazare(BaseBarcoDigitalSpider):
    name = "to_nazare"
    TERRITORY_ID = "1714302"
    base_url = "https://api-nazare.barcodigital.com.br"

    start_date = date(year=2017, month=3, day=7)
