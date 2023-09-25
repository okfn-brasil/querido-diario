from gazette.spiders.base.fecam import FecamGazetteSpider


class ScAgronomicaSpider(FecamGazetteSpider):
    name = "sc_agronomica"
    FECAM_QUERY = "cod_entidade:7"
    TERRITORY_ID = "4200309"
