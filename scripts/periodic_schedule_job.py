import datetime
from decouple import config, Csv

from scrapinghub import ScrapinghubClient

YESTERDAY = datetime.date.today() - datetime.timedelta(days=1)

ENABLED_SPIDERS = [
    "am_manaus",
    "al_maceio",
    "ba_salvador",
    "go_goiania",
    "ms_campo_grande",
    "pb_joao_pessoa",
    "pi_teresina",
    "rj_rio_de_janeiro",
    "rn_natal",
    "rr_boa_vista",
    "sc_florianopolis",
    "to_palmas",
]


def periodic_schedule_job(spider_name, start_date):
    client = ScrapinghubClient(config("SHUB_APIKEY"))
    project = client.get_project(config("SCRAPY_CLOUD_PROJECT_ID"))

    job_settings = {
        "FILES_STORE": config("FILES_STORE"),
        "QUERIDODIARIO_DATABASE_URL": config("QUERIDODIARIO_DATABASE_URL"),
        "AWS_ACCESS_KEY_ID": config("AWS_ACCESS_KEY_ID"),
        "AWS_SECRET_ACCESS_KEY": config("AWS_SECRET_ACCESS_KEY"),
        "AWS_ENDPOINT_URL": config("AWS_ENDPOINT_URL"),
        "AWS_REGION_NAME": config("AWS_REGION_NAME"),
        "SPIDERMON_TELEGRAM_SENDER_TOKEN": config("SPIDERMON_TELEGRAM_SENDER_TOKEN"),
        "SPIDERMON_TELEGRAM_RECIPIENTS": config(
            "SPIDERMON_TELEGRAM_RECIPIENTS", cast=Csv(),
        ),
        "SPIDERMON_TELEGRAM_FAKE": config("SPIDERMON_TELEGRAM_FAKE", cast=bool),
    }

    job_args = {
        "start_date": start_date,
    }

    spider = project.spiders.get(spider_name)
    spider.jobs.run(
        job_settings=job_settings, job_args=job_args,
    )


if __name__ == "__main__":
    YESTERDAY = datetime.date.today() - datetime.timedelta(days=1)
    for spider_name in ENABLED_SPIDERS:
        periodic_schedule_job(spider_name, YESTERDAY.strftime("%Y-%m-%d"))
