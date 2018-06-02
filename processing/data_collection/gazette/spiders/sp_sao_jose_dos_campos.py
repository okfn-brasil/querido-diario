import dateparser

from datetime import datetime
from scrapy import FormRequest
from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class SpSaoJoseDosCamposSpider(BaseGazetteSpider):
    MUNICIPALITY_ID = '3549904'

    GAZETTE_NAME_CSS = 'td:last-child a::text'
    GAZETTE_URL_CSS = 'td:last-child a::attr(href)'
    GAZETTE_DATE_CSS = 'td:nth-child(2)::text'
    NEXT_PAGE_LINK_CSS = '.paginador_anterior_proxima a'
    JAVASCRIPT_POSTBACK_REGEX = r"javascript:__doPostBack\('(.*)',''\)"

    allowed_domains = ['servicos2.sjc.sp.gov.br']
    name = 'sp_sao_jose_dos_campos'
    start_urls = [
        'http://servicos2.sjc.sp.gov.br/servicos/portal_da_transparencia/boletim_municipio.aspx'
    ]

    def parse(self, response):
        """
        @url http://servicos2.sjc.sp.gov.br/servicos/portal_da_transparencia/boletim_municipio.aspx
        @returns requests 1
        @scrapes date file_urls is_extra_edition municipality_id power scraped_at
        """

        for element in response.css('#corpo table tr'):
            if element.css('th').extract():
                continue

            date = element.css(self.GAZETTE_DATE_CSS).extract_first()
            date = dateparser.parse(date, languages=['pt']).date()
            url = element.css(self.GAZETTE_URL_CSS).extract_first()
            is_extra_edition = 'Extra' in element.css(self.GAZETTE_NAME_CSS).extract_first()

            yield Gazette(
                date=date,
                file_urls=[url],
                is_extra_edition=is_extra_edition,
                municipality_id=self.MUNICIPALITY_ID,
                power='executive_legislature',
                scraped_at=datetime.utcnow(),
            )

        for element in response.css(self.NEXT_PAGE_LINK_CSS):
            if not element.css('a::text').extract_first() == 'Próxima':
                continue

            event_target = element.css('a::attr(href)').re(self.JAVASCRIPT_POSTBACK_REGEX).pop()

            yield FormRequest.from_response(
                response,
                callback=self.parse,
                formname="aspnetForm",
                formxpath="//form[@id='aspnetForm']",
                formdata={
                    '__EVENTARGUMENT': '',
                    '__EVENTTARGET': event_target
                },
                dont_click=True,
                dont_filter=True,
                method="POST"
            )
