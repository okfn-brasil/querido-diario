import datetime as dt

from gazette.spiders.base.nucleogov import NucleoGovGazetteSpider


class GoAnapolisSpider(NucleoGovGazetteSpider):
    name = "go_anapolis"
    TERRITORY_ID = "5201108"
    allowed_domains = [
        "dom.anapolis.go.gov.br",
    ]
    url_base = (
        "https://dom.anapolis.go.gov.br/api/diarios?data={}&calendar=true&situacao=2"
    )

    start_date = dt.date(2010, 5, 31)
