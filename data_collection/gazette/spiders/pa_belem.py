import datetime
from urllib.parse import urlencode

import scrapy
from itemadapter import ItemAdapter

from gazette.items import Gazette
from gazette.pipelines import QueridoDiarioFilesPipeline
from gazette.spiders.base import BaseGazetteSpider


class PaBelemFilesPipeline(QueridoDiarioFilesPipeline):
    def get_media_requests(self, item, info):
        urls = ItemAdapter(item).get(self.files_urls_field, [])

        # We need to add this header to the requests that downloads
        # the files, or else we will receive just a JSON containing
        # meta information about the gazette
        headers = {"Accept": "application/octet-stream"}

        return [scrapy.Request(u, headers=headers) for u in urls]


class PaBelemSpider(BaseGazetteSpider):
    TERRITORY_ID = "1501402"
    name = "pa_belem"
    allowed_domains = ["sistemas.belem.pa.gov.br"]
    start_date = datetime.date(2005, 2, 1)

    BASE_URL = "https://sistemas.belem.pa.gov.br/diario-consulta-api/diarios"

    @classmethod
    def update_settings(cls, settings):
        super(PaBelemSpider, cls).update_settings(settings)
        files_pipeline_order = settings["ITEM_PIPELINES"].get(
            "gazette.pipelines.QueridoDiarioFilesPipeline", 300
        )

        # Disable default file item pipeline and enable customized
        settings["ITEM_PIPELINES"][
            "gazette.pipelines.QueridoDiarioFilesPipeline"
        ] = None
        settings["ITEM_PIPELINES"][
            "gazette.spiders.pa_belem.PaBelemFilesPipeline"
        ] = files_pipeline_order

    def start_requests(self):
        initial_date = self.start_date.strftime("%Y-%m-%dT00:00:00.000Z")
        end_date = datetime.date.today().strftime("%Y-%m-%dT00:00:00.000Z")

        params = {
            "dataRecebidoInicio": initial_date,
            "dataRecebidoFim": end_date,
            "start": "0",
        }
        encoded_params = urlencode(params)
        url = f"{self.BASE_URL}?{encoded_params}"

        yield scrapy.Request(url, callback=self.parse_get_number_of_items)

    def parse_get_number_of_items(self, response):
        number_of_documents = response.json()["response"]["numFound"]
        url = f"{self.BASE_URL}?start=0&rows={number_of_documents}"
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        data = response.json()["response"]

        for gazette_data in data["docs"]:
            gazette_date = datetime.datetime.strptime(
                gazette_data["data_publicacao"], "%Y-%m-%dT%H:%M:%SZ"
            ).date()
            edition_number = gazette_data["id"]

            url = f"{self.BASE_URL}/{edition_number}"
            yield Gazette(
                date=gazette_date,
                edition_number=edition_number,
                file_urls=[url],
                is_extra_edition=False,
                power="executive",
            )
