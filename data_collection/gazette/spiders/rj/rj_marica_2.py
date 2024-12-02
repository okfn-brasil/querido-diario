from datetime import date

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class UFMunicipioSpider(BaseGazetteSpider):
    name = "rj_marica_2"
    TERRITORY_ID = ""
    allowed_domains = ["www.marica.rj.gov.br"]
    start_urls = ["https://www.marica.rj.gov.br/jornal-oficial-marica"]
    start_date = date()

    def parse(self, response):
        # Lógica de extração de metadados

        # partindo de response ...
        #
        # ... o que deve ser feito para coletar DATA DO DIÁRIO?
        # ... o que deve ser feito para coletar NÚMERO DA EDIÇÃO?
        # ... o que deve ser feito para coletar se a EDIÇÃO É EXTRA?
        # ... o que deve ser feito para coletar a URL DE DOWNLOAD do arquivo?

        yield Gazette(
            date=date(),
            edition_number="",
            is_extra_edition=False,
            file_urls=[""],
            power="executive",
        )
