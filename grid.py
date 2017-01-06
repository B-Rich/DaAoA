from node import Node


class Grid:
    def __init__(self):
        self.node_dictionary = {}
        self.predecessor = None
        self.num_nodes = 0

    def __iter__(self):
        return iter(self.node_dictionary.values())

    def add_node(self, node_id, node_xpos, node_ypos):
        self.num_nodes += 1
        new_node = Node(node_id, node_xpos, node_ypos)
        self.node_dictionary[node_id] = new_node
        return new_node

    def get_node(self, n):
        if n in self.node_dictionary:
            return self.node_dictionary[n]
        else:
            return None

    def add_edge(self, src, dst):
        if src not in self.node_dictionary:
            print("Node doesn't exist")  # self.add_node(src)
            return False
        if dst not in self.node_dictionary:
            print("Node doesn't exist")
            return False

        self.node_dictionary[src].add_neighbor(self.node_dictionary[dst])
        self.node_dictionary[dst].add_neighbor(self.node_dictionary[src])

    def get_nodes(self):
        return self.node_dictionary.keys()

    def set_predecessor(self, current):
        self.predecessor = current

    def get_predecessor(self):
        return self.predecessor

    def establish_conn(self, opt=False):
        for node in self.node_dictionary:
            for other_node in self.node_dictionary:
                if node is not other_node:
                    self.add_edge(node, other_node)
        if opt:
            for node in self.node_dictionary.values():
                node.generate_rt(self)
                node.adj_range()

    def print_nodes(self):
        for node in self.node_dictionary.values():
            print(node)
