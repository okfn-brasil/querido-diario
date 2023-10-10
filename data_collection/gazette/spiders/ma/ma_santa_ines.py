from datetime import date, datetime

from scrapy import FormRequest, Request, Selector

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class MaSantaInes(BaseGazetteSpider):
    name = "ma_santa_ines"
    TERRITORY_ID = "2109908"
    start_date = date(2021, 9, 10)  # edition_number 01
    allowed_domains = ["santaines.ma.gov.br"]

    def start_requests(self):
        yield Request(
            url="https://santaines.ma.gov.br/diario-oficial-do-municipio-2/",
            callback=self.parse_initial_page,
        )

    def parse_initial_page(self, response):
        wdtNonce_value = response.xpath(
            "//input[@type='hidden' and @id='wdtNonceFrontendEdit_2']/@value"
        ).get()

        date_interval = (
            f"{self.start_date.strftime('%d/%m/%Y')}"
            "|"
            f"{self.end_date.strftime('%d/%m/%Y')}"
        )

        form_data = {
            "draw": "2",
            "columns[0][data]": "0",
            "columns[0][name]": "wdt_ID",
            "columns[0][searchable]": "true",
            "columns[0][orderable]": "true",
            "columns[0][search][value]": "",
            "columns[0][search][regex]": "false",
            "columns[1][data]": "1",
            "columns[1][name]": "edio",
            "columns[1][searchable]": "true",
            "columns[1][orderable]": "true",
            "columns[1][search][value]": "",
            "columns[1][search][regex]": "false",
            "columns[2][data]": "2",
            "columns[2][name]": "data",
            "columns[2][searchable]": "true",
            "columns[2][orderable]": "true",
            "columns[2][search][value]": date_interval,
            "columns[2][search][regex]": "false",
            "columns[3][data]": "3",
            "columns[3][name]": "sumrio",
            "columns[3][searchable]": "true",
            "columns[3][orderable]": "true",
            "columns[3][search][value]": "",
            "columns[3][search][regex]": "false",
            "columns[4][data]": "4",
            "columns[4][name]": "tipopublicao",
            "columns[4][searchable]": "true",
            "columns[4][orderable]": "true",
            "columns[4][search][value]": "",
            "columns[4][search][regex]": "false",
            "columns[5][data]": "5",
            "columns[5][name]": "arquivo",
            "columns[5][searchable]": "true",
            "columns[5][orderable]": "true",
            "columns[5][search][value]": "",
            "columns[5][search][regex]": "false",
            "order[0][column]": "2",
            "order[0][dir]": "desc",
            "start": "0",
            "length": "-1",  # retrieves all data in the interval in a single response
            "search[value]": "",
            "search[regex]": "false",
            "wdtNonce": wdtNonce_value,
            "sRangeSeparator": "|",
        }

        yield FormRequest(
            url="https://santaines.ma.gov.br/wp-admin/admin-ajax.php?action=get_wdtable&table_id=2",
            method="POST",
            formdata=form_data,
            callback=self.parse_gazette_list,
        )

    def parse_gazette_list(self, response):
        json_response = response.json()

        for entry in json_response["data"]:
            if not entry:
                continue

            raw_edition_number = entry[1].strip()
            raw_gazette_date = entry[2].strip()
            raw_publication_type = entry[4].strip()
            raw_link_node = entry[5].strip()

            gazette_date = datetime.strptime(raw_gazette_date, "%d/%m/%Y").date()

            if self.end_date < gazette_date:
                continue

            if gazette_date < self.start_date:
                break

            edition_number = raw_edition_number.split()[1]
            url = Selector(text=raw_link_node).xpath("//a/@href").get()
            is_extra_edition = raw_publication_type != "Executivo"

            yield Gazette(
                edition_number=edition_number,
                date=gazette_date,
                file_urls=[url],
                is_extra_edition=is_extra_edition,
                power="executive",
            )
