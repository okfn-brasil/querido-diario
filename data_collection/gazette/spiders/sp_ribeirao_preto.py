import re
from datetime import date, datetime

from dateutil.rrule import DAILY, rrule
from scrapy import FormRequest, Request, Selector

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider

SINGLE_FILE_GAZETTE_TEXTUAL_DATA = re.compile(
    r"Diário Oficial N."
    r"[A-Z\d]+(?#anniversary year of the gazette)"
    r"\D+"
    r"(\d+)(?#edition_number)"
    r"\D+"
    r"(\d{2}/\d{2}/\d{4})(?#date)"
)
MULTIPLE_FILES_GAZETTE_TEXTUAL_DATA = re.compile(r"Diário Oficial - .*")


class SpRibeiraoPretoSpider(BaseGazetteSpider):
    name = "sp_ribeirao_preto"
    TERRITORY_ID = "3543402"
    start_date = date(2007, 1, 2)  # edition_number 7679

    allowed_domains = ["www.ribeiraopreto.sp.gov.br"]
    BASE_URL = "https://www.ribeiraopreto.sp.gov.br/diario-oficial/pesquisa-data"

    FORM_XPATH = "//form[@id='formdiario']"

    # Given that after reaching a certain rate limit, servers stop responding,
    # we have adjusted some values to avoid this situation.
    custom_settings = {
        "DOWNLOAD_DELAY": 0.25,  # 250 ms
        "RANDOMIZE_DOWNLOAD_DELAY": True,
    }

    def __init__(self, *args, **kwargs):
        super(SpRibeiraoPretoSpider, self).__init__(*args, **kwargs)
        self.dates_to_retry = []

    def start_requests(self):
        for date_ in rrule(freq=DAILY, dtstart=self.start_date, until=self.end_date):
            gazette_date = date_.date()
            yield Request(
                url=self.BASE_URL,
                callback=self.before_choosing_gazette_date,
                cb_kwargs={"gazette_date": gazette_date},
                # We are isolating cookiejar per name-year-month-day combination
                # to avoid interference between concurrent requests
                meta={"cookiejar": f"{self.name}_{gazette_date.isoformat()}"},
                dont_filter=True,
            )

        while self.dates_to_retry:
            current_retries = self.dates_to_retry.copy()
            self.dates_to_retry.clear()
            for gazette_date in current_retries:
                self.logger.info(f"Retrying {gazette_date.isoformat()}...")
                yield Request(
                    url=self.BASE_URL,
                    callback=self.before_choosing_gazette_date,
                    cb_kwargs={"gazette_date": gazette_date},
                    # We are isolating cookiejar per name-year-month-day combination
                    # to avoid interference between concurrent requests
                    meta={"cookiejar": f"{self.name}_{gazette_date.isoformat()}"},
                    dont_filter=True,
                )

    def before_choosing_gazette_date(self, response, gazette_date):
        form_node = response.xpath(self.FORM_XPATH)

        form_data = {
            "javax.faces.partial.ajax": "true",
            "javax.faces.partial.render": "@all",
            "javax.faces.behavior.event": "dateSelect",
            "javax.faces.partial.event": "dateSelect",
        }

        dynamic_field_name = ""
        hidden_input_nodes = form_node.xpath("//input[@type='hidden']")
        for hidden_input_data in hidden_input_nodes:
            key = hidden_input_data.attrib["name"]
            if value := hidden_input_data.attrib.get("value"):
                form_data[key] = value
            else:
                dynamic_field_name = key

        if not dynamic_field_name:
            self.logger.warning(
                f"We could not extract form data while trying to retrieve gazette data"
                f" for {gazette_date.isoformat()}"
            )
            return

        value_based_on_dynamic_field_name = dynamic_field_name.rstrip("_input")

        form_data |= {
            "javax.faces.source": value_based_on_dynamic_field_name,
            "javax.faces.partial.execute": value_based_on_dynamic_field_name,
            dynamic_field_name: gazette_date.strftime("%d/%m/%Y"),
        }

        yield FormRequest.from_response(
            response,
            callback=self.parse_gazette_date_page,
            cb_kwargs={"gazette_date": gazette_date},
            formname="formdiario",
            formxpath=self.FORM_XPATH,
            formdata=form_data,
            dont_click=True,
            dont_filter=True,
            method="POST",
            meta={"cookiejar": f"{self.name}_{gazette_date.isoformat()}"},
        )

    def parse_gazette_date_page(self, response, gazette_date):
        """
        The response is a xml file in which HTML data as text in one of its nodes.

        This method extracts the actual data from the response and retrieves gazette data.
        """

        viewstate_data_from_xml = response.xpath(
            "//update[contains(@id, 'javax.faces.ViewState')]/text()"
        ).get()

        html_from_xml = response.xpath(
            "//update[@id='javax.faces.ViewRoot']/text()"
        ).get()
        try:
            html_node = Selector(text=html_from_xml)
        except ValueError:
            self.logger.info(
                f"Unable to extract HTML data from XML for {gazette_date.isoformat()}."
                " Adding that date to retry later."
            )
            self.dates_to_retry.append(gazette_date)
            return
        results_node = html_node.xpath("//span[@id='formdiario:panelresultado']")
        if not results_node:
            return

        file_requests_dict = {}
        edition_number = ""
        edition_number_from_text = ""
        date_from_text = None

        for button_node in results_node.xpath(".//button[@title='Diario PDF']"):
            button_text = (
                button_node.xpath(".//span[contains(@class, 'ui-button-text')]/text()")
                .get()
                .strip()
            )

            if MULTIPLE_FILES_GAZETTE_TEXTUAL_DATA.search(button_text):
                pass  # No metadata to extract from the match
            elif match_ := SINGLE_FILE_GAZETTE_TEXTUAL_DATA.search(button_text):
                edition_number_from_text = match_.group(1)
                date_from_text = datetime.strptime(match_.group(2), "%d/%m/%Y").date()
            else:
                self.logger.warning(
                    f"Unable to extract metadata from '{button_text}'"
                    f" for {gazette_date.isoformat()}"
                )
                continue

            if edition_number:
                if edition_number != edition_number_from_text:
                    self.logger.info(
                        f"Results for {gazette_date.isoformat()} contain"
                        f" different edition_number: '{edition_number}'"
                        f" and '{edition_number_from_text}'"
                    )
            else:
                edition_number = edition_number_from_text

            if date_from_text and gazette_date != date_from_text:
                self.logger.warning(
                    f"Results for {gazette_date.isoformat()} contains data for"
                    f" {date_from_text}. Skipping..."
                )
                continue

            form_data = {
                "formdiario": "formdiario",
                "javax.faces.ViewState": viewstate_data_from_xml,
                button_node.attrib["id"]: "",
            }

            relative_url = button_node.xpath("//ancestor::form/@action").get().strip()
            url = response.urljoin(relative_url)

            file_requests_dict[button_text] = FormRequest(
                url=url,
                formdata=form_data,
                dont_filter=True,
                method="POST",
                meta={"cookiejar": f"{self.name}_{gazette_date.isoformat()}"},
            )

        file_requests = [file_requests_dict[key] for key in sorted(file_requests_dict)]

        yield Gazette(
            date=gazette_date,
            file_requests=file_requests,
            edition_number=edition_number,
            is_extra_edition=False,
            power="executive",
        )
