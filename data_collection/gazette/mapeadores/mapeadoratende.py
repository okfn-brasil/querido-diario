from gazette.mapeadores.base.mapeadorsemantico import MapeadorSemantico


class MapeadorAtende(MapeadorSemantico):
    name = "mapeadoratende"

    # No mapeamento completo, todos os links http foram redirecionados para https.
    protocols = ["https"]

    def pattern_name(self):
        return "ATENDE"

    def valid_urls(self):
        return "vATENDE"

    def current_status(self):
        return "ATENDE_status"

    def urls_pattern(self, protocol, city, state_code):
        # casos conhecidos
        # https://campomourao.atende.net/?pg=diariooficial
        # https://gravatai.atende.net/diariooficial/edicao
        # https://camaqua.atende.net/cidadao/pagina/diario-oficial

        return [
            # f"{protocol}://{city}.atende.net",
            f"{protocol}://{city}.atende.net/?pg=diariooficial",
            f"{protocol}://{city}.atende.net/diariooficial",
            f"{protocol}://{city}.atende.net/cidadao/pagina/diario-oficial",
        ]

    def validation(self, response):
        if "atende.net" in response.text:
            if (
                "Diário Oficial" in response.text
                or "Órgão Oficial Eletrônico" in response.text
            ):
                if (
                    "Diário Oficial não está disponível para esta entidade"
                    not in response.text
                    and "Página indisponível no momento" not in response.text
                    and "Nenhum Resultado Encontrado" not in response.text
                ):
                    return True
        return False

    def is_current(self, response):
        raw = response.xpath('//*[@class="tituloAno"]/text()').get()

        if "2024" in raw:
            return "atual"
        else:
            return "verificar"
