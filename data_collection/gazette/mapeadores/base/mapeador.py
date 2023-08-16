import csv
import unicodedata

import pkg_resources
import scrapy


class Mapeador(scrapy.Spider):

    """
    Class base para Mepeadores (Em Processo)

    format_url : link base que sera usado para o mapeamento.
    @city sera substitudo pelo o nome do estado.
    @uf sera substitudo pela uf do estado

    Exemplo: https://transparencia.@city.@uf.gov.br/diario

    sep: Define o que sera colado entre os espaço do nome do estado

    preference_state_code : Define UF de pesquisa. Quando não declarada pesquisa todas as Ufs do Brasil. Aceita
    um valor ou lista de UFs. Por enquanto só maiscula.
    """

    name = "mapeador"
    custom_settings = {
        "CONCURRENT_REQUESTS": 100,
    }

    format_url = ""
    sep = "_"
    preference_state_code = None
    citys_confirmed = []
    citys = None

    def start_requests(self):
        self.create_csv()
        self.citys = self.link_forme()

        for city in self.citys[:10]:
            yield scrapy.Request(url=city["link"], callback=self.parse)

    def parse(self, response, **kwargs):
        good = next(item for item in self.citys if item["link"] == response.url)
        self.log(good)
        self.save_citys(good)
        self.log(response.url)
        self.log(f"Fui salvo: {good}")

    def get_estados(self):
        territories_file = pkg_resources.resource_filename(
            "gazette", "resources/territories.csv"
        )

        with open(territories_file, encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            territories = []
            for row in reader:
                if (
                    self.preference_state_code
                    and row["state_code"] in self.preference_state_code
                ):
                    territories.append(row)
                elif not self.preference_state_code:
                    territories.append(row)

            # for territorie in territories:
            #     self.log(territorie)
            return territories

    def link_forme(self):
        links = []
        citys = self.get_estados()
        for city in citys:
            city_name_clear = self.formatar_city_name(city["name"], sep=self.sep)
            link = self.format_url

            format_link_clear = {
                "@city": city_name_clear,
                "@uf": city["state_code"].lower(),
            }

            for place, replace_ in format_link_clear.items():
                link = link.replace(place, replace_)

            city["link"] = link
            links.append(city)

        return links

    def save_citys(self, city_save):
        with open(
            f"gazette/mapeadores/output/{self.name}.csv",
            "a",
            newline="",
            encoding="utf-8",
        ) as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(city_save.values())

    def create_csv(self):
        with open(
            f"gazette/mapeadores/output/{self.name}.csv",
            "w",
            newline="",
            encoding="utf-8",
        ) as csvfile:
            fieldnames = ["id", "name", "state_code", "state", "link"]
            writer = csv.writer(csvfile)
            writer.writerow(fieldnames)

    @staticmethod
    def formatar_city_name(name, sep="-"):
        x = name.strip().lower()
        x = unicodedata.normalize("NFD", x)
        x = x.encode("ascii", "ignore")
        x = x.decode("utf-8")
        x = x.replace(" ", sep)

        return x
