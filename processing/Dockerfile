FROM python:3.7-stretch

RUN export DEBIAN_FRONTEND=noninteractive && \
apt-get update && apt-get install -y \
poppler-utils \
postgresql-client \
wait-for-it \ 
default-jre 

WORKDIR /usr/src/app

COPY . . 

ADD http://archive.apache.org/dist/tika/tika-app-1.24.jar tika-app.jar

RUN pip install --no-cache-dir -r requirements.txt 

RUN chmod 755 tika-app.jar 

WORKDIR /usr/src/app/data_collection

CMD scrapy crawl sc_florianopolis



