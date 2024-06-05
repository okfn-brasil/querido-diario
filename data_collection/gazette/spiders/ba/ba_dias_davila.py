from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaDiasDavilaSpider(SaiGazetteSpider):
    TERRITORY_ID = "2910057"
    name = "ba_dias_davila"
    allowed_domains = ["sai.io.org.br"]
    base_url = "https://sai.io.org.br/ba/diasdavila"
    start_date = date(2011, 7, 27)
