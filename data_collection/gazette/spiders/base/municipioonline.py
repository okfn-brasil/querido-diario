from collections import deque
from datetime import datetime, timedelta
from itertools import islice

import scrapy
from dateutil.rrule import YEARLY, rrule

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class BaseMunicipioOnlineSpider(BaseGazetteSpider):
    custom_settings = {
        "DOWNLOAD_DELAY": 0.5,
        "RANDOMIZE_DOWNLOAD_DELAY": True,
    }

    allowed_domains = ["municipioonline.com.br"]

    def start_requests(self):
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
        dates_of_interest = [
            dt
            for dt in rrule(freq=YEARLY, dtstart=self.start_date, until=self.end_date)
        ]

        if self.end_date not in dates_of_interest:
            dates_of_interest.append(self.end_date)

        for filter_start, filter_end in self._sliding_window(dates_of_interest, 2):
            if dates_of_interest[-1] != filter_end:
                filter_end -= timedelta(days=1)

            filter_start = filter_start.strftime("%d/%m/%Y")
            filter_end = filter_end.strftime("%d/%m/%Y")

            formdata = {
                "__EVENTTARGET": "ctl00$body$btnBuscaPalavrachave",
                "ctl00$body$txtDtPeriodo": f"{filter_start}-{filter_end}",
            }

            yield scrapy.FormRequest.from_response(response, formdata=formdata)

    def _sliding_window(self, iterable, n):
        it = iter(iterable)
        window = deque(islice(it, n - 1), maxlen=n)
        for x in it:
            window.append(x)
            yield tuple(window)

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
