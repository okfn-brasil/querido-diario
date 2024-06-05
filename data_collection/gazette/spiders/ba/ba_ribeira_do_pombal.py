from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaRibeiraDoPombalSpider(SaiGazetteSpider):
    TERRITORY_ID = "2926608"
    name = "ba_ribeira_do_pombal"
    allowed_domains = ["sai.io.org.br"]
    base_url = "https://sai.io.org.br/ba/ribeiradopombal"
    start_date = date(2007, 9, 18)
