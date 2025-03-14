import datetime
import re
import scrapy
from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider
import dateparser


class ToPortoNacionalSpider(BaseGazetteSpider):
    TERRITORY_ID = "1718204"
    name = "to_porto_nacional"
    allowed_domains = ["diariooficial.portonacional.to.gov.br"]
    start_urls = ["https://diariooficial.portonacional.to.gov.br/edicoes"]    
    start_date = datetime.date(2021, 2, 25)
    end_date = datetime.datetime.today().date()
       
    def parse(self, response):
            
        editions = response.xpath('//table[@class="table"]/tbody/tr')    
        for edition in editions:
            
            link = edition.xpath('./td[3]/div/a/@href').get()
            title = edition.xpath('./td[1]/strong/text()').get()
            edition_number = re.search(r'EDIÇÃO Nº (\d+)', title).group(1)
            date_text = edition.xpath('./td[1]/br/following-sibling::text()').get().strip()
            date = dateparser.parse(date_text, languages=["pt"]).date()
            is_extra_edition = "suplement" in title.lower()
            
            if date < self.start_date:
                return
            
            if date <= self.end_date:
                
                gazette_item = Gazette(
                    date=date,
                    edition_number=edition_number, 
                    file_urls=[link], 
                    power="executive",
                    is_extra_edition=is_extra_edition,
                    )
                
                yield gazette_item
        
        next_page_link = response.xpath('//a[@rel="next"]/@href').get()
        
        if next_page_link:
            yield scrapy.Request( 
                url=next_page_link,
                callback=self.parse,
            ) 