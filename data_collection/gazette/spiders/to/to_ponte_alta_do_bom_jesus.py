import datetime
import re

from gazette.spiders.base.deto import BaseDetoSpider


class ToPonteAltaDoBomJesus(BaseDetoSpider):
    TERRITORY_ID = "1717800"
    name = "to_ponte_alta_do_bom_jesus"
    allowed_domains = ["pontealtadobomjesus.to.gov.br"]
    start_date = datetime.date(2020, 1, 6)
    BASE_URL = "https://pontealtadobomjesus.to.gov.br/transparencia"

    def extract_total_items_count(self, response):
        table_footer = response.xpath(
            "(//table[contains(@class, 'scGridToolbar')]//span)[last()]/text()"
        ).get()
        items_counter_search = re.search(r"(\d+?)\]$", table_footer)

        if items_counter_search:
            total_items_count = int(items_counter_search.group(1))
            return total_items_count

    def extract_modal_params(self, line_html):
        modal_param_search = re.search(
            r"(@SC_par@\d+?@SC_par@diarioeletronico_grid_cliente@SC_par@.+?)'",
            line_html,
        )
        if modal_param_search:
            return modal_param_search.group(1)
