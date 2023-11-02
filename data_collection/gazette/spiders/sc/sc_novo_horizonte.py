from gazette.spiders.base.fecam import FecamGazetteSpider


class ScNovoHorizonteSpider(FecamGazetteSpider):
    name = "sc_novo_horizonte"
    FECAM_QUERY = "cod_entidade:178"
    TERRITORY_ID = "4211652"
