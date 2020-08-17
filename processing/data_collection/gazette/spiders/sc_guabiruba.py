from gazette.spiders.base import FecamGazetteSpider


class ScGuabirubaSpider(FecamGazetteSpider):
    name = "sc_guabiruba"
    FECAM_QUERY = 'entidade:"Prefeitura municipal de Guabiruba"'
    TERRITORY_ID = "4206306"
