from config import config
from pdb import set_trace as trace
from persistance import *
import os
from tree import *

if config['mysql']['enabled']:
    conf = config['mysql']
    per = MySQLPersistance(host=conf['host'],
                           user=conf['user'],
                           passwd=conf['password'],
                           db=conf['database'])
else:
    per = PostgreSQLPersistance(config['postgres']['details'])

cache = {}

per.drop_tables()
per.create_tables()
db.commit()

start_path = '/'
root = create_node(per, None, 'folder', description=start_path)
cache[start_path] = root.id

for dirname, folders, files in os.walk(start_path):
    for folder in folders:
        path = os.path.join(dirname, folder)
        #print path
        parent = cache[dirname]
        node = create_node(per, parent, 'folder', description=path[0:254])
        cache[path] = node.id

    for filex in files:
        path = os.path.join(dirname, filex)
        #print path
        parent = cache[dirname]
        node = create_node(per, parent, 'file', description=path[0:254])
        cache[path] = node.id

    db.commit()

#trace()
