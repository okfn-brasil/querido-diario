"""pr_curitiba spider.

This website is built with ASP.NET, using VIEWSTATES and other types of formdata keys
to validate that certain flows aren't followed (like not being able to paginate the
months of a year which is not the current response).

That's why so many `FormRequest.from_response` are necessary, to catch those formdata
keys dynamically as they are hidden inputs in the page.
"""

import datetime as dt

import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class PrCuritibaSpider(BaseGazetteSpider):
    name = "pr_curitiba"
    TERRITORY_ID = "4106902"
    start_urls = [
        "https://legisladocexterno.curitiba.pr.gov.br/DiarioConsultaExterna_Pesquisa.aspx"
    ]
    start_date = dt.date(1993, 1, 5)

    def parse(self, response):
        year_select = response.xpath("//select[contains(@id, 'ddlGrAno')]")
        year_formkey = year_select.attrib["name"]
        years_available = map(int, year_select.xpath("./option/@value").getall())
        for year in years_available:
            if not self.start_date.year <= year <= self.end_date.year:
                continue

            if year == dt.date.today().year:
                yield from self.parse_year(response, year)
                continue

            yield scrapy.FormRequest.from_response(
                response,
                formdata={year_formkey: str(year)},
                callback=self.parse_year,
                cb_kwargs={"year": year},
            )

    def parse_year(self, response, year):
        first_day_of_start_date_month = dt.date(
            self.start_date.year, self.start_date.month, 1
        )
        for month in range(1, 13):
            first_day_of_month = dt.date(year, month, 1)
            if not first_day_of_start_date_month <= first_day_of_month <= self.end_date:
                continue

            if month == dt.date.today().month:
                yield from self.parse_editions_list(response)
                continue

            formdata = {
                "__EVENTTARGET": "ctl00$cphMasterPrincipal$TabContainer1",
                "__EVENTARGUMENT": f"activeTabChanged:{month - 1}",
                "ctl00_cphMasterPrincipal_TabContalegacyDealPooliner1_ClientState": '{{"ActiveTabIndex":{},"TabState":[true,true,true,true,true,true,true,true,true,true,true,true]}}',
            }
            yield scrapy.FormRequest.from_response(
                response,
                formdata=formdata,
                callback=self.parse_editions_list,
            )

    def parse_editions_list(self, response, current_page=1):
        for row in response.css(".grid_Row"):
            date = self._parse_date(row.xpath("./td[2]/span/text()").get())

            if date > self.end_date:
                continue
            elif date < self.start_date:
                return

            text = row.xpath("./td[1]/span/text()")
            edition_number = text.re_first(r"\d+")
            gazette_item = Gazette(
                date=date,
                edition_number=edition_number,
                is_extra_edition=False,
                power="executive_legislative",
            )

            is_supplement = "supl" in text.get().lower()
            if is_supplement:
                gazette_id = row.xpath("./td[3]/a/@data-teste").get()
                url = f"https://legisladocexterno.curitiba.pr.gov.br/DiarioSuplementoConsultaExterna_Download.aspx?Id={gazette_id}"
                gazette_item["file_urls"] = [url]
                yield gazette_item
            else:
                # Regular editions need an extra request to discover the gazette id
                eventtarget = row.xpath("./td[3]/a/@href").re_first(
                    r"'(.*lnkVisualizar)'"
                )
                yield scrapy.FormRequest.from_response(
                    response,
                    formdata={"__EVENTTARGET": eventtarget},
                    callback=self.parse_regular_edition,
                    cb_kwargs={"gazette_item": gazette_item},
                )

        number_of_pages = len(
            response.css(".grid_Pager:nth-child(1) table td").getall()
        )
        if current_page < number_of_pages:
            yield scrapy.FormRequest.from_response(
                response,
                formdata={
                    "__EVENTARGUMENT": f"Page${current_page + 1}",
                    "__EVENTTARGET": "ctl00$cphMasterPrincipal$gdvGrid2",
                },
                callback=self.parse_editions_list,
                cb_kwargs={"current_page": current_page + 1},
            )

    def parse_regular_edition(self, response, gazette_item):
        gazette_id = response.selector.re_first(r"Id=(\d+)")
        url = f"https://legisladocexterno.curitiba.pr.gov.br/DiarioConsultaExterna_Download.aspx?Id={gazette_id}"
        gazette_item["file_urls"] = [url]
        yield gazette_item

    def _parse_date(self, raw_date):
        return dt.datetime.strptime(raw_date, "%d/%m/%Y").date()
