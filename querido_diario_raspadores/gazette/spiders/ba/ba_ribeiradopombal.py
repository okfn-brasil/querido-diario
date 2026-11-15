from datetime import date

from gazette.spiders.base.diof import BaseDiofSpider


class BaRibeiraDoPombalSpider(BaseDiofSpider):
    TERRITORY_ID = "2926608"
    name = "ba_ribeiradopombal"
    website = "https://sai.io.org.br/ba/ribeiradopombal/Site/DiarioOficial"
    start_date = date(2007, 9, 18)
    power = "executive"
