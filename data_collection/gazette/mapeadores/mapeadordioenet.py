from gazette.mapeadores.base.mapeador import Mapeador


class MapeadorDioenet(Mapeador):
    name = "mapeadordioenet"

    def pattern_name(self):
        return "DIOENET"

    def valid_urls(self):
        return "vDIOENET"

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
