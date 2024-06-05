from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaRafaelJambeiroSpider(SaiGazetteSpider):
    TERRITORY_ID = "2925956"
    name = "ba_rafael_jambeiro"
    allowed_domains = ["rafaeljambeiro.ba.gov.br"]
    base_url = "https://www.rafaeljambeiro.ba.gov.br"
    start_date = date(2007, 9, 28)
