from gazette.spiders.base.fecam import FecamGazetteSpider


class ScIbiamSpider(FecamGazetteSpider):
    name = "sc_ibiam"
    FECAM_QUERY = "cod_entidade:110"
    TERRITORY_ID = "4206751"
