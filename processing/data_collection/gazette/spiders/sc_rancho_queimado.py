from gazette.spiders.base import FecamGazetteSpider


class ScRanchoQueimadoSpider(FecamGazetteSpider):
    name = "sc_rancho_queimado"
    FECAM_QUERY = 'cod_entidade:215'
    TERRITORY_ID = "4214300"