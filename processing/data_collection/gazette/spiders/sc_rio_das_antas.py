from gazette.spiders.base import FecamGazetteSpider


class ScRioDasAntasSpider(FecamGazetteSpider):
    name = "sc_rio_das_antas"
    FECAM_QUERY = "cod_entidade:216"
    TERRITORY_ID = "4214409"
