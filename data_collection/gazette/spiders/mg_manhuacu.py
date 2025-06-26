from datetime import date

from gazette.spiders.base.ajaxpro import AjaxProSpider


class MgManhuacuSpider(AjaxProSpider):
    TERRITORY_ID = "3139409"
    name = "mg_manhuacu"
    start_url = "https://www.manhuacu.mg.gov.br/diario-eletronico"
    base_file_url = (
        "https://www.manhuacu.mg.gov.br/abrir_arquivo.aspx?cdLocal=12&arquivo={}{}"
    )
    power_codes = {1: "executive"}
    start_date = date(2015, 1, 8)
