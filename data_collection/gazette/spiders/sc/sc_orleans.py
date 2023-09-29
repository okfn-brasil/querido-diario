from gazette.spiders.base.fecam import FecamGazetteSpider


class ScOrleansSpider(FecamGazetteSpider):
    name = "sc_orleans"
    FECAM_QUERY = "cod_entidade:179"
    TERRITORY_ID = "4211702"
