FROM python:3.6

WORKDIR /mnt/code

RUN apt-get update \
  && apt-get -y install poppler-utils postgresql-client

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
CMD ["celery", "-A", "tasks", "worker", "-B", "--loglevel=INFO"]
