from gazette.spiders.base.doem import DoemGazetteSpider


class SPSaoCarlosSpider(DoemGazetteSpider):
    TERRITORY_ID = ""
    
    state_city_url_part = "sp/sao carlos"
