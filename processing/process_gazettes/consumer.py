import os
import logging
import json
import sys
import re
import csv

from kafka import KafkaConsumer, KafkaProducer
import pydgraph

logging.basicConfig(level=logging.INFO)

CNPJ_REGEX = r"\d{2}\.\d{3}\.\d{3}\/\d{4}\-\d{2}"
EMAIL_REGEX = r"\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}"

# stores all the cities data
CITIES = {}


def get_topic():
    """
    Get the Kafka topic name where the gazettes are published
    """
    topic = os.environ["KAFKA_TOPIC"]
    logging.info(f"Kafka topic: {topic}")
    return topic


def get_cnpj_topic():
    """
    Get Kafka topic name where the CNPJ should be published
    """
    topic = os.environ["KAFKA_CNPJ_TOPIC"]
    logging.info(f"Kafka CNPJ topic: {topic}")
    return topic


def get_kafka_servers():
    """
    Get Kafka servers info used by the consumer and producer clients
    """
    server = os.environ["KAFKA_SERVERS"]
    logging.info(f"Kafka server: {server}")
    return server


def get_group_id():
    """
    Get the group id used by the Kafka consumer client
    """
    group = os.environ["KAFKA_GROUP_ID"]
    logging.info(f"Kafka server: {group}")
    return group


def create_kafka_consumer():
    """
    Establishes connection to Kafka to consume the gazattes
    """
    consumer = KafkaConsumer(
        get_topic(),
        group_id=get_group_id(),
        bootstrap_servers=get_kafka_servers(),
        api_version=(0, 10, 1),
    )
    logging.info("Kafka consumer created")
    return consumer


def create_kafka_producer():
    """
    Establishes a connection to Kafka cluster to publish the CNPJ found
    """
    return KafkaProducer(
        bootstrap_servers=get_kafka_servers(),
        client_id="gazettes_processer",
        api_version=(0, 10, 1),
    )


def get_dgraph_server():
    """
    Get DGraph servers info used to establish the connection with the graph
    database
    """
    server = os.environ["DGRAPH_SERVER"]
    logging.info(f"Dgraph server: {server}")
    return server


def get_dgraph_client():
    """
    Establish a connection to DGraph and returns the client
    """
    stub = pydgraph.DgraphClientStub(get_dgraph_server())
    return pydgraph.DgraphClient(stub), stub


def get_city_uuid(t, msg):
    """
    Query the graph database to get the uid of the node for the given city
    """
    query = (
        "{ var(func: has(ibge)) { id as ibge }\n"
        'city(func: eq(val(id), "' + msg["territory_id"] + '")) { uid } }'
    )
    res = t.query(query)
    rjson = json.loads(res.json)
    if len(rjson["city"]) > 0:
        return rjson["city"][0]["uid"]
    return None


def add_city(dgraph, msg):
    """
    Adds the city in the graph database
    """
    t = dgraph.txn()
    try:
        city_uuid = get_city_uuid(t, msg)
        if city_uuid is not None:
            return

        city = {
            "ibge": msg["territory_id"],
            "nome": CITIES[msg["territory_id"]]["Nome_Município"],
            "estado": CITIES[msg["territory_id"]]["Nome_UF"],
        }
        res = t.mutate(set_obj=city, commit_now=True)
        logging.info(f"{city['nome']}({city['ibge']}) updated!")
    finally:
        t.discard()


def get_cnpj_uuid(t, msg):
    """
    Query the graph database to get the uid of the node for the given cnpj
    """
    query = "{cnpj(func: has(cnpj)) { uid cnpj }}"
    res = t.query(query)
    cnpjs = {}
    for cnpj in json.loads(res.json)["cnpj"]:
        cnpjs[cnpj["cnpj"]] = cnpj["uid"]
    return cnpjs


def add_cnpj(dgraph, msg):
    """
    Adds the CNPJ in the graph database
    """
    t = dgraph.txn()
    try:
        cnpjs = get_cnpj_uuid(t, msg)
        m = []
        for cnpj in msg["cnpj"]:
            if cnpj not in cnpjs:
                m.append({"cnpj": cnpj})
        if len(m) > 0:
            res = t.mutate(set_obj=m, commit_now=True)
            logging.info(f"{m} updated!")
    finally:
        t.discard()


def link_city_cnpj(dgraph, msg):
    """
    Create the edges between cities and the CNPJ cited in their gazettes
    """
    t = dgraph.txn()
    try:
        cnpjs = get_cnpj_uuid(t, msg)
        city = get_city_uuid(t, msg)
        cnpj_business = []
        for c in msg["cnpj"]:
            cnpj_business.append({"uid": cnpjs[c]})
        if len(cnpj_business) > 0:
            city_links = {"uid": city, "related": cnpj_business}
            res = t.mutate(set_obj=city_links, commit_now=True)
            logging.info(f"Edge between {city} and {cnpj_business} has been created")
    finally:
        t.discard()


def update_graph(dgraph, msg):
    """
    Update the graph databse with the given gazette
    """
    # get a new transaction
    add_city(dgraph, msg)
    add_cnpj(dgraph, msg)
    link_city_cnpj(dgraph, msg)


def drop_all(client):
    """
    Drop all data in the graph database
    """
    return client.alter(pydgraph.Operation(drop_all=True))


def load_cities():
    """
    Loads the CSV from IBGE with the cities data
    """
    with open("/mnt/data/municipios.csv", "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            CITIES[row["Código Município Completo"]] = row


def update_cnpj_data(producer, topic, msg):
    """
    Publishes the CNPJ found in the gazette to another kafka topic.
    """
    if len(msg["cnpj"]) == 0:
        return
    for cnpj in msg["cnpj"]:
        producer.send(topic, cnpj.encode())
    producer.flush()
    logging.info(f"CNPJ sent: {msg['cnpj']}")


def process_gazettes():
    consumer = create_kafka_consumer()
    producer = create_kafka_producer()
    cnpj_topic = get_cnpj_topic()
    dgraph, stub = get_dgraph_client()
    load_cities()
    drop_all(dgraph)
    for data in consumer:
        msg = json.loads(data.value.decode())
        msg["cnpj"] = re.findall(CNPJ_REGEX, msg["source_text"])
        msg["cnpj"] = [
            cnpj.replace(".", "").replace("/", "").replace("-", "")
            for cnpj in msg["cnpj"]
        ]
        update_graph(dgraph, msg)
        update_cnpj_data(producer, cnpj_topic, msg)
    stub.close()


if __name__ == "__main__":
    process_gazettes()
