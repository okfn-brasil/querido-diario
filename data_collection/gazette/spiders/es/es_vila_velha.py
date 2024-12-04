import datetime as dt
import re

from scrapy import FormRequest, Request

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class VilaVelhaSpider(BaseGazetteSpider):
    TERRITORY_ID = "3205200"
    name = "es_vila_velha"
    start_date = dt.date(2016, 7, 1)
    allowed_domains = ["diariooficial.vilavelha.es.gov.br"]

    BASE_URL = "https://diariooficial.vilavelha.es.gov.br/Default.aspx"

    def start_requests(self):
        start_date = self.start_date.strftime("%d/%m/%Y")
        end_date = self.end_date.strftime("%d/%m/%Y")
        url = f"{self.BASE_URL}?dataInicial={start_date}&dataFinal={end_date}"
        yield Request(url)

    def parse(self, response, page=1):
        pagination = response.css("tr.pagination-ys")

        for row in response.css("table#ctl00_cpConteudo_gvDocumentos > tr"):
            element_is_pagination = self._element_is_pagination(row, pagination)
            if element_is_pagination:
                continue

            title = row.css("td span::text")
            is_extra_edition = "extra" in title.get().lower()
            edition_number = title.re_first(r"Edição nº (\d+)")
            raw_date = title.re_first(r"\d{2}-\d{2}-\d{4}")
            date = dt.datetime.strptime(raw_date, "%d-%m-%Y").date()

            formdata = self._extract_form_fields(row.css("td a::attr(href)").get())
            document_request = FormRequest.from_response(
                response,
                formdata=formdata,
            )

            yield Gazette(
                date=date,
                file_requests=[document_request],
                edition_number=edition_number,
                is_extra_edition=is_extra_edition,
                power="executive_legislative",
            )

        if not pagination:
            return

        next_page = pagination.xpath(
            f"//a[contains(@href, 'Page${page + 1}')]/@href"
        ).get()
        if next_page:
            formdata = self._extract_form_fields(next_page)
            yield FormRequest.from_response(
                response, formdata=formdata, cb_kwargs={"page": page + 1}
            )

    def _element_is_pagination(self, element, pagination_selector_list):
        if not pagination_selector_list:
            return False
        return element.get() == pagination_selector_list[0].get()

    def _extract_form_fields(self, text):
        target_and_argument = re.search(
            r"javascript:__doPostBack\('(.*)','(.*)'\)", text
        )

        if not target_and_argument:
            raise Exception(
                "Regex for event target and argument extraction does not work"
            )

        return {
            "__EVENTTARGET": target_and_argument.group(1),
            "__EVENTARGUMENT": target_and_argument.group(2),
        }
