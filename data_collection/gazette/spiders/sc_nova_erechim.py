from gazette.spiders.base.fecam import FecamGazetteSpider


class ScNovaErechimSpider(FecamGazetteSpider):
    name = "sc_nova_erechim"
    FECAM_QUERY = "cod_entidade:174"
    TERRITORY_ID = "4211405"
