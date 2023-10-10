from datetime import date 

from gazette.items import Gazette 
from gazette.spiders.base.doem import DoemGazetteSpider 


class BaSentoSeSpider(DoemGazetteSpider):
    TERRITORY_ID = "2930204"
    name = "ba_sento_se"
    state_city_url_part = "ba/sentose"
    start_date = date(2017, 1, 2) 
    start_urls = "https://doem.org.br/ba/sentose/diarios/"

    def parse(self, response): 
     
        edition_links = response.css(".publicacao-item a::attr(href)").getall() 

        for edition_link in edition_links: 
            yield response.follow(edition_link, callback=self.parse_gazette)

    def parse_gazette(self, response): 
        date_str = response.css(".header-publicacao span::text").get() 
        gazette_date = date.fromisoformat(date_str)

        
        pdf_url = response.css(".btn-download-pdf::attr(href)").get()

        if pdf_url: 
            yield Gazette(
                date=gazette_date,
                file_urls=[pdf_url],
                power="executive", 
                is_extra_edition=False,
            )
        else:
            self.logger.error(f"Unable to retrieve PDF URL for {gazette_date}.")
