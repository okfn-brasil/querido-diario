from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class SeUmbaubaSpider(SaiGazetteSpider):
    TERRITORY_ID = "2807600"
    name = "se_umbauba"
    allowed_domains = ["umbauba.se.gov.br"]
    base_url = "https://www.umbauba.se.gov.br"
    start_date = date(2018, 3, 6)
