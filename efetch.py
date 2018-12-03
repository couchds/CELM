"""
efetch.py
Use Entrez's API to search for co-occurring compound-effect terms.
"""
from Bio import Entrez
from neo4j.v1 import GraphDatabase, basic_auth
import time
Entrez.email = "couchd@musc.edu"

with open('.env', 'r') as infile:
    addr = infile.readline().strip().split('=')[1]
    user = infile.readline().strip().split('=')[1]
    pwd = infile.readline().strip().split('=')[1]

driver = GraphDatabase.driver(addr, auth=basic_auth(user, pwd))
session = driver.session()

all_drugs = session.run("MATCH (n: Drug) RETURN n.name AS name, n.product_name AS product_name")
all_drugs_data = [(d['name'], d['product_name']) for d in all_drugs]
all_effects = session.run("MATCH (n: Effect) RETURN n.name AS name")
all_effects_data = [d['name'] for d in all_effects]
for drug_data in all_drugs_data:
    query = '"%s"[title/abstract] OR "%s"[title/abstract]' % drug_data
    result = Entrez.esearch(db="pubmed", term=query, retmax=1000000)
    id_list = Entrez.read(result)["IdList"]
    time.sleep(3)
