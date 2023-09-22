from gazette.spiders.base.fecam import FecamGazetteSpider


class ScPescariaBravaSpider(FecamGazetteSpider):
    name = "sc_pescaria_brava"
    FECAM_QUERY = 'entidade:"Prefeitura Municipal de Pescaria Brava"'
    TERRITORY_ID = "4212650"
