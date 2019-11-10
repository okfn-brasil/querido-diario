import re
from datetime import date, datetime

from dateparser import parse
from dateutil.relativedelta import relativedelta

from gazette.items import Gazette
from gazette.spiders.base import FecamGazetteSpider


class ScGasparSpider(FecamGazetteSpider):
    name = "sc_gaspar"
    FECAM_QUERY = 'entidade:"Prefeitura municipal de Gaspar"'
    TERRITORY_ID = "4205902"
