from gazette.spiders.base.fecam import FecamGazetteSpider


class ScTurvoSpider(FecamGazetteSpider):
    name = "sc_turvo"
    FECAM_QUERY = "cod_entidade:281"
    TERRITORY_ID = "4218806"
