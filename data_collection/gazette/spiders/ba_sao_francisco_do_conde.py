from datetime import date

from gazette.spiders.base.imprensa_oficial import ImprensaOficialSpider


class BaSaoFranciscoDoCondeSpider(ImprensaOficialSpider):

    name = "ba_sao_francisco_do_conde"
    allowed_domains = ["pmsaofranciscodocondeba.imprensaoficial.org"]
    start_date = date(2019, 3, 1)
    end_date = date.today()
    url_base = "http://pmsaofranciscodocondeba.imprensaoficial.org/{}"
    TERRITORY_ID = "2929206"
