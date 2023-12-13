import datetime

from gazette.spiders.base.sigpub import SigpubGazetteSpider


class AlAssociacaoMunicipiosSpider(SigpubGazetteSpider):
    name = "al_associacao_municipios"
    TERRITORY_ID = "2700000"
    CALENDAR_URL = "https://www.diariomunicipal.com.br/ama/"
    start_date = datetime.date(2014, 4, 10)
