import datetime as dt

from scrapy import Request

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider
from gazette.utils.dates import monthly_sequence


class RsPortoAlegreSpider(BaseGazetteSpider):
    TERRITORY_ID = "4314902"
    name = "rs_porto_alegre"
    allowed_domains = ["apigateway.procempa.com.br"]
    start_date = dt.date(2011, 5, 2)

    API_BASE_URL = (
        "https://apigateway.procempa.com.br/apiman-gateway/"
        "administracao-planejamento/dopa/1.1"
    )

    custom_settings = {"CONCURRENT_REQUESTS": 8}

    async def start(self):
        for month_date in monthly_sequence(self.start_date, self.end_date):
            url = (
                f"{self.API_BASE_URL}/api/diarios/busca-por-mes-agrupada"
                f"?mes={month_date.month}&ano={month_date.year}"
            )
            yield Request(url, callback=self.parse_api_month)

    def parse_api_month(self, response):
        gazettes_by_power = response.json()

        for api_power, power in (
            ("executivo", "executive"),
            ("legislativo", "legislative"),
        ):
            for date_group in gazettes_by_power.get(api_power, []):
                date = dt.datetime.strptime(date_group["data"], "%d/%m/%Y").date()

                if not self.start_date <= date <= self.end_date:
                    continue

                for publication in date_group.get("publicacoes", []):
                    link_download = publication.get("linkDownload")
                    if not link_download:
                        self.logger.warning(
                            "Edition %s does not have a download link.",
                            publication.get("idEdicao"),
                        )
                        continue

                    if link_download.startswith(("http://", "https://")):
                        file_url = link_download
                    else:
                        file_url = f"{self.API_BASE_URL}/{link_download.lstrip('/')}"

                    yield Gazette(
                        date=date,
                        edition_number=publication["numeroEdicao"],
                        file_urls=[file_url],
                        is_extra_edition=publication["isExtra"],
                        power=power,
                    )
