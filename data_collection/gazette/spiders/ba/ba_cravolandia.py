from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaCravolandiaSpider(SaiGazetteSpider):
    TERRITORY_ID = "2909505"
    name = "ba_cravolandia"
    allowed_domains = ["cravolandia.ba.gov.br"]
    base_url = "https://www.cravolandia.ba.gov.br"
    start_date = date(2007, 3, 6)
