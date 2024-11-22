from datetime import datetime

import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class BaseSiganetSpider(BaseGazetteSpider):
    # until now the base url for download is the same in both versions. No need to customise
    P_BASE_URL_DOWNLOAD = (
        "https://painel.siganet.net.br/upload/{}/cms/publicacoes/diario"
    )
    # P_VERSION
    # Version 1: (default) ma_coroata e ma_sao_jose_dos_basilios
    # Version 2: ma_sao_luis
    P_VERSION = "1"
    # values for default version 1
    P_MUST_GET_COOKIE = False  # Not needed in the default version
    P_URL_DIR_GET_COOKIE = ""  # Not needed in the default version
    P_URL_DIR_SEARCH = "listarDiario/"
    P_KEY_URL_FILENAME = "TDI_ARQUIVO"
    P_KEY_DATE = "TDI_DT_PUBLICACAO"
    P_KEY_EDITION_NUMBER = "TDI_EDICAO"
    P_KEY_EXTRA_EDITION = ""  # Not needed in the default version
    P_KEY_CLIENT_ID = "TDI_TPS_ID"
    P_CLIENT_ID = ""  # Not needed in the default version
    P_POWER = "executive_legislative"

    def set_version_params(self, version_number):
        # values for version 2
        if version_number == "2":
            self.P_MUST_GET_COOKIE = True
            self.P_URL_DIR_GET_COOKIE = (
                "todasEdicoes/"  # Not needed in the default version
            )
            self.P_URL_DIR_SEARCH = "pesquisaEdicoes/"
            self.P_KEY_URL_FILENAME = "TDO_ASSINADO_ARQUIVO"
            self.P_KEY_DATE = "TDO_DT_GERACAO"
            self.P_KEY_EDITION_NUMBER = "TDO_EDICAO"
            self.P_KEY_EXTRA_EDITION = "TDO_EDICAO_EXTRA"
            self.P_KEY_CLIENT_ID = "TDI_TPS_ID"
            self.P_CLIENT_ID = "485"
            self.P_POWER = "executive_legislative"

    def start_requests(self):
        # set the apropriate params according to the version
        self.set_version_params(self.P_VERSION)
        """must call the main page to get the cookie
        otherwise you can't get the json with the listing
        """
        if self.P_MUST_GET_COOKIE:
            yield scrapy.Request(
                f"{self.BASE_URL}/{self.P_URL_DIR_GET_COOKIE}",
                callback=self.parse_cookie,
            )
        else:
            yield scrapy.Request(f"{self.BASE_URL}/{self.P_URL_DIR_SEARCH}")

    def parse(self, response):
        for gazette in response.json()["data"]:
            gazette_date = gazette[self.P_KEY_DATE]
            gazette_date = datetime.strptime(gazette_date, "%Y-%m-%d %H:%M:%S").date()

            if self.P_CLIENT_ID == "":
                gazette_url_client_id = gazette[self.P_KEY_CLIENT_ID].zfill(10)
            else:
                gazette_url_client_id = self.P_CLIENT_ID.zfill(10)

            gazette_url_filename = gazette[self.P_KEY_URL_FILENAME]
            gazette_url_base_download = self.P_BASE_URL_DOWNLOAD.format(
                gazette_url_client_id
            )
            gazette_url = f"{gazette_url_base_download}/{gazette_url_filename}"
            gazette_edition_number = gazette[self.P_KEY_EDITION_NUMBER]
            if self.P_KEY_EXTRA_EDITION == "":
                gazette_is_extra_edition = False
            else:
                gazette_is_extra_edition = gazette[self.P_KEY_EXTRA_EDITION].lower()
                gazette_is_extra_edition = "extra" in gazette_is_extra_edition

            if self.start_date <= gazette_date <= self.end_date:
                yield Gazette(
                    date=gazette_date,
                    edition_number=gazette_edition_number,
                    file_urls=[gazette_url],
                    is_extra_edition=gazette_is_extra_edition,
                    territory_id=self.TERRITORY_ID,
                    scraped_at=datetime.utcnow(),
                    power=self.P_POWER,
                )

    def parse_cookie(self, response):
        yield scrapy.Request(f"{self.BASE_URL}/{self.P_URL_DIR_SEARCH}")
