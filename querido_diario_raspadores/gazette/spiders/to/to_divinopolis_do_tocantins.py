from datetime import date

from gazette.spiders.base.barcodigital import BaseBarcoDigitalSpider


class ToDivinopolisDoTocantins(BaseBarcoDigitalSpider):
    name = "to_divinopolis_do_tocantins"
    TERRITORY_ID = "1707108"
    base_url = "https://api-divinopolis.barcodigital.com.br"

    start_date = date(2021, 4, 29)
