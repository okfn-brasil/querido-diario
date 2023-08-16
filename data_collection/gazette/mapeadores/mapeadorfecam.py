import re

from unidecode import unidecode

from gazette.mapeadores.base.mapeadornumerico import MapeadorNumerico


class MapeadorFECAM(MapeadorNumerico):
    name = "mapeadorfecam"

    def pattern_name(self):
        return "FECAM"

    def current_status(self):
        return "FECAM_status"

    def urls_pattern(self, i):
        return f"https://www.diariomunicipal.sc.gov.br/site/?q=cod_entidade:{i}"

    def num_max(self):
        return 300

    def state(self):
        return "SC"

    def collect_metadata(self, response):
        rawname = response.xpath('//*[@title="Página inicial"]/text()').get()
        rawname = unidecode(rawname).lower()

        nome = re.search("prefeitura\s*municipal\s*de\s*([-\w\s']*)", rawname).group(1)

        data = response.xpath('//*[@class="quiet"]').getall()[1]
        if "/2024" in data:
            iscurrent = "atual"
        elif "/20" in data or "/19" in data:
            iscurrent = "descontinuado"
        else:
            iscurrent = "vazio"

        return nome, iscurrent
