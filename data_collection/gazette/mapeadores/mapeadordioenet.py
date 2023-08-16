from gazette.mapeadores.base.mapeadorsemantico import MapeadorSemantico


class MapeadorDioenet(MapeadorSemantico):
    name = "mapeadordioenet"

    custom_settings = {
        "CONCURRENT_REQUESTS_PER_DOMAIN": 25,
        "RETRY_ENABLED": False,
    }

    def pattern_name(self):
        return "DIOENET"

    def valid_urls(self):
        return "vDIOENET"

    def current_status(self):
        return "DIOENET_status"

    def urls_pattern(self, protocol, city, state_code):
        # casos conhecidos
        # https://plenussistemas.dioenet.com.br/list/santo-antonio-da-alegria
        # https://plenussistemas.dioenet.com.br/list/santa-rosa-de-viterbo

        return [f"{protocol}://plenussistemas.dioenet.com.br/list/{city}"]

    def validation(self, response):
        if (
            "https://plenussistemas.dioenet.com.br/public/uploads/cidades/"
            in response.text
        ):
            if "Sem registros encontrados" not in response.text:
                return True
        return False

    def is_current(self, response):
        raw = response.xpath('//*[@class="col-one"]/h3/text()').get()

        if raw is None:
            return "verificar"
        elif "2024" in raw:
            return "atual"
        elif "/20" in raw or "/19" in raw:
            return "descontinuado"
        else:
            return "vazio"
