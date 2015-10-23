# Copyright (c) 2015 Fabian Kochem


try:
    from libtree.config import config
except ImportError:
    config = {
        'postgres': {
            'test_details': 'dbname=test_libtree user=postgres'
        }
    }

from libtree import Node, Transaction
from libtree.core.query import get_node
from libtree.core.tree import insert_node
import pytest

try:
    from psycopg2cffi import compat
except ImportError:
    pass
else:
    compat.register()

import psycopg2


"""
Create this structure:

/
  - node1
  - node2
    - node2-1
      - node2-1-1
        - node2-leaf
  - node3
"""

node_ids = {}


def get_or_create_node(cur, parent, properties, *args, **kwargs):
    xtype = properties.get('type')
    node_id = node_ids.get(xtype, None)
    if node_id is None:
        node = insert_node(cur, parent, properties=properties, *args, **kwargs)
        node_ids[xtype] = node.id
        return node
    return get_node(cur, node_id)


@pytest.fixture(scope='module')
def dsn():
    return config['postgres']['test_details']


@pytest.fixture(scope='module')
def trans(request, dsn):
    connection = psycopg2.connect(dsn)
    transaction = Transaction(connection, Node)

    node_ids.clear()
    transaction.install()
    transaction.commit()

    def fin():
        transaction.uninstall()
        transaction.commit()
    request.addfinalizer(fin)

    return transaction


@pytest.fixture(scope='module')
def cur(trans):
    return trans.cursor


@pytest.fixture
def root(cur):
    props = {
        'title': 'Root',
        'type': 'root',
        'boolean': False,
        'integer': 1
    }
    return get_or_create_node(cur, None, auto_position=False, properties=props)


@pytest.fixture
def node1(cur, root):
    props = {
        'type': 'node1',
        'title': 'Node 1'
    }
    return get_or_create_node(cur, root, position=4, auto_position=False,
                              properties=props)


@pytest.fixture
def node2(cur, root):
    props = {
        'type': 'node2',
        'title': 'Node 2',
        'boolean': True,
        'foo': 'bar'
    }
    return get_or_create_node(cur, root, position=5, auto_position=False,
                              properties=props)


@pytest.fixture
def node3(cur, root):
    props = {
        'type': 'node3',
        'title': 'Node 3'
    }
    return get_or_create_node(cur, root, position=6, auto_position=False,
                              properties=props)


@pytest.fixture
def node2_1(cur, node2):
    props = {
        'type': 'node2_1',
        'title': 'Node 2-1'
    }
    return get_or_create_node(cur, node2, auto_position=False,
                              properties=props)


@pytest.fixture
def node2_1_1(cur, node2_1):
    props = {
        'type': 'node2_1_1',
        'title': 'Node 2-1-1',
        'boolean': False
    }
    return get_or_create_node(cur, node2_1, auto_position=False,
                              properties=props)


@pytest.fixture
def node2_leaf(cur, node2_1_1):
    props = {
        'type': 'node2_leaf',
        'title': 'Node 2-leaf'
    }
    return get_or_create_node(cur, node2_1_1, auto_position=False,
                              properties=props)
