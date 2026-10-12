from datetime import datetime, timedelta

import scrapy
from scrapy.exceptions import NotConfigured
from scrapy.spidermiddlewares.httperror import HttpError

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider
from gazette.utils.dates import yearly_window


class BaseMunicipioOnlineSpider(BaseGazetteSpider):
    custom_settings = {
        "DOWNLOAD_DELAY": 1,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 4,
    }

    allowed_domains = ["municipioonline.com.br"]

    def __init__(self, *args, **kwargs):
        if not hasattr(self, "url_uf"):
            raise NotConfigured("Please set a value for `url_uf`")

        if not hasattr(self, "url_city"):
            raise NotConfigured("Please set a value for `url_city`")

        super(BaseMunicipioOnlineSpider, self).__init__(*args, **kwargs)

    async def start(self):
        url = f"https://www.municipioonline.com.br/{self.url_uf}/prefeitura/{self.url_city}/cidadao/diariooficial"
        yield scrapy.Request(url, callback=self.date_filter_request)

    def date_filter_request(self, response):
        """
        Cria requisições para filtro por data.

        O sistema em teoria permite fazer uma requisição única para qualquer start_date
        e end_date. Porém, alguns municípios com cobertura cronológica maior retornam
        resposta com código 500 caso o intervalo de tempo seja muito grande.

        Assim, nessa implementação, o intervalo de tempo máximo para apenas uma
        requisição é de um ano. Acima disso, mais de uma requisição será realizada.
        """
        for interval in yearly_window(self.start_date, self.end_date):
            yield self.interval_request(
                response, interval.start.date(), interval.end.date()
            )

    def interval_request(self, form_response, start, end):
        formdata = {
            "__EVENTTARGET": "ctl00$body$btnBuscaPalavrachave",
            "ctl00$body$txtDtPeriodo": f"{start:%d/%m/%Y}-{end:%d/%m/%Y}",
        }
        return scrapy.FormRequest.from_response(
            form_response,
            formdata=formdata,
            errback=self.split_failed_interval,
            meta={"form_response": form_response, "interval": (start, end)},
        )

    def split_failed_interval(self, failure):
        """
        Divide ao meio um intervalo cuja busca falhou.

        Basta uma edição com problema no intervalo para o sistema responder com
        código 500 à busca inteira, o que faria todas as outras edições do ano se
        perderem. Dividindo o intervalo sucessivamente, apenas o dia problemático
        fica de fora.
        """
        if not failure.check(HttpError):
            self.logger.error(repr(failure))
            return

        form_response = failure.request.meta["form_response"]
        start, end = failure.request.meta["interval"]
        if start >= end:
            self.logger.warning(
                f"Unable to fetch gazettes for {start}: {failure.value}"
            )
            return

        middle = start + (end - start) // 2
        yield self.interval_request(form_response, start, middle)
        yield self.interval_request(form_response, middle + timedelta(days=1), end)

    def parse(self, response):
        editions_list = response.css("div.panel")

        for edition in editions_list:
            metadata = edition.css("div.panel-title ::text")
            edition_number = metadata.re_first(r"(\d+)/")
            raw_date = metadata.re_first(r"\d{2}/\d{2}/\d{4}")
            edition_date = datetime.strptime(raw_date, "%d/%m/%Y").date()

            url_path = edition.xpath(".//a[@onclick]").re_first(r"l=(.+)'")

            gazette_url = response.urljoin(
                f"diariooficial/diario?n=diario.pdf&l={url_path}"
            )

            yield Gazette(
                date=edition_date,
                edition_number=edition_number,
                file_urls=[gazette_url],
                is_extra_edition=False,
                power="executive",
            )
