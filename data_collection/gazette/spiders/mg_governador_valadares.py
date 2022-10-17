from datetime import date

from gazette.spiders.base.ajaxpro import AjaxProSpider


class MgGovernadorValadares(AjaxProSpider):
    TERRITORY_ID = "3127701"
    name = "mg_governador_valadares"
    start_url = "https://www.valadares.mg.gov.br/diario-eletronico"
    base_file_url = (
        "https://www.valadares.mg.gov.br/abrir_arquivo.aspx?cdLocal=12&arquivo={}{}"
    )
    power_codes = {1: "executive"}
    start_date = date(2014, 4, 1)
