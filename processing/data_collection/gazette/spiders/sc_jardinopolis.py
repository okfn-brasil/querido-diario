from gazette.spiders.base import FecamGazetteSpider


class ScJardinopolisSpider(FecamGazetteSpider):
    name = "sc_jardinopolis"
    FECAM_QUERY = "cod_entidade:139"
    TERRITORY_ID = "4208955"
