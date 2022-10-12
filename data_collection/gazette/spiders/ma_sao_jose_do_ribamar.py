from datetime import date

from gazette.spiders.base.ajaxpro import AjaxProSpider


class MaSaoJoseDoRibamar(AjaxProSpider):
    TERRITORY_ID = "2111201"
    name = "ma_sao_jose_do_ribamar"
    start_url = "https://www.saojosederibamar.ma.gov.br/diario-eletronico"
    base_file_url = "https://www.saojosederibamar.ma.gov.br/abrir_arquivo.aspx?cdLocal=12&arquivo={}{}"
    power_codes = {1: "legislative", 3: "executive", 8: "executive_legislative"}
    start_date = date(2015, 12, 1)
