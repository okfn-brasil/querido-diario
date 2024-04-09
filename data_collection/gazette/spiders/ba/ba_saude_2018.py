"""The files from the years 2018 and 2019 are available using the Imprensa Oficial system.
This city now uses the BR Transparência system, which covers other cities. The Base is not developed.
"""
from datetime import date

from gazette.spiders.base.imprensa_oficial import ImprensaOficialSpider


class BaSaudeSpider(ImprensaOficialSpider):
    name = "ba_saude_2018"
    allowed_domains = ["pmsaudeba.imprensaoficial.org"]
    start_date = date(2018, 2, 1)
    end_date = date(2019, 4, 12)
    city_domain = "http://pmsaudeba.imprensaoficial.org"
    TERRITORY_ID = "2929800"
