from dateparser import parse
import datetime as dt
import re

import scrapy


from gazette.items import Gazette

class PrCuritibaSpider(scrapy.Spider):
    MUNICIPALITY_ID = '4106902'
    name = 'pr_curitiba'
    allowed_domains = ['legisladocexterno.curitiba.pr.gov.br']
    start_urls = ['http://legisladocexterno.curitiba.pr.gov.br/DiarioConsultaExterna_Pesquisa.aspx']


    def parse(self, response):
        """
        The Curitiba website is a statefull page, so we can't just build the
        request from zero, we have to resend the viewstate with every request.
        @url http://legisladocexterno.curitiba.pr.gov.br/DiarioConsultaExterna_Pesquisa.aspx
        @returns requests 1
        """
        todays_date = dt.date.today()
        current_year = todays_date.year
        current_month = todays_date.month
        yield self.scrap_year(response, 2015)

    def scrap_year(self, response, year):
        return scrapy.FormRequest.from_response(
            response,
            formdata={
                'ctl00$cphMasterPrincipal$ddlGrAno': str(year)
            },
            callback=self.parse_year
        )


    def parse_year(self, response):
        for i in range(12):
            yield self.scrap_month(response, i)

    def scrap_month(self, response, month):
        return scrapy.FormRequest.from_response(
            response,
            formdata={
                'ctl00_cphMasterPrincipal_TabContainer1_ClientState' : '{{"ActiveTabIndex":{},"TabState":[true,true,true,true,true,true,true,true,true,true,true,true]}}'.format(month)
            },
            callback=self.parse_month,
        )

    def parse_month(self, response):
        #Count how many pages and iterate
        page_count = len(response.css(".grid_Pager:nth-child(1) table td").extract())
        for page_number in range(1,page_count + 1):
            yield scrapy.FormRequest.from_response(
                response,
                formdata={
                    '__EVENTARGUMENT' : 'Page${}'.format(page_number),
                    '__EVENTTARGET' : 'ctl00$cphMasterPrincipal$gdvGrid2'
                },
                callback=self.parse_page,
            )

    def parse_page(self, response):
        gazettes = []

        numbers = response.css(".grid_Row td:nth-child(1) span ::text").extract()
        pdf_dates = response.css(".grid_Row td:nth-child(2) span ::text").extract()
        ids = response.css(".grid_Row td:nth-child(3) a ::attr(data-teste)").extract()
        print("Lengths {0} {1} {2}".format(len(numbers), len(pdf_dates), len(ids)))
        for i in range(len(numbers)):
            number = numbers[i]
            pdf_date = pdf_dates[i]
            id = ids[i]
            parsed_date = parse(f'{pdf_date}', languages=['pt']).date()
            if id == '0':
                yield scrapy.FormRequest.from_response(response,
                                                       headers = {
                                                           'user-agent': 'Mozilla/5.0',
                                                       },
				                                       formdata = {
					                                       '__LASTFOCUS': '',
				                                           '__EVENTTARGET': 'ctl00$cphMasterPrincipal$gdvGrid2$ctl{num:02d}$lnkVisualizar'.format(num=(i+3)),
					                                       '__EVENTARGUMENT': '',
                                                           '__ASYNCPOST': 'true'
				                                       },
                                                       callback=self.scrap_not_extra_edition,
                                                       meta={"gazettes": gazettes, "parsed_date": parsed_date}
                )

                #gazettes.append(yield self.scrap_not_extra_edition(response, i))
            else:
                gazettes.append(Gazette(
                    date = parsed_date,
                    file_urls=["http://legisladocexterno.curitiba.pr.gov.br/DiarioSuplementoConsultaExterna_Download.aspx?id={}".format(id)],
                    is_extra_edition= True,
                    municipality_id=self.MUNICIPALITY_ID,
                    power='executive_legislature',
                    scraped_at=dt.datetime.utcnow()
                ))

        return []#gazettes

    def scrap_not_extra_edition(self, response):
        gazettes = response.meta['gazettes']
        parsed_date = response.meta['parsed_date']
        id = re.findall(r'Id=(\d+)', response.text )
        gazettes.append(Gazette(
            date = parsed_date,
            file_urls=["http://legisladocexterno.curitiba.pr.gov.br/DiarioConsultaExterna_Download.aspx?id={}".format(id)],
            is_extra_edition= False,
            municipality_id=self.MUNICIPALITY_ID,
            power='executive_legislature',
            scraped_at=dt.datetime.utcnow()
        ))
