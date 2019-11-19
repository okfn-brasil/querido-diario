from gazette.spiders.base import FecamGazetteSpider


class ScAngelinaSpider(FecamGazetteSpider):
    name = "sc_angelina"
    FECAM_QUERY = 'cod_entidade:15'
    TERRITORY_ID = "4200903"