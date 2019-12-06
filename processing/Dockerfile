FROM python:3.7-stretch

WORKDIR /mnt/code

COPY requirements.txt requirements.txt

# install Apache Tika
ADD http://ftp.unicamp.br/pub/apache/tika/tika-app-1.22.jar /

RUN adduser --system -u ${LOCAL_USER_ID:-1000} gazette \
	&& apt-get update \
	&& apt-get -y install poppler-utils postgresql-client wait-for-it default-jre \
	&& pip install --no-cache-dir -r requirements.txt \
	&& chmod 755 /tika-app-1.22.jar

USER gazette
