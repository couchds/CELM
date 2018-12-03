"""
load.py
Load the drugs and effects into the Neo4j database.

TODO:
  - use os.path module
  - parameterize queries

(Abatacept[Title/Abstract]) OR ORENCIA[Title/Abstract] 

"""
from neo4j.v1 import GraphDatabase, basic_auth

with open('.env', 'r') as infile:
    addr = infile.readline().strip().split('=')[1]
    user = infile.readline().strip().split('=')[1]
    pwd = infile.readline().strip().split('=')[1]

driver = GraphDatabase.driver(addr, auth=basic_auth(user, pwd))
session = driver.session()


with open('./data/serious_effects.list', 'r') as infile:
    for line in infile:
        effect_name = line.strip()
        session.run('MERGE (:Effect {name: "%s"})' % (effect_name))

with open('./data/drugs.list', 'r') as infile:
    for line in infile:
        drug_name, product_name = line.strip().split('\t')
        session.run('MERGE (:Drug {name: "%s", product_name: "%s"})' % (drug_name, product_name))

print('Done!')
