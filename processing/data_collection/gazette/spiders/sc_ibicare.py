from gazette.spiders.base import FecamGazetteSpider


class ScIbicareSpider(FecamGazetteSpider):
    name = "sc_ibicare"
    FECAM_QUERY = "cod_entidade:111"
    TERRITORY_ID = "4206801"
