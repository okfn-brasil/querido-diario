import os
import logging
import json
import sys
import re
from kafka import KafkaConsumer

logging.basicConfig(level=logging.INFO)

CNPJ_REGEX = r"\d{2}\.\d{3}\.\d{3}\/\d{4}\-\d{2}"
EMAIL_REGEX = r"\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}"


def get_topic():
    topic = os.environ["KAFKA_TOPIC"]
    logging.info(f"Kafka topic: {topic}")
    return topic


def get_kafka_servers():
    server = os.environ["KAFKA_SERVERS"]
    logging.info(f"Kafka server: {server}")
    return server


def get_group_id():
    group = os.environ["KAFKA_GROUP_ID"]
    logging.info(f"Kafka server: {group}")
    return group


def create_kafka_consumer():
    consumer = KafkaConsumer(
        get_topic(),
        group_id=get_group_id(),
        bootstrap_servers=get_kafka_servers(),
        api_version=(0, 10, 1),
    )
    logging.info("Kafka consumer created")
    return consumer


def process_gazettes():
    consumer = create_kafka_consumer()
    for data in consumer:
        msg = json.loads(data.value.decode())
        city = msg["territory_id"]
        text = msg["source_text"]
        cnpj = re.findall(CNPJ_REGEX, text)
        email = re.findall(EMAIL_REGEX, text)
        logging.info(f"City: {city} -> CPNJ: {cnpj}, EMAIL: {email}")


if __name__ == "__main__":
    process_gazettes()
