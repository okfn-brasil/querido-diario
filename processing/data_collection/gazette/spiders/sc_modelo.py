from gazette.spiders.base import FecamGazetteSpider


class ScModeloSpider(FecamGazetteSpider):
    name = "sc_modelo"
    FECAM_QUERY = 'cod_entidade:167'
    TERRITORY_ID = "4210902"