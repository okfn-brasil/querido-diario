from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaSantoAntonioDeJesusSpider(SaiGazetteSpider):
    TERRITORY_ID = "2928703"
    name = "ba_santo_antonio_de_jesus"
    allowed_domains = ["sai.io.org.br"]
    base_url = "https://sai.io.org.br/ba/santoantoniodejesus"
    start_date = date(2005, 9, 30)
