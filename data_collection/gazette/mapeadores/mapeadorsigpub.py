import csv
import re
from pathlib import Path

import scrapy
from unidecode import unidecode


class MapeadorSigpub(scrapy.Spider):
    custom_settings = {"CONCURRENT_REQUESTS": 1}

    name = "mapeadorsigpub"
    territories = []

    associacoes = {
        "aam": "AM",
        "ama": "AL",
        "bahia": "BA",
        "amurc": "BA",
        "aprece": "CE",
        "agm": "GO",
        "fgm": "GO",
        "amm-mg": "MG",
        "amm-mt": "MT",
        "ms": "MS",
        "famep": "PA",
        "famup": "PB",
        "amp": "PR",
        "amupe": "PE",
        "appm": "PI",
        "aemerj": "RJ",
        "femurn": "RN",
        "amr": "RR",
        "arom": "RO",
        "famurs": "RS",
        "sergipe": "SE",
        "apm": "SP"
        # monte alto, sp
        # macatuba
    }

    def start_requests(self):
        self.read_csv()
        self.add_column_key()

        for association in self.associacoes.keys():
            yield scrapy.Request(
                self.urls_pattern(association),
                cb_kwargs=dict(assoc=association),
            )

        self.save_csv("[SIGPUB] dados_mapeamento_parcial")

    def parse(self, response, assoc):
        texto = unidecode(response.text.lower())
        lista = texto.replace("d&#039;", "d'").replace("´", "'").split("\n")

        municipios = []
        for item in lista:
            if "prefeitura" in item:
                municipios += re.findall(
                    r">prefeitura\s*municipal\s*de\s*([-\w\s']*)</option>", item
                )
                municipios += re.findall(
                    r">prefeitura\s*de\s*([-\w\s']*)</option>", item
                )
            if "municipio" in item:
                municipios += re.findall(
                    r">municipio\s*de\s*([-\w\s']*)</option>", item
                )

        for i in range(len(municipios)):
            municipios[i] = municipios[i].replace("d' ", "d'").strip()
            municipios += self.fix(municipios[i])

        self.searches(self.associacoes[assoc], municipios, assoc)

    def searches(self, state_code, cities_list, assoc):
        for j in range(len(self.territories)):
            if state_code in self.territories[j]["state_code"]:
                v1 = unidecode(self.territories[j]["name"].lower())
                v2 = v1.replace("d'", "do ")
                if v1 in cities_list or v2 in cities_list:
                    self.territories[j][self.pattern_name()].append(assoc)

    def pattern_name(self):
        return "SIGPUB"

    def urls_pattern(self, association):
        return f"https://www.diariomunicipal.com.br/{association}/pesquisar/"

    def save_csv(self, file_name):
        file_path = (Path(__file__).parent / f"../../{file_name}.csv").resolve()

        with open(file_path, "w", newline="") as csvfile:
            writer = csv.DictWriter(
                csvfile, fieldnames=list(self.territories[0].keys())
            )
            writer.writeheader()
            for i in range(len(self.territories)):
                writer.writerow(self.territories[i])
        csvfile.close()

    def add_column_key(self):
        column = self.pattern_name()
        for y in range(len(self.territories)):
            self.territories[y][column] = []

    def read_csv(self):
        file_path = (Path(__file__).parent / "../resources/territories.csv").resolve()

        with open(file_path, encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.territories.append(row)
        csvfile.close()

    def fix(self, item):
        if "major izidoro" == item:
            item = "major isidoro"
        elif item in [
            "abadia",
            "campestre",
            "corumba",
            "divinopolis",
            "guarani",
            "ipiranga",
            "montes claros",
            "palmeiras",
            "petrolina",
            "bom jesus",
            "teresina",
        ]:
            item = item + " de goias"
        elif "sao joao da alianca" == item:
            item = "sao joao d'alianca"
        elif item in ["lagoa formosa-mg", "pedra do anta-mg", "silvianopolis-mg"]:
            item = item[:-3]
        elif item == "barao do monte alto":
            item = "barao de monte alto"
        elif item == "dona euzebia":
            item = "dona eusebia"
        elif item == "santo antonio de leverger":
            item = "santo antonio do leverger"
        elif item == "rio verde de mt":
            item = "rio verde de mato grosso"
        elif item == "arez":
            item = "ares"
        elif item == "assu":
            item = "acu"
        elif item == "boa saude":
            item = "januario cicco (boa saude)"
        elif item == "cerro-cora":
            item = "cerro cora"
        elif item == "olho d'agua do borges":
            item = "olho-d'agua do borges"
        elif item == "santa luzia do itanhi":
            item = "santa luzia do itanhy"
        elif item == "santana do livramento":
            item = "sant'ana do livramento"
        elif item in ["sapucai mirim", "sem peixe", "venha ver"]:
            item = item.replace(" ", "-")
        return [item]
