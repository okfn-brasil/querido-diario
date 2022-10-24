import datetime as dt


from gazette.spiders.base.dioenet import BaseDioenetSpider


class ApPedraBrancadoAmapariSpider(BaseDioenetSpider):
    TERRITORY_ID = "1600154"
    name = "ap_pedra_branca_do_amapari"
    start_date = dt.date(2020, 3, 9)
    end_date = dt.date.today()
    allowed_domains = ["plenussistemas.dioenet.com.br"]
    BASE_URL = "https://plenussistemas.dioenet.com.br/list/pedra-branca-do-amapari"
