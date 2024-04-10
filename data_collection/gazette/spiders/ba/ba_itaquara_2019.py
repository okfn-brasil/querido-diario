"""The files between the years 2019 and 2022 are available using the Imprensa Oficial system.
This city now uses the BR Transparência system, which covers other cities. The Base is not developed.
"""
from datetime import date

from gazette.spiders.base.imprensa_oficial import ImprensaOficialSpider


class BaItaquaraSpider(ImprensaOficialSpider):
    name = "ba_itaquara_2019"
    allowed_domains = ["pmitaquaraba.imprensaoficial.org"]
    start_date = date(2019, 1, 1)
    end_date = date(2022, 1, 4)
    city_domain = "http://pmitaquaraba.imprensaoficial.org"
    TERRITORY_ID = "2916708"
