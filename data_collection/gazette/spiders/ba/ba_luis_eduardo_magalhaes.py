import datetime as dt

from gazette.spiders.base.sai import SaiGazetteSpider


class BaLuisEduardoMagalhaesSpider(SaiGazetteSpider):
    TERRITORY_ID = "2919553"
    name = "ba_luis_eduardo_magalhaes"
    start_date = dt.date(2017, 1, 4)
    allowed_domains = ["sai.io.org.br"]
    base_url = "https://sai.io.org.br/ba/luiseduardomagalhaes"
