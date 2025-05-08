from datetime import date

from gazette.spiders.base.barcodigital import BaseBarcoDigitalSpider


class ToAraguainaSpider(BaseBarcoDigitalSpider):
    name = "to_araguaina"
    TERRITORY_ID = "1702109"
    base_url = "https://api-araguaina.barcodigital.com.br"

    start_date = date(2011, 12, 6)
