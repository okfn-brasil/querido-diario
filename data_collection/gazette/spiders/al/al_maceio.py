from datetime import date

from gazette.spiders.base.sigpub import SigpubGazetteSpider


class AlMaceioSpider(SigpubGazetteSpider):
    name = "al_maceio"
    TERRITORY_ID = "2704302"
    CALENDAR_URL = "https://www.diariomunicipal.com.br/maceio"
    start_date = date(2018, 8, 9)
