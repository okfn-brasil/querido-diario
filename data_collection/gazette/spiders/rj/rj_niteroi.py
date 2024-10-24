import datetime as dt
from dateutil import rrule

import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class RjNiteroiSpider(BaseGazetteSpider):
    """
    Spider para coletar diários oficiais do município de Niterói-RJ.

    A spider coleta arquivos PDF de diários oficiais no site do Diário Oficial de Niterói
    e armazena informações como a data e o URL dos arquivos.
    """

    TERRITORY_ID = "3303302"
    name = "rj_niteroi"
    allowed_domains = ["diariooficial.niteroi.rj.gov.br"]
    download_url = "https://diariooficial.niteroi.rj.gov.br/do/{}/{}/{}.pdf"
    start_date = dt.date(2024, 7, 1)
    end_date = dt.date.today()

    # Mapeamento de nomes dos meses
    month_names = [
        "01_Jan",
        "02_Fev",
        "03_Mar",
        "04_Abr",
        "05_Mai",
        "06_Jun",
        "07_Jul",
        "08_Ago",
        "09_Set",
        "10_Out",
        "11_Nov",
        "12_Dez",
    ]

    def start_requests(self):
        """
        Gera as requests a partir da data inicial até a data final (hoje).
        O uso do `rrule` facilita a iteração de dias.
        """
        for date in rrule.rrule(
            rrule.DAILY, dtstart=self.start_date, until=self.end_date
        ):
            month_name = self.month_names[date.month - 1]
            url = self.download_url.format(date.year, month_name, f"{date.day:02d}")
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
