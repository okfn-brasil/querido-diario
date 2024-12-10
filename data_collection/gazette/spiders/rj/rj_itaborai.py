import re
from datetime import date, datetime as dt, timedelta

import scrapy
from dateutil.rrule import MONTHLY, rrule

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class UFMunicipioSpider(BaseGazetteSpider):
    name = "rj_itaborai"
    TERRITORY_ID = "3301900"
    allowed_domains = ["site.ib.itaborai.rj.gov.br", "do.ib.itaborai.rj.gov.br"]
    start_urls = ["https://site.ib.itaborai.rj.gov.br/diario-oficial/"]
    BASE_URL = "https://do.ib.itaborai.rj.gov.br/dados-portal-novo.php"
    start_date = date(2020, 1, 1)

    def start_requests(self):
        for monthly_date in rrule(
            MONTHLY, dtstart=self.start_date, until=self.end_date
        ):
            data_inicio = monthly_date.strftime("%d/%m/%Y")
            ultimo_dia = (monthly_date.replace(day=1) + timedelta(days=31)).replace(
                day=1
            ) - timedelta(days=1)
            data_fim = ultimo_dia.strftime("%d/%m/%Y")

            url = f"{self.BASE_URL}?acao=3&dado={data_inicio},{data_fim}"
            self.logger.info(f"Requisição feita para: {url}")

            yield scrapy.Request(
                url=url,
                method="GET",
                callback=self.parse,
            )

    def parse(self, response):
        # Lógica de extração de metadados
        self.logger.info(f"Resposta: {response.text[:1000]}")

        try:
            html = response.json()["html"]
        except (KeyError, ValueError):
            self.logger.warning("Resposta inesperada")
            return

        gazette_list = html.split("\n\n\n")
        if not gazette_list:
            self.logger.warning("Nenhum diario encontrado")
            return

        for gazette_data in gazette_list:
            raw_gazette_date = re.search(r"\d{2}/\d{2}/\d{4}", gazette_data)

            gazette_date = (
                dt.strptime(raw_gazette_date.group(), "%d/%m/%Y").date()
                if raw_gazette_date
                else None
            )
            if not gazette_date or not (
                self.start_date <= gazette_date <= self.end_date
            ):
                continue

            gazette_edition_number = re.search(r"Edição N° (\d+)", gazette_data)
            gazette_url = re.search(r'href="(.*?)"', gazette_data)

            if gazette_date and gazette_edition_number and gazette_url:
                yield Gazette(
                    date=gazette_date,
                    edition_number=gazette_edition_number,
                    is_extra_edition=False,
                    file_urls=[response.urljoin(gazette_url)],
                    power="executive",
                )
            else:
                self.logger.warning("Campos faltando")
        # partindo de response ...
        #
        # ... o que deve ser feito para coletar DATA DO DIÁRIO?
        # ... o que deve ser feito para coletar NÚMERO DA EDIÇÃO?
        # ... o que deve ser feito para coletar se a EDIÇÃO É EXTRA?
        # ... o que deve ser feito para coletar a URL DE DOWNLOAD do arquivo?
