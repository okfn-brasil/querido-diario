from gazette.spiders.base.fecam import FecamGazetteSpider


class ScBlumenauSpider(FecamGazetteSpider):
    name = "sc_blumenau"
    FECAM_QUERY = "cod_entidade:41"
    TERRITORY_ID = "4202404"
