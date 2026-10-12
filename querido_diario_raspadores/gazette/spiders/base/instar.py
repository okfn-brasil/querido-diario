import datetime
import math
import re
from urllib.parse import urlparse

import scrapy
from scrapy.exceptions import NotConfigured
from scrapy.http import TextResponse

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider

# Opção `defaultUrl` do PDF.js embutido na página `/diario-oficial/ver/<id>/`.
DEFAULT_URL_RE = re.compile(
    r"defaultUrl\s*:\s*\{\s*value\s*:\s*(?P<q>['\"])(?P<url>.*?)(?P=q)", re.DOTALL
)


class BaseInstarSpider(BaseGazetteSpider):
    power = "executive_legislative"

    def __init__(self, *args, **kwargs):
        if not hasattr(self, "base_url"):
            raise NotConfigured("Please set a value for `base_url`")

        self.allowed_domains = [urlparse(self.base_url).netloc]

        super(BaseInstarSpider, self).__init__(*args, **kwargs)

    async def start(self):
        page = 1
        start_date = self.start_date.strftime("%d-%m-%Y")
        end_date = self.end_date.strftime("%d-%m-%Y")

        start_url = f"{self.base_url}/{page}/{start_date}/{end_date}/0/0/"

        yield scrapy.Request(
            start_url,
            cb_kwargs={"page": page, "start_date": start_date, "end_date": end_date},
        )

    def _pagination_requests(self, response, page, start_date, end_date):
        if page == 1:
            num_results = int(response.css(".sw_qtde_resultados::text").get("0"))
            results_per_page = 50
            total_pages = math.ceil(num_results / results_per_page)

            for next_page in range(2, total_pages + 1):
                next_page_url = (
                    f"{self.base_url}/{next_page}/{start_date}/{end_date}/0/0/"
                )

                yield scrapy.Request(
                    next_page_url,
                    cb_kwargs={
                        "page": next_page,
                        "start_date": start_date,
                        "end_date": end_date,
                    },
                )

    def parse(self, response, page, start_date, end_date):
        gazettes = response.css(".dof_publicacao_diario")
        for gazette in gazettes:
            raw_gazette_date = gazette.css("span::text").re_first(
                r"\d{2}\/\d{2}\/\d{4}"
            )
            gazette_date = datetime.datetime.strptime(
                raw_gazette_date, "%d/%m/%Y"
            ).date()
            edition_number = gazette.css(".dof_titulo_publicacao span::text").re_first(
                r"\d+"
            )
            gazette_url = response.urljoin(gazette.css("a::attr(href)").get())

            item = Gazette(
                date=gazette_date,
                edition_number=edition_number,
                is_extra_edition=False,
                power=self.power,
            )

            yield scrapy.Request(
                gazette_url, callback=self.parse_gazette_url, cb_kwargs={"item": item}
            )

        yield from self._pagination_requests(response, page, start_date, end_date)

    def _extract_file_url(self, response):
        """Devolve a URL do arquivo da edição, ou None se a página não tiver.

        A página `/ver/<id>/` é o visualizador PDF.js, não o arquivo. O arquivo
        fica no `defaultUrl` das opções do PDF.js embutido na página. Se a página
        trouxer um link de download explícito (`.d_titulo_edicao a`), ele tem
        prioridade.
        """
        if not isinstance(response, TextResponse):
            # O link da listagem já aponta para o arquivo (PDF), não para o visualizador.
            return response.url

        href = response.css(".d_titulo_edicao a::attr(href)").get()
        if not href:
            match = DEFAULT_URL_RE.search(response.text)
            href = match.group("url") if match else None
        if not href or not href.strip():
            return None
        file_url = response.urljoin(href.strip())
        # O link não pode apontar para a própria página do visualizador.
        return None if file_url.rstrip("/") == response.url.rstrip("/") else file_url

    def parse_gazette_url(self, response, item):
        gazette_url = self._extract_file_url(response)

        if gazette_url is None:
            self.logger.warning(
                f"Nenhum arquivo encontrado na página da edição {response.url}"
            )
            return

        yield Gazette(
            file_urls=[
                gazette_url,
            ],
            **item,
        )
