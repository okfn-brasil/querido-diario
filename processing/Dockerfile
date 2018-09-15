FROM python:3.6

WORKDIR /mnt/code

RUN adduser --system gazette \
  && mkdir /mnt/data \
  && chown gazette. /mnt/data \
  && apt-get update \
  && apt-get -y install poppler-utils postgresql-client

COPY data/territories.csv /mnt/data/
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
USER gazette
CMD ["celery", "-A", "tasks", "worker", "-B", "--loglevel=INFO", "--schedule=/tmp/celerybeat-schedule"]
