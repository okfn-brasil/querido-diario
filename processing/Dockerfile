FROM python:3.7-stretch

ARG LOCAL_USER_ID

WORKDIR /mnt/code

COPY requirements.txt requirements.txt

# install Apache Tika
ADD http://archive.apache.org/dist/tika/tika-app-1.24.jar /tika-app.jar

RUN adduser --system -u ${LOCAL_USER_ID:-1000} gazette \
	&& apt-get update \
	&& apt-get -y install poppler-utils postgresql-client wait-for-it default-jre \
	&& pip install --no-cache-dir -r requirements.txt \
	&& chmod 755 /tika-app.jar

USER gazette
