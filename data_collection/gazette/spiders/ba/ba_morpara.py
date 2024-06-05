from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaMorparaSpider(SaiGazetteSpider):
    TERRITORY_ID = "2921609"
    name = "ba_morpara"
    allowed_domains = ["morpara.ba.gov.br"]
    base_url = "https://www.morpara.ba.gov.br"
    start_date = date(2008, 10, 17)
