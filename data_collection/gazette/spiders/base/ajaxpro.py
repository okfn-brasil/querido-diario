import ast
import json
import re
from datetime import datetime
from typing import Dict, List
from urllib.parse import urljoin

from scrapy import Request

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class AjaxProSpider(BaseGazetteSpider):
    """
    Base spider for all cities that uses the AjaxPro framework.
    To implement this base class, the following attributes
    are required to be defined by child classes:

    Attributes:
        TERRITORY_ID (str): Same as `BaseGazetteSpider` requires.
        start_url (str): Url of the gazette from the given city.
        base_fire_url (str): Base url to open the file, with `{}` placeholders
         for the ID and type of the file, using :meth:`str.format` formatting.
            Example: https://www.city.gov.br/abrir_arquivo.aspx?cdLocal=12&arquivo={}{}"
        power_codes (dict): A dict with ID's of a given power as `key` and the
            name of the power as `value`.
            Example: {1: "executive", "2": "legislative"}
    """

    # Optional attribute
    items_per_page: str = "100"

    # Required attributes
    TERRITORY_ID: str = None
    start_url: str = None
    base_file_url: str = None
    power_codes: Dict[int, str] = None

    # Not exposed attributes that should not be overriden
    _current_page: int = 0
    _current_power: int = None
    _crawled_power_stack: List[int] = []

    def start_requests(self) -> None:
        yield Request(self.start_url, dont_filter=True, callback=self.ajaxpro_request)

    def ajaxpro_request(self, response) -> None:
        """
        Custom POST request to the AjaxPro Method.

        Uses the first response to get the correct endpoint.
        Within the request, creates a custom body described
        in :meth:`make_body`.
        """

        request_path = urljoin(self.start_url, self.get_path_to_request_items(response))

        yield Request(
            request_path,
            method="POST",
            headers={
                "X-AjaxPro-Method": "GetDiario",
            },
            body=self.make_body(),
        )

    def get_path_to_request_items(self, response) -> str:
        """Get the endpoint that implements the GetDiario script"""

        scripts = response.xpath("//script//@src").getall()
        endpoint = next(path for path in scripts if "diel_diel_lis" in path)
        return endpoint

    def make_body(self) -> str:
        """
        Create a custom body needed to the GetDiario script.

        To create the body, this methods updates :attribute:`_current_power`.
        This is needed in order to dinamically request all
        available power mappeds in :attribute:`_power_codes`.
        Also, :attribute:start_date and :attribute:end_date needs to be
        parsed in a custom date format accepted by the endpoint script.
        This is done by :meth:`date_to_system_date`.
        """

        self.update_current_power()
        return json.dumps(
            {
                "Page": self._current_page,
                "cdCaderno": self._current_power,
                "Size": self.items_per_page,
                "dtDiario_menor": self.date_to_system_date(self.start_date),
                "dtDiario_maior": self.date_to_system_date(self.end_date),
                "dsPalavraChave": "",
                "nuEdicao": -1,
            }
        )

    def update_current_power(self) -> None:
        """
        Updates :attribute:`_current_power`.

        This attribute is used to define which power to request.
        """

        if self._current_page != 0:
            return

        uncrawled_codes = list(
            set(self.power_codes).difference(self._crawled_power_stack)
        )

        if uncrawled_codes:
            self._current_power = uncrawled_codes[0]
        return

    def is_body_empty(self, response) -> bool:
        """Validate if the response body is empty."""

        return response.body == "null;/*".encode()

    @staticmethod
    def date_to_system_date(timestamp: datetime.date) -> Dict[str, any]:
        """Parse a `datetime.date` to a custom date format."""

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

    def system_date_to_date(self, system_date: tuple) -> datetime.date:
        """
        Parse the response `Tuple` containing the custom system date.

        System the system date starts at month 0, it is needed to
        add 1 to the month, as the `datetime` object starts at month 1.
        """

        date = (system_date[0], system_date[1] + 1, system_date[2])
        return datetime.date(datetime(*date))

    def parse(self, response) -> None:
        """
        Parse each gazette metadata returned from :meth:`parse_ajaxpro_response`
        and yields its `Gazette` object.

        It implements the control flow to iterate over each available page for
        each power mapped in :attribute:`power_codes`, yielding a new
        request if there is a mapped power not yet crawled or if the response
        for the current page isn't an empty body.
        """

        if self.is_body_empty(response) and len(self._crawled_power_stack) == len(
            self.power_codes
        ):
            return

        elif self.is_body_empty(response):
            self._current_page = 0
            self._crawled_power_stack.append(self._current_power)
            yield Request(
                self.start_url, dont_filter=True, callback=self.ajaxpro_request
            )

        else:
            for gazette in self.parse_ajaxpro_response(response):
                url = self.base_file_url.format(
                    gazette["NMARQUIVO"], gazette["NMEXTENSAOARQUIVO"]
                )
                print(gazette)
                yield Gazette(
                    date=self.system_date_to_date(gazette["DTVISUALIZACAO"]),
                    file_urls=[url],
                    is_extra_edition=self.is_extra_edition(),
                    territory_id=self.TERRITORY_ID,
                    power=self.power_codes[self._current_power],
                    scraped_at=datetime.utcnow(),
                )

            self._current_page += 1
            yield Request(
                self.start_url, dont_filter=True, callback=self.ajaxpro_request
            )

    def parse_ajaxpro_response(self, response) -> List[dict]:
        """
        Parse the AjaxPro response body to `list` containing
        all gazette metadata formatted in to `dict` objects.
        """

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

    def is_extra_edition(self) -> bool:
        """Method to be overrided if possible to determine extra_edition."""
        return False
