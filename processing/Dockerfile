FROM python:3.7-stretch

WORKDIR /mnt/code

RUN adduser --system -u ${LOCAL_USER_ID:-1000} gazette \
  && apt-get update \
  && apt-get -y install poppler-utils postgresql-client wait-for-it default-jre

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# install Apache Tika
ADD http://ftp.unicamp.br/pub/apache/tika/tika-app-1.22.jar /

RUN chmod 755 /tika-app-1.22.jar

USER gazette
