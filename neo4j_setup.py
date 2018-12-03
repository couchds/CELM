from neo4j.v1 import GraphDatabase, basic_auth

with open('.env', 'r') as infile:
    addr = infile.readline().strip().split('=')[1]
    user = infile.readline().strip().split('=')[1]
    pwd = infile.readline().strip().split('=')[1]

driver = GraphDatabase.driver(addr, auth=basic_auth(user, pwd))
session = driver.session()

# set up node indexes
session.run('CREATE INDEX ON :Drug(name)')
session.run('CREATE INDEX ON :SideEffect(name)')
print('Done')
