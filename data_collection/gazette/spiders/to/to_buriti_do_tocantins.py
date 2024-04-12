from datetime import date

from gazette.spiders.base.vale import ValeGazetteSpider


class ToBuritiDoTocantinsSpider(ValeGazetteSpider):
    TERRITORY_ID = "1703800"
    name = "to_buriti_do_tocantins"
    allowed_domains = ["diario.buritidotocantins.to.gov.br"]
    start_date = date(2017, 3, 20)
