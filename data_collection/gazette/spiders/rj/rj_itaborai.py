from datetime import datetime as dt, timedelta

import scrapy
from dateutil.rrule import MONTHLY, rrule

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class RjItaboraiSpider(BaseGazetteSpider):
    name = "rj_itaborai"
    TERRITORY_ID = "3301900"
    allowed_domains = ["do.ib.itaborai.rj.gov.br"]
    BASE_URL = "https://do.ib.itaborai.rj.gov.br/dados-portal-novo.php"
    start_date = dt(2020, 1, 1).date()
    end_date = dt.today().date()

    def start_requests(self):
        formatos_data = ["%Y-%m-%d"]
        self.logger.info(f"Iniciando a coleta a partir de {self.start_date}")
        for monthly_date in self.get_monthly_dates():
            for formato in formatos_data:
                data_inicio = monthly_date.strftime(formato)
                ultimo_dia = (monthly_date.replace(day=1) + timedelta(days=31)).replace(
                    day=1
                ) - timedelta(days=1)
                data_fim = ultimo_dia.strftime(formato)
                self.logger.info(
                    f"Tentando coletar de {data_inicio} até {data_fim} no formato {formato}"
                )

                yield scrapy.FormRequest(
                    url=self.BASE_URL,
                    formdata={"acao": "3", "dado[]": [data_inicio, data_fim]},
                    method="POST",
                    callback=self.parse,
                )

    def get_monthly_dates(self):
        return rrule(MONTHLY, dtstart=self.start_date, until=self.end_date)

    def parse(self, response):
        self.logger.info(f"Resposta recebida: {response.text[:1000]}")

        if "no-results" in response.text or "Data inválida" in response.text:
            self.logger.warning("Nenhum resultado encontrado ou data inválida.")
            return

        gazettes = response.xpath('//div[contains(@class, "card-avulso-diario")]')
        if not gazettes:
            self.logger.warning("Nenhuma edição encontrada.")
            return

        for gazette in gazettes:
            raw_gazette_date = gazette.xpath(
                './/p[contains(text(),"Postado em")]/text()'
            ).re_first(r"\d{2}/\d{2}/\d{4}")
            if not raw_gazette_date:
                self.logger.warning("Data não encontrada.")
                continue

            gazette_date = dt.strptime(raw_gazette_date, "%d/%m/%Y").date()

            gazette_edition_number = gazette.xpath(
                './/p[contains(text(),"Edição N°")]/text()'
            ).re_first(r"\d+")
            if not gazette_edition_number:
                self.logger.warning("Número da edição não encontrado.")
                continue

            is_extra = (
                gazette.xpath('.//p[contains(text(),"EXTRAORDINÁRIA")]/text()').get()
                is not None
            )

            gazette_url = gazette.xpath(
                './/a[contains(text(),"Abrir documento")]/@href'
            ).get()
            if not gazette_url:
                self.logger.warning("URL de download não encontrada.")
                continue

            gazette_url = response.urljoin(gazette_url)

            yield Gazette(
                date=gazette_date,
                edition_number=gazette_edition_number,
                is_extra_edition=is_extra,
                file_urls=[gazette_url],
                power="executive",
            )
