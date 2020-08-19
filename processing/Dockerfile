FROM python:3.7-stretch

RUN export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && apt-get install --no-install-recommends -y \
    poppler-utils \
    postgresql-client \
    wait-for-it \ 
    default-jre \ 
    && rm -rf /var/lib/apt/lists/*


WORKDIR /mnt/code

COPY . . 

ADD http://archive.apache.org/dist/tika/tika-app-1.24.jar tika-app.jar

RUN pip install --no-cache-dir -r requirements.txt 

WORKDIR /mnt/code/data_collection

CMD scrapy crawl sc_florianopolis
