FROM python:3.7-stretch

WORKDIR /mnt/code

COPY requirements.txt requirements.txt

# install Apache Tika
COPY ./download-tika-app.py /download-tika-app.py
RUN cd / \
    && python download-tika-app.py \
    && rm -f download-tika-app.py

RUN adduser --system -u ${LOCAL_USER_ID:-1000} gazette \
	&& apt-get update \
	&& apt-get -y install poppler-utils postgresql-client wait-for-it default-jre \
	&& pip install --no-cache-dir -r requirements.txt \
	&& chmod 755 /tika-app.jar

USER gazette
