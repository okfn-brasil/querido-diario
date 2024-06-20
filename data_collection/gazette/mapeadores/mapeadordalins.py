from gazette.mapeadores.base.mapeadorsemantico import MapeadorSemantico


class MapeadorDalins(MapeadorSemantico):
    name = "mapeadordalins"

    def pattern_name(self):
        return "DALINS"

    def valid_urls(self):
        return "vDALINS"

    def current_status(self):
        return "DALINS_status"

    def urls_pattern(self, protocol, city, state_code):
        # casos conhecidos
        # https://cachoeirinha.to.gov.br/diariooficial
        # https://saobentodotocantins.to.gov.br/diariooficial

        return [f"{protocol}://{city}.{state_code}.gov.br/diariooficial"]

    def validation(self, response):
        if "datalins.com.br" in response.text:
            return True
        return False

    def is_current(self, response):
        raw = response.xpath('//*[@class="btndiariopg"]/div/div[2]/text()').get()

        if raw is None:
            return "verificar"
        elif "2024" in raw:
            return "atual"
        elif "/20" in raw or "/19" in raw:
            return "descontinuado"
        else:
            return "vazio"
