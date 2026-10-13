import re
from datetime import date, datetime

import scrapy
from parsel import Selector
from scrapy import signals
from scrapy.exceptions import DontCloseSpider, NotConfigured

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class BaseAgapeSpider(BaseGazetteSpider):
    """
    Spider base para o sistema de Diário Oficial da AGAPE Sistemas.

    O site é feito em JSF/RichFaces e guarda o resultado da última busca na sessão
    do servidor: o download de uma edição é feito com um postback que referencia a
    posição da edição na lista dessa última busca. Por isso, cada janela de busca usa
    uma sessão própria (`cookiejar`), e os downloads da janela são feitos nessa mesma
    sessão.

    A sessão expira depois de cerca de 30 minutos sem uso. Por isso, as janelas são
    processadas uma de cada vez: a busca da janela seguinte só começa quando o spider
    fica ocioso, isto é, depois que todos os arquivos da janela anterior foram
    baixados. Com todas as buscas feitas no início, os anos baixados por último
    falhavam inteiros nas coletas longas.
    """

    allowed_domains = ["agportal.agapesistemas.com.br"]
    custom_settings = {
        "DOWNLOAD_DELAY": 1,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 2,
    }

    EDITION_LINK_SUFFIX = ":j_id73"
    # Quando o arquivo de uma edição não está disponível, o portal responde ao
    # download com a página HTML do sistema (status 200)
    FILE_CONTENT_TYPES = (b"application/download", b"application/pdf")
    power = "executive"

    def __init__(self, *args, **kwargs):
        if not hasattr(self, "alias"):
            raise NotConfigured("Please set a value for `alias`")

        super().__init__(*args, **kwargs)

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super().from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_idle, signal=signals.spider_idle)
        return spider

    async def start(self):
        self._pending_windows = self.window_requests()
        first_window = next(self._pending_windows, None)
        if first_window is not None:
            yield first_window

    def spider_idle(self, spider):
        pending_windows = getattr(self, "_pending_windows", None)
        next_window = next(pending_windows, None) if pending_windows else None
        if next_window is None:
            return

        self.crawler.engine.crawl(next_window)
        raise DontCloseSpider

    def window_requests(self):
        url = f"https://agportal.agapesistemas.com.br/DiarioOficial/?alias={self.alias}"
        for year in range(self.start_date.year, self.end_date.year + 1):
            yield scrapy.Request(
                url,
                callback=self.search_request,
                meta={"cookiejar": year},
                cb_kwargs={
                    "start": max(self.start_date, date(year, 1, 1)),
                    "end": min(self.end_date, date(year, 12, 31)),
                },
                dont_filter=True,
            )

    def search_request(self, response, start, end):
        formdata = self._formdata(response, start, end)
        search_button = response.xpath("//input[@value='Buscar']/@id").get()
        formdata.update({"AJAXREQUEST": "_viewRoot", search_button: search_button})

        yield scrapy.FormRequest.from_response(
            response,
            formid="form",
            formdata=formdata,
            dont_click=True,
            meta={"cookiejar": response.meta["cookiejar"]},
            cb_kwargs={
                "form_response": response,
                "formdata": formdata,
                "search_button": search_button,
            },
        )

    def parse(self, response, form_response, formdata, search_button):
        # O download é um postback comum: sem AJAX e sem o botão "Buscar", que o
        # FormRequest incluiria a partir do formulário (valor None o remove).
        formdata = {
            **{
                key: value
                for key, value in formdata.items()
                if key not in ("AJAXREQUEST", search_button)
            },
            search_button: None,
        }

        # A resposta AJAX é XHTML com namespace; lê-la como HTML simplifica os seletores
        results = Selector(text=response.text, type="html")
        for link in results.xpath("//a[contains(@onclick, 'jsfcljs')]"):
            link_id = re.search(
                r"jsfcljs\(document\.forms\['form'\],'([^,']+),",
                link.attrib["onclick"],
            ).group(1)
            if not link_id.endswith(self.EDITION_LINK_SUFFIX):
                continue

            raw_date = link.xpath(
                "ancestor::div[contains(@class, 'resultadoDocumentos')][1]"
                "/preceding-sibling::div[1]//span[@class='rtitulo']/text()"
            ).get()
            edition_number = link.xpath("normalize-space(.)").get()
            gazette_date = datetime.strptime(raw_date, "%d/%m/%Y").date()

            # Todos os downloads são postbacks para a mesma URL. A query string,
            # ignorada pelo servidor, torna a URL de cada edição única e termina em
            # ".pdf"; sem ela, o FilesPipeline daria o mesmo nome e a extensão
            # ".xht" (de "index.xhtml") a todos os arquivos.
            action_url = form_response.urljoin(
                form_response.xpath("//form[@id='form']/@action").get()
            )
            download_url = (
                f"{action_url}?data={gazette_date}&edicao={edition_number}"
                "&arquivo=diario.pdf"
            )

            yield Gazette(
                date=gazette_date,
                edition_number=edition_number,
                file_requests=[
                    scrapy.FormRequest.from_response(
                        form_response,
                        url=download_url,
                        formid="form",
                        formdata={**formdata, link_id: link_id},
                        dont_click=True,
                        meta={
                            "cookiejar": response.meta["cookiejar"],
                            "expected_content_types": self.FILE_CONTENT_TYPES,
                        },
                    )
                ],
                is_extra_edition=False,
                power=self.power,
            )

    def _formdata(self, response, start, end):
        entity = self._entity(response)
        return {
            "form:entidade": entity,
            "form:de": start.strftime("%d/%m/%Y"),
            "form:ate": end.strftime("%d/%m/%Y"),
        }

    def _entity(self, response):
        if hasattr(self, "entity"):
            return self.entity

        for option in response.xpath("//select[@name='form:entidade']/option"):
            if "PREFEITURA" in option.xpath("normalize-space(.)").get().upper():
                return option.attrib["value"]

        raise NotConfigured("Could not find the entity option for the city hall")
