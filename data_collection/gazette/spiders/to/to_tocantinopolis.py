from datetime import date

from gazette.spiders.base.barcodigital import BaseBarcoDigitalSpider


class ToTocantinopolisSpider(BaseBarcoDigitalSpider):
    name = "to_tocantinopolis"
    TERRITORY_ID = "1721208"
    base_url = "https://api-tocantinopolis.barcodigital.com.br"

    start_date = date(year=2017, month=5, day=17)
