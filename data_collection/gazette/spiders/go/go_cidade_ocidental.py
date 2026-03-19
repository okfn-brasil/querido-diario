from datetime import date

from gazette.spiders.base.nucleogov import BaseNucleoGovSpider


class GoCidadeOcidentalSpider(BaseNucleoGovSpider):
    TERRITORY_ID = "5205497"
    name = "go_cidade_ocidental"
    base_url = "https://dom.cidadeocidental.go.gov.br"
    start_date = date(2023, 2, 1)
