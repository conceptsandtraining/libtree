import psycopg2
import math
import libtree


def postgres_create_db(dsn, dbname):
    conn = psycopg2.connect(dsn)
    conn.set_isolation_level(0)
    cur = conn.cursor()
    try:
        cur.execute("DROP DATABASE {}".format(dbname))
        print("dropped database {}".format(dbname))
    except psycopg2.ProgrammingError:
        # database does not exist
        pass
    cur.execute("CREATE DATABASE {}".format(dbname))
    print("created database {}".format(dbname))


def postgres_analyze_db(cur):
    cur.execute('ANALYZE VERBOSE')


def calculate_tree_size(levels, per_level):
    # time.sleep(0.5)
    if per_level == 1:
        return levels
    return int(((1 - per_level ** (levels + 1)) / (1 - per_level)) - 1)


def generate_tree(per, levels, per_level):
    def insert_children(parent, label, current_depth=1):
        label.append("x")
        for x in range(per_level):
            label2 = label.copy()
            label2.append(x)
            title = "".join(map(str, label2))
            properties = {"title": title}
            node = libtree.insert_node(
                per, parent, properties, position=x, auto_position=False)
            if current_depth < levels:
                insert_children(node, label2, current_depth + 1)
    expected_nodes = calculate_tree_size(levels, per_level)
    print("generating tree with {} nodes..".format(expected_nodes))
    root = libtree.insert_node(per, None, properties={"title": "0"})
    insert_children(root, [0])


def format_duration(n):
    units = ["s", "ms", 'us', "ns"]
    scaling = [1, 1e3, 1e6, 1e9]
    if n > 0.0 and n < 1000.0:
        order = min(-int(math.floor(math.log10(n)) // 3), 3)
    elif n >= 1000.0:
        order = 0
    else:
        order = 3
    return "{:.2f}{}".format(n * scaling[order], units[order])
