from datetime import date 

from gazette.items import Gazette 
from gazette.spiders.base.doem import DoemGazetteSpider 

class BaTeixeiraDeFreitasSpider(DoemGazetteSpider):
    TERRITORY_ID = "2931350"
    name = "ba_teixeira_de_freitas"
    state_city_url_part = "ba/teixeiradefreitas"
    start_date = date(2014, 12, 31) 
    url_base = "http://diario2.teixeiradefreitas.ba.gov.br"
    
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
