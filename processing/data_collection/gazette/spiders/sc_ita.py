from gazette.spiders.base import FecamGazetteSpider


class ScItaSpider(FecamGazetteSpider):
    name = "sc_ita"
    FECAM_QUERY = 'entidade:"Prefeitura Municipal de Itá"'
    TERRITORY_ID = "4208005"