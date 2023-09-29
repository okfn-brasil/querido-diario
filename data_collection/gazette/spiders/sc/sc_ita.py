from gazette.spiders.base.fecam import FecamGazetteSpider


class ScItaSpider(FecamGazetteSpider):
    name = "sc_ita"
    FECAM_QUERY = 'entidade:"Prefeitura Municipal de Itá"'
    TERRITORY_ID = "4208005"
