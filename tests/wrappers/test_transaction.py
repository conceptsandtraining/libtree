# Copyright (c) 2015 Fabian Kochem


from libtree.wrappers import Transaction
from mock import Mock


def test_it_takes_a_connection(dsn):
    conn = Mock()
    assert Transaction(connection=conn).connection is conn


def test_commit():
    conn = Mock()
    Transaction(connection=conn).commit()
    assert conn.commit.called


def test_rollback():
    conn = Mock()
    Transaction(connection=conn).rollback()
    assert conn.rollback.called


def xtest_print_tree():
    raise NotImplementedError


def xtest_get_tree_size():
    raise NotImplementedError


def xtest_get_root_node():
    raise NotImplementedError


def xtest_insert_root_node():
    raise NotImplementedError


def xtest_get_node():
    raise NotImplementedError


def xtest_get_node_at_position():
    raise NotImplementedError


def xtest_get_nodes_by_property_dict():
    raise NotImplementedError


def xtest_get_nodes_by_property_key():
    raise NotImplementedError


def xtest_get_nodes_by_property_value():
    raise NotImplementedError
