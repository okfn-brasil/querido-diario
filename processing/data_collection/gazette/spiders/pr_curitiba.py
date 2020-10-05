from dateparser import parse
from datetime import date, datetime

import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class PrCuritibaSpider(BaseGazetteSpider):
    TERRITORY_ID = "4106902"
    name = "pr_curitiba"
    allowed_domains = ["legisladocexterno.curitiba.pr.gov.br"]
    custom_settings = {"DEFAULT_REQUEST_HEADERS": {"user-agent": "Mozilla/5.0"}}

    def start_requests(self):
        yield scrapy.Request(
            "https://legisladocexterno.curitiba.pr.gov.br/DiarioConsultaExterna_Pesquisa.aspx",
            callback=self.fetch_years,
        )

    def fetch_years(self, response):
        years_available = response.xpath(
            "//select[@id='ctl00_cphMasterPrincipal_ddlGrAno']/option/@value"
        ).getall()
        for year in years_available:
            yield scrapy.FormRequest.from_response(
                response,
                formdata={"ctl00$cphMasterPrincipal$ddlGrAno": str(year)},
                meta={"year": int(year)},
                callback=self.parse_year,
            )

    def parse_year(self, response):
        for month in range(12):
            if date(response.meta["year"], month + 1, 1) <= date.today():
                formdata = {
                    "__EVENTTARGET": "ctl00$cphMasterPrincipal$TabContainer1",
                    "__EVENTARGUMENT": f"activeTabChanged:{month}",
                    "ctl00_cphMasterPrincipal_TabContalegacyDealPooliner1_ClientState": '{{"ActiveTabIndex":{},"TabState":[true,true,true,true,true,true,true,true,true,true,true,true]}}',
                }
                yield scrapy.FormRequest.from_response(
                    response,
                    formdata=formdata,
                    meta={"month": month},
                    callback=self.parse_month,
                )

    def parse_month(self, response):
        page_count = len(response.css(".grid_Pager:nth-child(1) table td").extract())
        month = response.meta["month"]
        # The first page of pagination cannot be accessed by page number
        yield scrapy.FormRequest.from_response(
            response,
            formdata={
                "__EVENTTARGET": "ctl00$cphMasterPrincipal$TabContainer1",
                "ctl00_cphMasterPrincipal_TabContalegacyDealPooliner1_ClientState": '{{"ActiveTabIndex":{},"TabState":[true,true,true,true,true,true,true,true,true,true,true,true]}}',
                "__EVENTARGUMENT": f"activeTabChanged:{month}",
            },
            callback=self.parse_page,
        )
        for page_number in range(2, page_count + 1):
            yield scrapy.FormRequest.from_response(
                response,
                formdata={
                    "__EVENTARGUMENT": f"Page${page_number}",
                    "__EVENTTARGET": "ctl00$cphMasterPrincipal$gdvGrid2",
                },
                callback=self.parse_page,
            )

    def parse_page(self, response):
        for idx, row in enumerate(response.css(".grid_Row")):
            pdf_date = row.css("td:nth-child(2) span ::text").extract_first()
            gazette_id = row.css("td:nth-child(3) a ::attr(data-teste)").extract_first()
            parsed_date = parse(f"{pdf_date}", languages=["pt"]).date()
            if gazette_id == "0":
                starting_offset = 3
                formdata = {
                    "__LASTFOCUS": "",
                    "__EVENTTARGET": f"ctl00$cphMasterPrincipal$gdvGrid2$ctl{idx + starting_offset:02d}$lnkVisualizar",
                    "__EVENTARGUMENT": "",
                    "__ASYNCPOST": "true",
                }
                yield scrapy.FormRequest.from_response(
                    response,
                    formdata=formdata,
                    callback=self.parse_regular_edition,
                    meta={"parsed_date": parsed_date},
                )
            else:
                yield Gazette(
                    date=parsed_date,
                    file_urls=[
                        f"https://legisladocexterno.curitiba.pr.gov.br/DiarioSuplementoConsultaExterna_Download.aspx?Id={gazette_id}"
                    ],
                    is_extra_edition=True,
                    territory_id=self.TERRITORY_ID,
                    power="executive_legislature",
                    scraped_at=datetime.utcnow(),
                )

    def parse_regular_edition(self, response):
        parsed_date = response.meta["parsed_date"]
        gazette_id = response.selector.re_first("Id=(\d+)")
        return Gazette(
            date=parsed_date,
            file_urls=[
                f"https://legisladocexterno.curitiba.pr.gov.br/DiarioConsultaExterna_Download.aspx?Id={gazette_id}"
            ],
            is_extra_edition=False,
            territory_id=self.TERRITORY_ID,
            power="executive_legislature",
            scraped_at=datetime.utcnow(),
        )
