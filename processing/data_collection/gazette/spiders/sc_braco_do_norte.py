from gazette.spiders.base import FecamGazetteSpider


class ScBracoDoNorteSpider(FecamGazetteSpider):
    name = "sc_braco_do_norte"
    FECAM_QUERY = 'entidade:"Prefeitura municipal de Braço do Norte"'
    TERRITORY_ID = "4202800"