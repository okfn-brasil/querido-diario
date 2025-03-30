import json
import re
from datetime import datetime
from urllib.parse import urlparse

from scrapy import Request
from scrapy.http import JsonRequest

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider
from gazette.utils.dates import monthly_window


class BaseDiofSpider(BaseGazetteSpider):
    """
    Base Spider for all cases that use DIOF/SAI service

    Attributes
    ----------
    website : str
        It must be defined in child classes.
        Refers to the URL of the page where humens access gazettes
        e.g:
            - https://diario.igaci.al.gov.br
            - https://sai.io.org.br/ba/abare/site/diariooficial
            - https://dom.imap.org.br/sitesMunicipios/imprensaOficial.cfm?varCodigo=219
    """

    custom_settings = {"DOWNLOAD_DELAY": 0.5}
    handle_httpstatus_list = [404]

    api_url = "https://diof.io.org.br/api"

    def __init__(self, *args, **kwargs):
        super(BaseDiofSpider, self).__init__(*args, **kwargs)

        domains = {
            "sai.io.org.br",
            "dom.imap.org.br",
            "diof.io.org.br",
            urlparse(self.website).netloc,
        }
        self.allowed_domains = list(domains)

    def start_requests(self):
        if "sai.io" in self.website or "dom.imap" in self.website:
            yield Request(
                self.website,
                callback=self.interval_request,
            )
        else:
            headers = {
                "Accept": "application/json, text/plain, */*",
                "Accept-Encoding": "gzip, deflate, br, zstd",
                "Accept-Language": "en-US,en;q=0.9",
                "Origin": self.website,
                "Referer": self.website,
            }
            yield Request(
                f"{self.api_url}/dados-cliente/info/",
                headers=headers,
                callback=self.interval_request,
            )

    def interval_request(self, response):
        self._get_client_id(response)

        for interval in monthly_window(
            self.start_date, self.end_date, format="%Y-%m-%d"
        ):
            data = {
                "cod_cliente": f"{self.client_id}",
                "dat_envio_ini": f"{interval.start}",
                "dat_envio_fim": f"{interval.end}",
                "des_observacao": "",
                "edicao": None,
            }
            yield JsonRequest(
                url=f"{self.api_url}/diario-oficial/edicoes-anteriores-group",
                data=data,
                callback=self.parse_items,
            )

    def parse_items(self, response):
        """
        The SAI service appears to be migrating its backend to consume a DIOF API,
        but some gazettes are only collectible through the old URL. So, this method
        checks whether the document exists in the new URL and, if not, collects
        it using the old URL.
        """

        for gazette_date in json.loads(response.text):
            for gazette in gazette_date["elements"]:
                date = gazette["dat_envio"]
                path = gazette["des_arquivoa4"]
                number = gazette["cod_documento"]

                first_option_url = f"{self.api_url}/diario-oficial/download/{path}.pdf"
                second_option_url = f"https://sai.io.org.br/Handler.ashx?f=diario&query={number}&c={self.client_id}&m=0"

                metadata = {
                    "date": datetime.fromisoformat(date).date(),
                    "edition_number": f"{number}",
                    "is_extra_edition": False,
                    "power": self.power,
                    "file_urls": [first_option_url],
                }

                yield Request(
                    first_option_url,
                    callback=self.collect_gazette,
                    dont_filter=True,
                    cb_kwargs={
                        "metadata": metadata,
                        "optional_url": second_option_url,
                    },
                )

    def collect_gazette(self, response, metadata, optional_url):
        if response.status != 200:
            metadata["file_urls"] = [optional_url]

        yield Gazette(**metadata)

    def _get_client_id(self, response):
        if "sai.io" in response.url:
            self.client_id = re.search(
                r"\d+", response.css("iframe").attrib["src"]
            ).group()
        elif "dom.imap" in response.url:
            self.client_id = re.search(r"varCodigo=(\d+)", response.url).group(1)
        else:
            self.client_id = response.json()["cod_cliente"]
