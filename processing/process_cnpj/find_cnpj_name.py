import logging
import json
import os
import requests

from kafka import KafkaConsumer
import pydgraph

logging.basicConfig(level=logging.INFO)

URL = "https://brasil.io/api/dataset/documentos-brasil/documents/data"
URL_PARTNERS = "https://brasil.io/api/dataset/socios-brasil/socios/data"


def get_topic():
    """
    Get the Kafka topic name where the cnpj are published
    """
    topic = os.environ["KAFKA_CNPJ_TOPIC"]
    logging.info(f"Kafka topic: {topic}")
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
    Establishes connection to Kafka to consume the CNPJ found
    """
    consumer = KafkaConsumer(
        get_topic(),
        group_id=get_group_id(),
        bootstrap_servers=get_kafka_servers(),
        api_version=(0, 10, 1),
    )
    logging.info("Kafka consumer created")
    return consumer


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


def do_request(url, params):
    """
    Common method to perform a request to the given URL and query string
    """
    if url is None:
        return
    r = requests.get(url, params=params)
    return r.json().get("results", [])


def get_cnpj_data(cnpj):
    """
    Query the Brasil.io API to check if there is addtional info for the given
    CNPJ
    """
    return do_request(URL, {"document": cnpj})


def get_cnpj_partners(cnpj):
    """
    Query the Brasil.io API to check if there is addtional info about business partners
    for the given CNPJ
    """
    return do_request(URL_PARTNERS, {"cnpj": cnpj})


def get_cnpj_uuid(t, cnpj):
    """
    Query the graph database to get the uid of the node for the given CNPJ
    """
    query = (
        "{ var(func: has(cnpj)) { cnpj as cnpj }\n"
        'cnpj(func: eq(val(cnpj), "' + cnpj + '")) { uid } }'
    )
    res = t.query(query)
    rjson = json.loads(res.json)
    if len(rjson["cnpj"]) > 0:
        if len(rjson["cnpj"]) > 1:
            logging.warning(
                f"There are more then one node with the CNPJ {cnpj}. Let's use the first one"
            )
        return rjson["cnpj"][0]["uid"]
    return None


def get_partner_uuid(dgraph, partner):
    """
    Look for the partner by name

    Returns the partner uid if exists
    """
    t = dgraph.txn()
    try:
        query = (
            "{ var(func: has(name)) { id as name }\n"
            'partner(func: eq(val(id), "' + partner["nome_socio"] + '")) { uid } }'
        )
        res = t.query(query)
        rjson = json.loads(res.json)
        if len(rjson["partner"]) > 0:
            return rjson["partner"][0]["uid"]
    finally:
        t.discard()


def add_partner(dgraph, partner):
    """
    Adds the partner in the graph database
    """
    t = dgraph.txn()
    try:
        p = {
            "name": partner["nome_socio"],
            "qualificacao": partner["qualificacao_socio"],
            "type": partner["tipo_socio"],
        }
        res = t.mutate(set_obj=p, commit_now=True)
        logging.info(f"{p['name']}({next(iter(res.uids))}) updated!")
        return res.uids[next(iter(res.uids))]
    finally:
        t.discard()


def link_cnpj_partners(dgraph, cnpj_uuid, partner_uuid):
    """
    Create an edge between the companies and its partner
    """
    if cnpj_uuid is None or partner_uuid is None:
        logging.info("Missing CNPJ or partner uids!")
        return

    t = dgraph.txn()
    try:
        cnpj_partners = [{"uid": partner_uuid}]
        cnpj_links = {"uid": cnpj_uuid, "partners": cnpj_partners}
        res = t.mutate(set_obj=cnpj_links, commit_now=True)
        logging.info(f"Edge between {cnpj_uuid} and {cnpj_partners} has been created")
    finally:
        t.discard()


def add_update_partner(dgraph, cnpj_uuid, partner):
    """
    Add and update the partners and their edges
    """
    # check if the given partner already exists
    uuid = get_partner_uuid(dgraph, partner)
    if uuid is None:
        uuid = add_partner(dgraph, partner)
    # link partner and companies
    link_cnpj_partners(dgraph, cnpj_uuid, uuid)


def update_cnpj(dgraph, cnpj, partners):
    """
    Update the CNPJ node with the data found in the Brasil.io API
    """
    if cnpj is None or len(cnpj) == 0:
        return
    t = dgraph.txn()
    try:
        # Let's use just the first item for now
        cnpj = cnpj[0]
        document = cnpj.get("document", "")
        cnpj_uuid = get_cnpj_uuid(t, document)
        if cnpj_uuid is None:
            # TODO maybe add the node?
            logging.info(f"{document}({cnpj_uuid}) skipped!")
            return

        cnpjobj = {
            "uid": cnpj_uuid,
            "name": cnpj.get("name", "Unknown"),
            "type": cnpj.get("document_type", "Unknown"),
        }

        # if we have companies partners, we need to link them
        if partners:
            cnpjobj["razao_social"] = partners[0].get("razao_social", "Unknown")
            for partner in partners:
                add_update_partner(dgraph, cnpj_uuid, partner)

        res = t.mutate(set_obj=cnpjobj, commit_now=True)
        logging.info(f"{cnpjobj['name']}({cnpjobj['uid']}) updated!")
    finally:
        t.discard()


def process_cnpj():
    consumer = create_kafka_consumer()
    dgraph, stub = get_dgraph_client()
    for data in consumer:
        msg = data.value.decode()
        if "." in msg:
            # skip old data. TODO Remove this if soon
            continue
        logging.info(f"Get: {msg}")
        cnpj = get_cnpj_data(msg)
        partners = get_cnpj_partners(msg)
        update_cnpj(dgraph, cnpj, partners)
    stub.close()


if __name__ == "__main__":
    process_cnpj()
