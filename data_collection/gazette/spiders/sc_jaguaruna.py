from gazette.spiders.base import FecamGazetteSpider


class ScJaguarunaSpider(FecamGazetteSpider):
    name = "sc_jaguaruna"
    FECAM_QUERY = 'entidade:"Prefeitura municipal de Jaguaruna"'
    TERRITORY_ID = "4208807"
