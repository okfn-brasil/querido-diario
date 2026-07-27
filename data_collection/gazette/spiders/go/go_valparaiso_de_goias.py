from datetime import date

from gazette.spiders.base.nucleogov import BaseNucleoGovSpider


class GoValparaisoDeGoiasSpider(BaseNucleoGovSpider):
    TERRITORY_ID = "5221858"
    name = "go_valparaiso_de_goias"
    base_url = "https://diariooficial.valparaisodegoias.go.gov.br"
    start_date = date(2021, 2, 17)
