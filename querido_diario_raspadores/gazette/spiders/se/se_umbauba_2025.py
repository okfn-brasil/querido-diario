from datetime import date

from gazette.spiders.base.municipioonline import BaseMunicipioOnlineSpider


class SeUmbaubaSpider(BaseMunicipioOnlineSpider):
    TERRITORY_ID = "2807600"
    name = "se_umbauba_2025"
    url_uf = "se"
    url_city = "umbauba"
    start_date = date(2025, 1, 2)
    end_date = date(2026, 3, 13)
