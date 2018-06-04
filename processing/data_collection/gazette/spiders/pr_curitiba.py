from dateparser import parse
import datetime as dt
import re

from gazette.spiders.base import BaseGazetteSpider

import scrapy

from gazette.items import Gazette


class PrCuritibaSpider(BaseGazetteSpider):
    MUNICIPALITY_ID = '4106902'
    name = 'pr_curitiba'
    allowed_domains = ['legisladocexterno.curitiba.pr.gov.br']
    start_urls = ['http://legisladocexterno.curitiba.pr.gov.br/DiarioConsultaExterna_Pesquisa.aspx']

    def start_requests(self):
        """
        The Curitiba website is a statefull page, so we can't just build the
        request from zero, we have to resend the viewstate with every request.
        @url http://legisladocexterno.curitiba.pr.gov.br/DiarioConsultaExterna_Pesquisa.aspx
        @returns requests 1
        """
        todays_date = dt.date.today()
        current_year = todays_date.year
        stop_on_year = 2015
        if hasattr(self, 'start_date'):
            stop_on_year = self.start_date.year
        for year in range(current_year, stop_on_year - 1, -1):
            yield scrapy.FormRequest(
                'http://legisladocexterno.curitiba.pr.gov.br/DiarioConsultaExterna_Pesquisa.aspx',
                formdata={
                    'ctl00$cphMasterPrincipal$ddlGrAno': str(year)
                },
                callback=self.parse_year
            )

    def parse_year(self, response):
        for i in range(12):
            yield self.scrape_month(response, i)

    def scrape_month(self, response, month):
        return scrapy.FormRequest.from_response(
            response,
            formdata={
                '__EVENTTARGET': 'ctl00$cphMasterPrincipal$TabContainer1',
                '__EVENTARGUMENT': 'activeTabChanged:{}'.format(month),
                'ctl00_cphMasterPrincipal_TabContalegacyDealPooliner1_ClientState': '{{"ActiveTabIndex":{},"TabState":[true,true,true,true,true,true,true,true,true,true,true,true]}}'.format(month)
            },
            meta={"month": month},
            callback=self.parse_month
        )

    def parse_month(self, response):
        page_count = len(response.css(".grid_Pager:nth-child(1) table td").extract())
        month = response.meta["month"]
        # The first page of pagination cannot be accessed by page number
        yield scrapy.FormRequest.from_response(
            response,
            formdata={
                '__EVENTTARGET': 'ctl00$cphMasterPrincipal$TabContainer1',
                'ctl00_cphMasterPrincipal_TabContalegacyDealPooliner1_ClientState': '{{"ActiveTabIndex":{},"TabState":[true,true,true,true,true,true,true,true,true,true,true,true]}}'.format(month),
                '__EVENTARGUMENT': 'activeTabChanged:{}'.format(month),
            },
            callback=self.parse_page,
        )
        for page_number in range(2, page_count + 1):
            yield scrapy.FormRequest.from_response(
                response,
                formdata={
                    '__EVENTARGUMENT': 'Page${}'.format(page_number),
                    '__EVENTTARGET': 'ctl00$cphMasterPrincipal$gdvGrid2'
                },
                callback=self.parse_page,
            )

    def parse_page(self, response):
        for idx, row in enumerate(response.css(".grid_Row")):
            pdf_date = row.css("td:nth-child(2) span ::text").extract_first()
            gazette_id = row.css("td:nth-child(3) a ::attr(data-teste)").extract_first()
            parsed_date = parse(f'{pdf_date}', languages=['pt']).date()
            if gazette_id == '0':
                starting_offset = 3
                yield scrapy.FormRequest.from_response(
                    response,
                    headers={'user-agent': 'Mozilla/5.0'},
                    formdata={
                        '__LASTFOCUS': '',
                        '__EVENTTARGET': 'ctl00$cphMasterPrincipal$gdvGrid2$ctl{num:02d}$lnkVisualizar'.format(num=(idx+starting_offset)),
                        '__EVENTARGUMENT': '',
                        '__ASYNCPOST': 'true'
                    },
                    callback=self.scrap_not_extra_edition,
                    meta={"parsed_date": parsed_date}
                )
            else:
                yield Gazette(
                    date=parsed_date,
                    file_urls=["http://legisladocexterno.curitiba.pr.gov.br/DiarioSuplementoConsultaExterna_Download.aspx?id={}".format(gazette_id)],
                    is_extra_edition=True,
                    municipality_id=self.MUNICIPALITY_ID,
                    power='executive_legislature',
                    scraped_at=dt.datetime.utcnow()
                )

    def scrap_not_extra_edition(self, response):
        parsed_date = response.meta['parsed_date']
        gazette_id = re.findall(r'Id=(\d+)', response.text)[0]
        return Gazette(
            date=parsed_date,
            file_urls=["http://legisladocexterno.curitiba.pr.gov.br/DiarioConsultaExterna_Download.aspx?id={}".format(gazette_id)],
            is_extra_edition=False,
            municipality_id=self.MUNICIPALITY_ID,
            power='executive_legislature',
            scraped_at=dt.datetime.utcnow()
        )
