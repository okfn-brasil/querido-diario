from gazette.spiders.base.fecam import FecamGazetteSpider


class ScFreiRogerioSpider(FecamGazetteSpider):
    name = "sc_frei_rogerio"
    FECAM_QUERY = "cod_entidade:96"
    TERRITORY_ID = "4205555"
