from gazette.spiders.base import FecamGazetteSpider


class ScRioDosCedrosSpider(FecamGazetteSpider):
    name = "sc_rio_dos_cedros"
    FECAM_QUERY = 'cod_entidade:220'
    TERRITORY_ID = "4214706"