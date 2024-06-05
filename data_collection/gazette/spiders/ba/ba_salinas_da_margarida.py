from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaSalinasDaMargaridaSpider(SaiGazetteSpider):
    TERRITORY_ID = "2927309"
    name = "ba_salinas_da_margarida"
    allowed_domains = ["salinasdamargarida.ba.gov.br"]
    base_url = "https://www.salinasdamargarida.ba.gov.br"
    start_date = date(2005, 6, 9)
