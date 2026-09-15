import datetime as dt

from gazette.spiders.base.nucleogov import NucleoGovGazetteSpider


class ToParanaSpider(NucleoGovGazetteSpider):
    name = "to_parana"
    TERRITORY_ID = "1716208"
    allowed_domains = [
        "diariooficial.parana.to.gov.br",
    ]
    url_base = "https://diariooficial.parana.to.gov.br/api/diarios?data={}&calendar=true&situacao=2"

    start_date = dt.date(2023, 5, 8)
