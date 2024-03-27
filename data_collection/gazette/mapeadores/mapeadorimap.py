import re

from unidecode import unidecode

from gazette.mapeadores.base.mapeadornumerico import MapeadorNumerico


class MapeadorImap(MapeadorNumerico):
    custom_settings = {"CONCURRENT_REQUESTS": 1, "DOWNLOAD_DELAY": 0.1}

    name = "mapeadorimap"

    def pattern_name(self):
        return "IMAP"

    def current_status(self):
        return "IMAP_status"

    def urls_pattern(self, i):
        # casos conhecidos
        # https://dom.imap.org.br/sitesMunicipios/imprensaOficial.cfm?varCodigo=461
        # https://dom.imap.org.br/sitesMunicipios/imprensaOficial.cfm?varCodigo=872
        # https://dom.imap.org.br/sitesMunicipios/imprensaOficial.cfm?varCodigo=10986

        return (
            f"https://dom.imap.org.br/sitesMunicipios/imprensaOficial.cfm?varCodigo={i}"
        )

    def num_max(self):
        return 12000

    def state(self):
        return ""

    def collect_metadata(self, response):
        if "Não foram encontrados registros para esta busca" in response.text:
            return None, None
        if "Câmara Municipal" in response.text:
            return None, None

        rawname = response.xpath('//*[@method="post"]/strong/text()').get()
        if rawname is None:
            return None, None

        rawname = unidecode(rawname).lower()
        nome = re.search("prefeitura\s*municipal\s*de\s*([-\w\s']*)", rawname)
        if nome is None:
            return None, None

        nome = nome.group(1)
        data = response.xpath('//*[@class="todo-task"]/strong/text()').get()
        if data is None:
            return None, None

        if "/2024" in data:
            iscurrent = "atual"
        elif "/20" in data or "/19" in data:
            iscurrent = "descontinuado"
        else:
            iscurrent = "vazio"

        return nome, iscurrent
