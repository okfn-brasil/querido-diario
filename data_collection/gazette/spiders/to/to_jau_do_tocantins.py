import datetime as dt

from gazette.spiders.base.nucleogov import NucleoGovGazetteSpider


class ToJauDoTocantinsSpider(NucleoGovGazetteSpider):
    name = "to_jau_do_tocantins"
    TERRITORY_ID = "1711506"
    allowed_domains = [
        "diariooficial.jau.to.gov.br",
    ]
    url_base = "https://diariooficial.jau.to.gov.br/api/diarios?data={}&calendar=true&situacao=2"

    start_date = dt.date(2023, 5, 15)
