import datetime
import re

from gazette.spiders.base.deto import BaseDetoSpider


class ToNovoAlegre(BaseDetoSpider):
    TERRITORY_ID = "1715150"
    name = "to_novo_alegre"
    allowed_domains = ["novoalegre.to.gov.br"]
    start_date = datetime.date(2020, 2, 6)
    BASE_URL = "https://novoalegre.to.gov.br/transparencia"

    def extract_total_items_count(self, response):
        count_str = response.xpath("(//*[@class='sm_counter_total'])//text()").get()
        return int(count_str)

    def extract_modal_params(self, line_html):
        modal_param_search = re.search(
            r"@SC_par@diarioeletronico_grid_cliente@SC_par@(.+?)'", line_html
        )
        hash = modal_param_search.group(1)
        return f"@SC_par@1@SC_par@diarioeletronico_grid_cliente@SC_par@{hash}"
