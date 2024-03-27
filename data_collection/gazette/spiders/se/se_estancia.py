import datetime as dt

from gazette.spiders.base.sai import SaiGazetteSpider


class SeEstanciaSpider(SaiGazetteSpider):
    TERRITORY_ID = "2802106"
    name = "se_estancia"
    start_date = dt.date(2016, 4, 28)
    allowed_domains = ["estancia.se.gov.br"]
    base_url = "https://www.estancia.se.gov.br"
