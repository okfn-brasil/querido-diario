from datetime import date

from gazette.spiders.base.eatos import BaseEatosSpider


class PrSerranopolisDoIguacuSpider(BaseEatosSpider):
    TERRITORY_ID = "4126355"
    name = "pr_serranopolis_do_iguacu"
    url_path = "serranopolis"
    start_date = date(2012, 1, 27)
