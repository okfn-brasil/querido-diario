from datetime import date

from gazette.spiders.base.imprensa_oficial import ImprensaOficialSpider


class BaMunizFerreiraSpider(ImprensaOficialSpider):
    name = "ba_muniz_ferreira"
    allowed_domains = ["pmmunizferreiraba.imprensaoficial.org"]
    start_date = date(2014, 12, 1)
    end_date = date(2021, 1, 19)
    city_domain = "http://pmmunizferreiraba.imprensaoficial.org"
    TERRITORY_ID = "2922201"
