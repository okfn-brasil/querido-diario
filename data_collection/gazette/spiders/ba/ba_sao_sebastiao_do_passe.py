from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaSaoSebastiaoDoPasseSpider(SaiGazetteSpider):
    TERRITORY_ID = "2929503"
    name = "ba_sao_sebastiao_do_passe"
    allowed_domains = ["sai.io.org.br"]
    base_url = "https://sai.io.org.br/ba/saosebastiaodopasse"
    start_date = date(2011, 1, 20)
