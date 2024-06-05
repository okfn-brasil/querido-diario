from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class PbMassarandubaSpider(SaiGazetteSpider):
    TERRITORY_ID = "2509206"
    name = "pb_massaranduba"
    allowed_domains = ["massaranduba.pb.gov.br"]
    base_url = "https://www.massaranduba.pb.gov.br"
    start_date = date(2015, 4, 22)
