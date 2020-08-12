FROM python:3.7-stretch

#RUN useradd -rm -d /home/gazette -s /bin/bash -g root -G sudo -u 1000 gazette

RUN export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && apt-get install -y \
    poppler-utils \
    postgresql-client \
    wait-for-it \ 
    default-jre \ 
    && rm -rf /var/lib/apt/lists/*

#USER gazette

WORKDIR /mnt/code

COPY . . 

ADD http://archive.apache.org/dist/tika/tika-app-1.24.jar tika-app.jar

RUN pip install --no-cache-dir -r requirements.txt 

#RUN chmod 755 tika-app.jar 

WORKDIR /mnt/code/data_collection

CMD scrapy crawl sc_florianopolis
