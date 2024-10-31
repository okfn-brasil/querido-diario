# Importando bibliotecas padrão
import datetime as dt
from dateutil import rrule

# Importando bibliotecas de terceiros
import scrapy

# Importando módulos locais do projeto
from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class AmAssociacaoMunicipiosSpider(BaseGazetteSpider):
    """
    Spider para coletar diários oficiais do município de Niterói-RJ.

    A spider coleta arquivos PDF de diários oficiais no site do Diário Oficial de Niterói
    e armazena informações como a data e o URL dos arquivos.
    """

    TERRITORY_ID = "1300000"
    name = "am_associacao_municipios"
    allowed_domains = ["https://diariomunicipalaam.org.br/"]
    download_url = "https://diariomunicipalaam.org.br/visualizar-publicacao/{}"
    start_date = dt.date(2009, 10, 19)  # primeira edição encontrada
    end_date = dt.date.today()

    def start_requests(self):
        """
        Gera as requests a partir da data inicial até a data final (hoje).
        """
        for date in rrule.rrule(
            rrule.DAILY, dtstart=self.start_date, until=self.end_date
        ):
            formatted_date = date.strftime("%Y%m%d")  # Formato YYYYMMDD
            url = self.download_url.format(formatted_date)
            yield scrapy.Request(
                url,
                method="HEAD",
                callback=self.parse_valid_gazette_file,
                cb_kwargs={"gazette_date": date.date()},
            )

    def parse_valid_gazette_file(self, response, gazette_date):
        """
        Verifica se o arquivo existe e gera o item do diário oficial.
        """
        if response.status == 200:
            yield Gazette(
                date=gazette_date,
                file_urls=[response.url],
                is_extra_edition=False,
                power="executive",
            )
