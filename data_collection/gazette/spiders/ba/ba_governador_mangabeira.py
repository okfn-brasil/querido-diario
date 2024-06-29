from datetime import date

from gazette.spiders.base.imprensa_oficial import ImprensaOficialSpider


class BaGovernadorMangabeiraSpider(ImprensaOficialSpider):
    name = "ba_governador_mangabeira"
    allowed_domains = ["pmgovernadormangabeiraba.imprensaoficial.org"]
    start_date = date(2018, 1, 1)
    city_domain = "http://pmgovernadormangabeiraba.imprensaoficial.org"
    TERRITORY_ID = "2911600"
