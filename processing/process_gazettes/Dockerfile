FROM python:3.7-stretch

WORKDIR /mnt/code

COPY requirements.txt requirements.txt

RUN adduser --system -u ${LOCAL_USER_ID:-1000} gazette \
	&& apt-get update \
	&& pip install --no-cache-dir -r requirements.txt

USER gazette
