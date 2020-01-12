import os
import logging
import json
import sys
import re
import csv

from kafka import KafkaConsumer
import pydgraph

logging.basicConfig(level=logging.INFO)

CNPJ_REGEX = r"\d{2}\.\d{3}\.\d{3}\/\d{4}\-\d{2}"
EMAIL_REGEX = r"\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}"

# stores all the cities data
CITIES = {}


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


def get_dgraph_server():
    server = os.environ["DGRAPH_SERVER"]
    logging.info(f"Dgraph server: {server}")
    return server


def get_dgraph_client():
    stub = pydgraph.DgraphClientStub(get_dgraph_server())
    return pydgraph.DgraphClient(stub), stub


def get_city_uuid(t, msg):
    query = (
        "{ var(func: has(ibge)) { id as ibge }\n"
        'city(func: eq(val(id), "' + msg["territory_id"] + '")) { uid } }'
    )
    res = t.query(query)
    rjson = json.loads(res.json)
    if len(rjson["city"]) > 0:
        return rjson["city"][0]["uid"]
    return None


def update_city(dgraph, msg):
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
    query = "{cnpj(func: has(cnpj)) { uid cnpj }}"
    res = t.query(query)
    cnpjs = {}
    for cnpj in json.loads(res.json)["cnpj"]:
        cnpjs[cnpj["cnpj"]] = cnpj["uid"]
    return cnpjs


def update_cnpj(dgraph, msg):
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
    t = dgraph.txn()
    try:
        cnpjs = get_cnpj_uuid(t, msg)
        city = get_city_uuid(t, msg)
        cnpj_business = []
        for c in msg["cnpj"]:
            cnpj_business.append({"uid": cnpjs[c]})
        if len(cnpj_business) > 0:
            city_links = {"uid": city, "business": cnpj_business}
            res = t.mutate(set_obj=city_links, commit_now=True)
            logging.info(f"Edge between {city} and {cnpj_business} has been created")
    finally:
        t.discard()


def update_graph(dgraph, msg):
    # get a new transaction
    update_city(dgraph, msg)
    update_cnpj(dgraph, msg)
    link_city_cnpj(dgraph, msg)


def set_dgraph_schema(dgraph):
    schema = """
    id: string @index(exact) .
    cnpj: string .
    email: string .
    """
    dgraph.alter(pydgraph.Operation(schema=schema))


# Drop All - discard all data and start from a clean slate.
def drop_all(client):
    return client.alter(pydgraph.Operation(drop_all=True))


def load_cities():
    with open("/mnt/data/municipios.csv", "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            CITIES[row["Código Município Completo"]] = row


def process_gazettes():
    consumer = create_kafka_consumer()
    dgraph, stub = get_dgraph_client()
    load_cities()
    drop_all(dgraph)
    # set_dgraph_schema(dgraph)
    for data in consumer:
        msg = json.loads(data.value.decode())
        msg["cnpj"] = re.findall(CNPJ_REGEX, msg["source_text"])
        msg["email"] = re.findall(EMAIL_REGEX, msg["source_text"])
        update_graph(dgraph, msg)
    stub.close()


if __name__ == "__main__":
    process_gazettes()
