FROM python:3.6.8-stretch

WORKDIR /mnt/code

RUN adduser --system -u ${LOCAL_USER_ID:-1000} gazette \
  && apt-get update \
  && apt-get -y install poppler-utils postgresql-client

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
USER gazette
CMD ["celery", "-A", "tasks", "worker", "-B", "--loglevel=INFO", "--schedule=/tmp/celerybeat-schedule"]
