"""The files from the year 2020 are available using the Imprensa Oficial system.
This city now uses the SAIIO system. The spider is available in the file 'ba_gongogi_2024'.
"""
from datetime import date

from gazette.spiders.base.imprensa_oficial import ImprensaOficialSpider


class BaGongogiImprensaOficialSpider(ImprensaOficialSpider):
    name = "ba_gongogi_2020"
    allowed_domains = ["pmgongogiba.imprensaoficial.org"]
    start_date = date(2020, 2, 1)
    end_date = date(2020, 12, 30)
    city_domain = "http://pmgongogiba.imprensaoficial.org"
    TERRITORY_ID = "2911501"
