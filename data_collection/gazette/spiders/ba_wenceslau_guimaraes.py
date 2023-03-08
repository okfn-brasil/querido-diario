from datetime import date

from gazette.spiders.base.imprensa_oficial import ImprensaOficialSpider


class BaWenceslauGuimaraesSpider(ImprensaOficialSpider):
    name = "ba_wenceslau_guimaraes"
    allowed_domains = ["pmwenceslauguimaraesba.imprensaoficial.org"]
    start_date = date(2017, 1, 1)
    url_base = "http://pmwenceslauguimaraesba.imprensaoficial.org/{}"
    TERRITORY_ID = "2933505"
