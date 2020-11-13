from gazette.spiders.base.fecam import FecamGazetteSpider


class ScTresBarrasSpider(FecamGazetteSpider):
    name = "sc_tres_barras"
    FECAM_QUERY = "cod_entidade:274"
    TERRITORY_ID = "4218301"
