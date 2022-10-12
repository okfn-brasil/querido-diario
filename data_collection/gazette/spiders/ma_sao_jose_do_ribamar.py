import ast
import json
import re
from datetime import date, datetime
from urllib.parse import urljoin

from dateutil.relativedelta import relativedelta
from scrapy import Request

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class MaSaoJoseDoRibamar(BaseGazetteSpider):
    name = "ma_sao_jose_do_ribamar_debug"
    TERRITORY_ID = "2111201"
    allowed_domains = ["saojosederibamar.ma.gov.br"]
    start_url = "https://www.saojosederibamar.ma.gov.br/diario-eletronico"
    open_file_url = "https://www.saojosederibamar.ma.gov.br/abrir_arquivo.aspx?cdLocal=12&arquivo={}{}"
    start_date = date(2015, 12, 1)
    ITEMS_PER_PAGE = "100"
    current_page = 0
    current_power = None
    crawled_power_stack = []
    power_codes = {1: "legislative", 3: "executive", 8: "executive_legislative"}

    def start_requests(self):
        yield Request(self.start_url, dont_filter=True, callback=self.ajaxpro_request)

    def ajaxpro_request(self, response):
        request_path = urljoin(self.start_url, self.get_path_to_request_items(response))

        yield Request(
            request_path,
            method="POST",
            headers={
                "X-AjaxPro-Method": "GetDiario",
            },
            body=self.make_body(),
        )

    def get_path_to_request_items(self, response):
        scripts = response.xpath("//script//@src").extract()
        endpoint = next(path for path in scripts if "diel_diel_lis" in path)
        return endpoint

    def make_body(self):
        self.update_current_power()
        return json.dumps(
            {
                "Page": self.current_page,
                "cdCaderno": self.current_power,
                "Size": self.ITEMS_PER_PAGE,
                "dtDiario_menor": self.timestamp_to_system_date(self.start_date),
                "dtDiario_maior": self.timestamp_to_system_date(self.end_date),
                "dsPalavraChave": "",
                "nuEdicao": -1,
            }
        )

    def update_current_power(self):
        if self.current_page != 0:
            return

        uncrawled_codes = list(
            set(self.power_codes).difference(self.crawled_power_stack)
        )

        if uncrawled_codes:
            self.current_power = uncrawled_codes[0]
        return

    def is_body_empty(self, response):
        return response.body == "null;/*".encode()

    @staticmethod
    def timestamp_to_system_date(timestamp):
        return {
            "__type": "System.DateTime",
            "Year": timestamp.year,
            "Month": timestamp.month,
            "Day": timestamp.day,
            "Hour": 0,
            "Millisecond": 0,
            "Minute": 0,
            "Second": 0,
        }

    def system_date_to_date(self, system_date):
        if system_date[1] == 0:
            system_date = system_date[:1] + (1,) + system_date[2:]

        try:
            return datetime.date(datetime(*system_date)) + relativedelta(months=+1)

        except ValueError:
            system_date = system_date[:1] + (system_date[1] + 1, 1) + system_date[3:]
            if system_date[1] > 12:
                system_date = (system_date[0] + 1,) + (1, 1) + system_date[3:]
            return datetime.date(datetime(*system_date)) + relativedelta(months=+1)

    def parse(self, response):
        self.logger.debug(
            "######################################################################################## \n"
        )
        self.logger.debug(f"SCRAPPING POWER: {self.current_power}\n)")
        self.logger.debug(f"SCRAPPING PAGE: {self.current_page}\n")
        if self.is_body_empty(response) and len(self.crawled_power_stack) == len(
            self.power_codes
        ):
            return

        elif self.is_body_empty(response):
            self.current_page = 0
            self.crawled_power_stack.append(self.current_power)
            yield Request(
                self.start_url, dont_filter=True, callback=self.ajaxpro_request
            )

        else:
            for gazette in self.parse_ajaxpro_response(response):
                url = self.open_file_url.format(
                    gazette["NMARQUIVO"], gazette["NMEXTENSAOARQUIVO"]
                )
                yield Gazette(
                    date=self.system_date_to_date(gazette["DTPUBLICACAO"]),
                    file_urls=[url],
                    is_extra_edition=self.current_power == 8,
                    territory_id=self.TERRITORY_ID,
                    power=self.power_codes[self.current_power],
                    scraped_at=datetime.utcnow(),
                )

            self.current_page += 1
            yield Request(
                self.start_url, dont_filter=True, callback=self.ajaxpro_request
            )

    def parse_ajaxpro_response(self, response):
        content = re.findall(
            r"new Ajax\.Web\.DataTable\((?P<conteudo>.*)\);",
            response.body.decode("utf-8"),
        )[0]

        content = ast.literal_eval(
            content.replace("new Date", "").replace("null", "None")
        )
        arg_names, arg_values = content

        parsed_response = []
        for row in arg_values:
            parsed_response.append(dict(zip([key[0] for key in arg_names], row)))
        return parsed_response
