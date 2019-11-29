from gazette.spiders.base import FecamGazetteSpider


class ScLuizAlvesSpider(FecamGazetteSpider):
    name = "sc_luiz_alves"
    FECAM_QUERY = "cod_entidade:154"
    TERRITORY_ID = "4210001"
