import datetime as dt

from gazette.spiders.base.nucleogov import NucleoGovGazetteSpider


class ToCaririDoTocantinsSpider(NucleoGovGazetteSpider):
    name = "to_cariri_do_tocantins"
    TERRITORY_ID = "1703867"
    allowed_domains = [
        "dom.cariri.to.gov.br",
    ]
    url_base = (
        "https://dom.cariri.to.gov.br/api/diarios?data={}&calendar=true&situacao=2"
    )

    start_date = dt.date(2023, 1, 30)
