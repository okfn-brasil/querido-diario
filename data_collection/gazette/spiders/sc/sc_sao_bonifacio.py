from gazette.spiders.base.fecam import FecamGazetteSpider


class ScSaoBonifacioSpider(FecamGazetteSpider):
    name = "sc_sao_bonifacio"
    FECAM_QUERY = "cod_entidade:241"
    TERRITORY_ID = "4215901"
