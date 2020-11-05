import argparse
import csv
from jinja2 import Environment, FileSystemLoader


def load_template(spider_data):
    env = Environment(loader=FileSystemLoader("."))
    template = env.get_template("spider_template.py")
    print(
        template.render(
            spider_class_base=spider_data["spider_class_base"],
            spider_class_name=spider_data["spider_class_name"],
            spider_name=spider_data["spider_name"],
            allowed_domain=spider_data["allowed_domain"],
            start_date=spider_data["start_date"],
            base_url=spider_data["base_url"],
            territory_id=spider_data["territory_id"],
        )
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Generate a spider structure from CSV.")
    parser.add_argument("file")
    args = parser.parse_args()

    with open(args.file) as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            spider_data = {
                "spider_class_base": row["base"],
                "spider_class_name": f"{row['state'].title()}{row['city'].title()}",
                "spider_name": f"{row['state'].lower()}_{row['city'].lower()}",
                "allowed_domain": row["domain"],
                "start_date": "",
                "base_url": row["base_url"],
                "territory_id": row["territory_id"],
            }
            load_template(spider_data)
