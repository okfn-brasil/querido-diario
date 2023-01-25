import datetime
from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider

class SpSaoBernardoDoCampoSpider(BaseGazetteSpider):
    name = "sp_sao_bernardo_do_campo"
    TERRITORY_ID = "3548708"
    allowed_domains = ["saobernardo.sp.gov.br"]
    start_urls = ["https://www.saobernardo.sp.gov.br/web/sbc/todas-as-edicoes"]
    #No endereço há diários a partir de 2002 mas não há um padrão na nomenclatura e muitos diários não possuem data, por isso a coleta começa em 04/01/2017
    start_date = datetime.date(2017, 1, 4)  
    
    def parse(self, response): 
        for edition in response.xpath('//i[@class="icon-file"]/parent::*'): #O link pode ser identificado pela presença de um ícone de arquivo. O seletor que queremos é a tag pai"
            text = edition.css("a::text").get()
            if "Especial" in text or "Complementar" in text:
                is_extra_edition = True
            else:
                is_extra_edition = False
            href = edition.css("a::attr(href)").get()
            edition_number = edition.css("a::text").re_first(r"\d{4}")
            date = edition.css("a::text").re_first(r"\d{2}[./]\d{2}[./]\d{4}")
            if date:
                if "." in date:
                    date = datetime.datetime.strptime(date, "%d.%m.%Y").date()
                elif "/" in date:
                   date = datetime.datetime.strptime(date, "%d/%m/%Y").date()
            url = response.urljoin(edition.css("a::attr(href)").get())
          
            yield Gazette(
                date=date,
                edition_number = edition_number,
                file_urls=[url],
                is_extra_edition=is_extra_edition,
                power="executive_legislative",
            )    