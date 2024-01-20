import datetime

from gazette.spiders.base.sjdbma import SjdbmaGazetteSpider


class MaSaoJoseDosBasiliosSpider(SjdbmaGazetteSpider):
    TERRITORY_ID = "2111250"
    name = "ma_sao_jose_dos_basilios_2023"
    start_date = datetime.date(2018, 2, 19)
    allowed_domains = ["diariooficial.saojosedosbasilios.ma.gov.br"]
    BASE_URL = "https://diariooficial.saojosedosbasilios.ma.gov.br/diariooficial"
