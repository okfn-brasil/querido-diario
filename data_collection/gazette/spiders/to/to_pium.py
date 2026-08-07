from datetime import date

from gazette.spiders.base.vale import ValeGazetteSpider


class ToPiumSpider(ValeGazetteSpider):
    TERRITORY_ID = "1717503"
    name = "to_pium"
    allowed_domains = ["diario.pium.to.gov.br"]
    start_date = date(2021, 4, 14)
