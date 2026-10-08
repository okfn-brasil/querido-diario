import re
from datetime import date, datetime, timedelta, timezone

import dateparser
from scrapy import Request
from scrapy.http import JsonRequest

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider
from gazette.utils.dates import monthly_sequence


class RnParnamirimSpider(BaseGazetteSpider):
    """
    Os diários publicados até 16/07/2018 estão listados em uma única página do
    site antigo da prefeitura. A partir de 17/07/2018, são publicados no SGIDOM,
    que lista as edições por mês e gera o PDF de cada edição sob demanda.
    """

    TERRITORY_ID = "2403251"
    name = "rn_parnamirim"
    allowed_domains = [
        "antigo.parnamirim.rn.gov.br",
        "sgidomapi.parnamirim.rn.gov.br",
        "sgidomhtmltopdf.parnamirim.rn.gov.br",
    ]
    start_date = date(2009, 1, 13)

    OLD_WEBSITE_URL = "https://antigo.parnamirim.rn.gov.br/diarioOficial.jsp"
    SGIDOM_START_DATE = date(2018, 7, 17)
    SGIDOM_API_URL = (
        "https://sgidomapi.parnamirim.rn.gov.br/sgidom/rest"
        "/sgidiario_diario_service/diarios_por_mes"
    )
    SGIDOM_EXPORT_URL = "https://sgidomhtmltopdf.parnamirim.rn.gov.br/export"
    SGIDOM_ORIGIN = "https://diariooficial.parnamirim.rn.gov.br"
    TIMEZONE = timezone(timedelta(hours=-3))

    async def start(self):
        if self.start_date < self.SGIDOM_START_DATE:
            yield Request(self.OLD_WEBSITE_URL, callback=self.parse_old_website)

        if self.end_date >= self.SGIDOM_START_DATE:
            start_date = max(self.start_date, self.SGIDOM_START_DATE)
            for month in monthly_sequence(start_date, self.end_date, format="%Y-%m"):
                yield Request(f"{self.SGIDOM_API_URL}?data={month}")

    def parse_old_website(self, response):
        end_date = min(self.end_date, self.SGIDOM_START_DATE - timedelta(days=1))

        for gazette in response.css("div.sub-dropdown > ul > ul > li"):
            raw_date = gazette.css("span::text").re_first(r"\d{1,2} de \w+ de \d{4}")
            gazette_date = dateparser.parse(raw_date, languages=["pt"]).date()
            if not self.start_date <= gazette_date <= end_date:
                continue

            title = gazette.css("a::text").get()
            edition_number = re.search(r"(?:DOM|BO)\W*(?:n\S?\W*)?(\d+)", title, re.I)

            yield Gazette(
                date=gazette_date,
                edition_number=(
                    str(int(edition_number.group(1))) if edition_number else ""
                ),
                is_extra_edition="especial" in title.lower(),
                file_urls=[response.urljoin(gazette.css("a::attr(href)").get())],
                power="executive_legislative",
            )

    def parse(self, response):
        for gazette in response.json():
            gazette_date = datetime.fromtimestamp(
                gazette["data_publicacao"] / 1000, tz=self.TIMEZONE
            ).date()
            if not self.start_date <= gazette_date <= self.end_date:
                continue

            gazette_id = gazette["id"]
            # O PDF é gerado por um POST sempre para a mesma URL. O id da edição
            # é incluído na URL para que cada arquivo tenha um nome diferente
            # ao ser salvo pelo FilesPipeline
            file_request = JsonRequest(
                f"{self.SGIDOM_EXPORT_URL}?id_diario={gazette_id}",
                data={
                    "domQueryParams": f"publicar=false&id_diario={gazette_id}&",
                    "domDataCabecalho": gazette_date.strftime("%d/%m/%Y"),
                    "domOrigin": self.SGIDOM_ORIGIN,
                    "diarioId": gazette_id,
                },
            )

            yield Gazette(
                date=gazette_date,
                edition_number=re.search(r"\d+", gazette["numero"]).group(),
                is_extra_edition="especial" in gazette["numero"].lower(),
                file_requests=[file_request],
                power="executive_legislative",
            )
