from gazette.spiders.base.fecam import FecamGazetteSpider


class ScCerroNegroSpider(FecamGazetteSpider):
    name = "sc_cerro_negro"
    FECAM_QUERY = "cod_entidade:69"
    TERRITORY_ID = "4204178"
