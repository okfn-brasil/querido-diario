from datetime import date

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class UFMunicipioSpider(BaseGazetteSpider):
    name = "rj_teresopolis"
    TERRITORY_ID = "3305802"
    allowed_domains = ["atos.teresopolis.rj.gov.br"]
    start_urls = ["https://atos.teresopolis.rj.gov.br/diario/#/diarios"]
    start_date = date(2016, 7, 22)

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
