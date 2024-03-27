import scrapy

from gazette.mapeadores.base.mapeadorsemantico import MapeadorSemantico


class MapeadorDosp(MapeadorSemantico):
    name = "mapeadordosp"

    custom_settings = {
        "CONCURRENT_REQUESTS_PER_DOMAIN": 40,
        "RETRY_ENABLED": False,
    }

    def pattern_name(self):
        return "DOSP"

    def valid_urls(self):
        return "vDOSP"

    def current_status(self):
        return "DOSP_status"

    def urls_pattern(self, protocol, city, state_code):
        # casos conhecidos
        # https://imprensaoficialmunicipal.com.br/adolfo
        # https://imprensaoficialmunicipal.com.br/guaracai

        return [f"{protocol}://www.imprensaoficialmunicipal.com.br/{city}"]

    def validation(self, response):
        if "dosp.com.br" in response.text:
            if "FILTRO POR DATA" in response.text:
                return True
        return False

    def is_current(self, response, index):
        if 'data": "2024-' in response.text:
            iscurrent = "atual"
        elif 'data": "20' in response.text or 'data": "19' in response.text:
            iscurrent = "descontinuado"
        else:
            iscurrent = "vazio"

        self.territories[index][self.current_status()].append(iscurrent)

    def parse(self, response, index):
        if self.validation(response):
            if response.url not in self.territories[index][self.pattern_name()]:
                self.territories[index][self.pattern_name()].append(response.url)

            string = "https://dosp.com.br/api/index.php/'+urlapi+'.js/"
            i = response.text.find("https://dosp.com.br/api/index.php/'+urlapi+'.js/")
            shift = i + len(string)

            rawid = response.text[shift : shift + 10]

            id = ""
            for char in rawid:
                if char.isdigit():
                    id += char

            yield scrapy.Request(
                f"https://dosp.com.br/api/index.php/dioe.js/{id}/",
                callback=self.is_current,
                cb_kwargs=dict(index=index),
            )

        elif response.url not in self.territories[index][self.valid_urls()]:
            self.territories[index][self.valid_urls()].append(response.url)
