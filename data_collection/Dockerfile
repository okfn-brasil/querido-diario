FROM python:3.6.5

# app

WORKDIR /mnt/code

RUN apt-get update \
  && apt-get -y install poppler-utils

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /mnt/code/gazette
