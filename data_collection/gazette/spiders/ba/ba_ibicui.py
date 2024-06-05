from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaIbicuiSpider(SaiGazetteSpider):
    TERRITORY_ID = "2912301"
    name = "ba_ibicui"
    allowed_domains = ["ibicui.ba.gov.br"]
    base_url = "https://www.ibicui.ba.gov.br"
    start_date = date(2007, 3, 22)
