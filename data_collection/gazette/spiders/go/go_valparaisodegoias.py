import datetime as dt

from gazette.spiders.base.nucleogov import NucleoGovGazetteSpider


class GoValparaisoDeGoiasSpider(NucleoGovGazetteSpider):
    name = "go_valparaisodegoias"
    TERRITORY_ID = "5221858"
    allowed_domains = [
        "diariooficial.valparaisodegoias.go.gov.br",
    ]
    url_base = "https://diariooficial.valparaisodegoias.go.gov.br/api/diarios?data={}&calendar=true&situacao=2"

    start_date = dt.date(2021, 2, 17)
