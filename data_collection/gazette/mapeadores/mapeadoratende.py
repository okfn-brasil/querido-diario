import scrapy

from gazette.mapeadores.base.mapeador import Mapeador


class MapeadorAtende(Mapeador):
    name = "mapeadoratende"

    # No mapeamento completo, todos os links http foram redirecionados para https.
    protocols = ["https"]

    # A list with States to be mapped. If empty, defaults to map All.
    # states_to_map = ['mg', 'pr', 'rs', 'sc', 'sp']

    def column(self):
        return "ATENDE"

    def backup_column(self):
        return "VALID_ATENDE"

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

    def start_requests(self):
        # self.logger.debug(f"STATES_MAP: {repr(self.states_to_map)} {len(self.states_to_map)}")
        self.read_csv("dados_mapeamento")
        self.add_column_key()  # add column to fill with search results

        for i in range(len(self.territories)):
            # Raise TypeError: Mapeador.log() got an unexpected keyword argument 'level'.
            # Should be renamed to print_status().
            self.log(i)
            # self.print_status(i)

            name, state_code = self.format_str(
                self.territories[i]["name"], self.territories[i]["state_code"]
            )
            # if len(self.states_to_map) > 0 and state_code not in self.states_to_map:
            #     continue
            for protocol_option in self.protocols:
                for name_option in self.city_name_generator(name):
                    for url_option in self.urls_pattern(
                        protocol_option, name_option, state_code
                    ):
                        yield scrapy.Request(
                            url_option, callback=self.parse, cb_kwargs=dict(index=i)
                        )

        self.save_csv("dados_mapeamento")

    def parse(self, response, index):
        # Get information regarding City and State.
        gov_br_city_state = response.xpath(
            '//a[contains(@href, "mailto:")][1]/@href'
        ).re(r"@(\w+)\.(\w+)\.gov\.br")
        address_city_state = response.css("div.mapa-texto span.linha::text").re(
            r"\w.+- ?([\w\s]+)/(\w+)"
        )
        # Get information regarding 'diario' links.
        links_diario_oficial = response.xpath(
            '//a[contains(@href, "diario")][1]/@href'
        ).getall()

        if self.validation(response):
            if response.url not in self.territories[index][self.column()]:
                self.territories[index][self.column()].append(response.url)
            if (
                len(gov_br_city_state) > 0
                and gov_br_city_state not in self.territories[index][self.column()]
            ):
                self.territories[index][self.column()].append(gov_br_city_state)
            if (
                len(address_city_state) > 0
                and address_city_state not in self.territories[index][self.column()]
            ):
                self.territories[index][self.column()].append(address_city_state)
            if (
                len(links_diario_oficial) > 0
                and links_diario_oficial not in self.territories[index][self.column()]
            ):
                self.territories[index][self.column()].append(links_diario_oficial)
        elif response.url not in self.territories[index][self.backup_column()]:
            self.territories[index][self.backup_column()].append(response.url)
            if (
                len(gov_br_city_state) > 0
                and gov_br_city_state
                not in self.territories[index][self.backup_column()]
            ):
                self.territories[index][self.backup_column()].append(gov_br_city_state)
            if (
                len(address_city_state) > 0
                and address_city_state
                not in self.territories[index][self.backup_column()]
            ):
                self.territories[index][self.backup_column()].append(address_city_state)
            if (
                len(links_diario_oficial) > 0
                and links_diario_oficial
                not in self.territories[index][self.backup_column()]
            ):
                self.territories[index][self.backup_column()].append(
                    links_diario_oficial
                )

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
                    and "Diário Oficial dos Municípios" not in response.text
                ):
                    return True
        return False
