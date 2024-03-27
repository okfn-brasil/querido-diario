import csv
import time
from pathlib import Path

import scrapy
from unidecode import unidecode


class MapeadorSemantico(scrapy.Spider):
    custom_settings = {
        "RETRY_ENABLED": False,
        "AUTOTHROTTLE_ENABLED": True,
        "AUTOTHROTTLE_TARGET_CONCURRENCY": 100,
    }

    name = "mapeadorsemantico"
    protocols = ["http", "https"]
    territories = []

    def start_requests(self):
        self.read_csv("")
        self.add_column_key()  # add column to fill with search results

        for i in range(len(self.territories)):
            self.log(i)

            name, state_code = self.format_str(
                self.territories[i]["name"], self.territories[i]["state_code"]
            )
            for protocol_option in self.protocols:
                for name_option in self.city_name_generator(name):
                    for url_option in self.urls_pattern(
                        protocol_option, name_option, state_code
                    ):
                        yield scrapy.Request(
                            url_option, callback=self.parse, cb_kwargs=dict(index=i)
                        )

        self.save_csv(f"[{self.pattern_name()}] dados_mapeamento")

    def parse(self, response, index):
        if self.validation(response):
            if response.url not in self.territories[index][self.pattern_name()]:
                self.territories[index][self.pattern_name()].append(response.url)

            self.territories[index][self.current_status()].append(
                self.is_current(response)
            )

        elif response.url not in self.territories[index][self.valid_urls()]:
            self.territories[index][self.valid_urls()].append(response.url)

    def city_name_generator(self, city_name):
        combination_list = []

        combination_list.append(self.remove_blankspaces(city_name))  # cityname
        # combination_list.append(self.blankspaces_to_underline(city_name))  # city_name
        # combination_list.append(self.blankspaces_to_hifen(city_name))  # city-name
        combination_list.append(self.name_abbreviation(city_name))  # cn
        combination_list += self.name_parts(city_name)  # city | name
        # combination_list += self.add_pm_to_names(combination_list) #pm + all

        return combination_list

    def add_column_key(self):
        patternname = self.pattern_name()
        currentstatus = self.current_status()
        validurls = self.valid_urls()

        for y in range(len(self.territories)):
            self.territories[y][patternname] = []
            self.territories[y][currentstatus] = []
            self.territories[y][validurls] = []

    def save_csv(self, file_name):
        file_path = (Path(__file__).parent / f"../../../{file_name}.csv").resolve()

        with open(file_path, "w", newline="") as csvfile:
            writer = csv.DictWriter(
                csvfile, fieldnames=list(self.territories[0].keys())
            )
            writer.writeheader()
            for i in range(len(self.territories)):
                writer.writerow(self.territories[i])
        csvfile.close()

    def read_csv(self, file_name):
        if (Path(__file__).parent / f"../../../{file_name}.csv").is_file():
            file_path = (Path(__file__).parent / f"../../../{file_name}.csv").resolve()
        else:
            file_path = (
                Path(__file__).parent / "../../resources/territories.csv"
            ).resolve()

        with open(file_path, encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.territories.append(row)
        csvfile.close()

    def log(self, i):
        if i % 10 == 0:
            print(
                f"[{i}/{len(self.territories)}] {time.strftime('%H:%M:%S', time.localtime())}"
            )
        if i % 500 == 0:
            print("[BACKUP PARCIAL] Salvando dados parciais...")
            self.save_csv(
                f"[PARCIAL][{self.pattern_name()}] dados_mapeamento-{i}-{len(self.territories)}"
            )

    # FORMATAÇÕES PARA DOMINIOS

    def format_str(self, name, state_code):
        name = unidecode(name).strip().lower().replace("-", " ").replace("'", "")
        state_code = unidecode(state_code).strip().lower()
        return name, state_code

    def remove_blankspaces(self, name):
        return name.replace(" ", "")

    def blankspaces_to_underline(self, name):
        return name.replace(" ", "_")

    def blankspaces_to_hifen(self, name):
        return name.replace(" ", "-")

    def name_parts(self, name):
        name = name.replace(" da ", " ").replace(" de ", " ").replace(" do ", " ")
        return name.split()

    def name_abbreviation(self, city_name):
        subnames = city_name.split()
        abbrev = ""
        for n in subnames:
            if n not in ["da", "de", "do"]:
                abbrev += n[0]
        return abbrev

    def add_pm_to_names(self, list_names):
        # pm: prefeitura municipal
        aux = []
        for name in list_names:
            aux.append(f"pm{name}")
        return aux
