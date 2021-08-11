from gazette.spiders.base.fecam import FecamGazetteSpider


class ScSaltoVelosoSpider(FecamGazetteSpider):
    name = "sc_salto_veloso"
    FECAM_QUERY = "cod_entidade:229"
    TERRITORY_ID = "4215406"
