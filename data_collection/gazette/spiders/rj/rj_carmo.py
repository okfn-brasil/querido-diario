from datetime import date, datetime
from urllib import parse

from gazette.utils.extraction import get_date_from_text
from gazette.items import Gazette
from scrapy import Request
from gazette.spiders.base import BaseGazetteSpider

class UFMunicipioSpider(BaseGazetteSpider):
    name = "rj_carmo"
    TERRITORY_ID = "3301207"
    allowed_domains = ["gesdom.carmo.rj.gov.br"]
    start_urls = ["https://gesdom.carmo.rj.gov.br/consulta_publica_todas_edicoes"]
    start_date = date(2021, 7, 6)
    pdf_base_url = "https://gesdom.carmo.rj.gov.br/_lib/file/doc/pdf/"

    def __init__(self, *args, **kwargs):
        """
        Garante que start_date e end_date sejam objetos date,
        mesmo se passados como string pela linha de comando.
        """
        super().__init__(*args, **kwargs)

        if isinstance(self.start_date, str):
            self.start_date = datetime.date.fromisoformat(self.start_date)
        # Garante que end_date também seja um objeto date
        if isinstance(self.end_date, str):
            self.end_date = datetime.date.fromisoformat(self.end_date)

    def start_requests(self):
        yield self.make_request(parm=1)

    def make_request(self, parm: int):
        payload = f"nmgp_opcao=ajax_navigate&script_case_init=9183&opc=rec&parm={parm}"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
        }
        return Request(
            url=self.start_urls[0],
            method="POST",
            body=payload,
            headers=headers,
            callback=self.parse,
            cb_kwargs={"parm": parm},
        )

    def parse_pdf(self, data):
        start_string = "var urlPDF = '\\/_lib\\/file\\/doc\\/pdf\\/' + '"
        end_string = ".pdf';"

        start_index = data.find(start_string) + len(start_string)
        end_index = data.find(end_string) + len(end_string) - 2 # Só até .pdf

        filename = data[start_index:end_index]
        url = self.pdf_base_url + filename

        return url

    def parse_date(self, data, id):
        start_string = f'id_sc_field_data_edicao_{id}">'
        start_index = data.find(start_string) + len(start_string)
        end_index = start_index + 12 # dd\/mm\/yyyy

        raw_date = data[start_index:end_index].replace('\\', '')
        try:
            return datetime.strptime(raw_date, '%d/%m/%Y')
        except ValueError:
            return get_date_from_text(raw_date)

    def parse_edition(self, pdf_url):
        start_index = pdf_url.find('/pdf/')
        end_index = pdf_url.find(' Prefeitura')
        return pdf_url[start_index+5:end_index]
    
    def parse_extra_edition(self, data, id):
        start_string = f'id_sc_field_informacoes_{id}">EDIÇÃO '
        start_index = data.find(start_string) + len(start_string)
        if 'extra' in data[start_index:start_index+5].lower():
            return True
        return False

    def parse(self, response, parm):
        """Processa o JSON retornado e continua até scrollEOF=True."""
        data = response.body.decode() # str
        data = data.encode("utf-8").decode("unicode_escape")

        pdf_url = self.parse_pdf(data)
        date = self.parse_date(data,id=parm)
        edition = self.parse_edition(pdf_url)
        is_extra = self.parse_extra_edition(data, id=parm)
        is_last = 'EOF":true' in data

        print(f"Processing id {parm}")
        print(data)
        print(f"pdf_url: {pdf_url}")
        print(f"date: {date}")
        print(f"edition: {edition}")
        print(f"is_extra: {is_extra}")
        print()

        yield Gazette(
            date=date,
            edition_number=edition,
            is_extra_edition=False,
            file_urls=[pdf_url],
            power="executive",
        )

        # Continua o loop até o backend sinalizar o fim
        if not is_last:
            next_parm = parm + 1
            yield self.make_request(parm=next_parm)


