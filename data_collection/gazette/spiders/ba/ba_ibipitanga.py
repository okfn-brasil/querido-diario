from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaIbipitangaSpider(SaiGazetteSpider):
    TERRITORY_ID = "2912509"
    name = "ba_ibipitanga"
    allowed_domains = ["ibipitanga.ba.gov.br"]
    base_url = "https://www.ibipitanga.ba.gov.br"
    start_date = date(2014, 1, 9)
