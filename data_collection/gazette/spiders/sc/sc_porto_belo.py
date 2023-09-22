from gazette.spiders.base.fecam import FecamGazetteSpider


class ScPortoBeloSpider(FecamGazetteSpider):
    name = "sc_porto_belo"
    FECAM_QUERY = "cod_entidade:206"
    TERRITORY_ID = "4213500"
