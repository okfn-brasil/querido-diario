import csv
import time
from pathlib import Path

import scrapy
from unidecode import unidecode


class MapeadorNumerico(scrapy.Spider):
    name = "mapeadornumerico"

    territories = []
    municipios = []

    def start_requests(self):
        self.read_csv()
        self.add_column_key()

        for i in range(self.num_max()):
            yield scrapy.Request(self.urls_pattern(i))

        time.sleep(60)
        print(self.municipios)
        print(len(self.municipios))
        self.save_csv(f"[{self.pattern_name()}] dados_mapeamento")

    def parse(self, response):
        # pode ser que seja necessário a validação

        nome, iscurrent = self.collect_metadata(response)

        if nome is None or iscurrent is None:
            pass
        else:
            self.municipios.append(nome)
            self.searches(nome, iscurrent, response.url)

    def searches(self, nome, iscurrent, url):
        for j in range(len(self.territories)):
            if self.state() in self.territories[j]["state_code"]:
                v1 = unidecode(self.territories[j]["name"].lower())
                v2 = v1.replace("d'", "do ")
                if v1 == nome or v2 == nome:
                    self.territories[j][self.pattern_name()].append(url)
                    self.territories[j][self.current_status()].append(iscurrent)

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

    def add_column_key(self):
        pattern = self.pattern_name()
        status = self.current_status()
        for y in range(len(self.territories)):
            self.territories[y][pattern] = []
            self.territories[y][status] = []

    def read_csv(self):
        file_path = (
            Path(__file__).parent / "../../resources/territories.csv"
        ).resolve()

        with open(file_path, encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.territories.append(row)
        csvfile.close()
