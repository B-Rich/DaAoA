import math
import weakref
from proto import Message
from trans_media import SignalCarrier, dequeue
from spf import aug_spf
from PyQt5.QtCore import Qt
from operator import itemgetter


class Node:
    instances = set()
    nodeCount = 0
    maxRange = 20
    maxCons = 1  # Maximum power consumption
    minCons = 0.05  # Least power consumption for transmission

    def __init__(self, name, x_pos, y_pos):
        self.name = name
        self.buffer = []
        self.message_id = []
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.t_range = 20
        self.consumption = 1
        self.neighbors = {}  # len(self.neighbors)
        self.instances.add(weakref.ref(self))
        self.distance = math.inf
        self.visited = False
        self.predecessor = None
        self.RT = {}  # Routing Table
        Node.nodeCount += 1

    def __eq__(self, node):
        if isinstance(node, self.__class__):
            return self.name == node.name
        return None

    def __str__(self):
        return " Name : " + str(self.name) + "\n Transmit Range(m): " + str(self.t_range) + " \n Power(mwh): " + str(
            self.consumption) + "\n Neighbors: " + str([node.name for node in self.neighbors])

    def __hash__(self):
        return id(self)

    def __lt__(self, node):
        if isinstance(node, self.__class__):
            return self.distance < node.distance
        return None

    def get_count(self):
        return self.nodeCount

    def get_range(self):
        return self.t_range

    def adj_range(self):
        if self.neighbors.values():
            far_node = max(self.neighbors.values())
            if far_node <= self.maxRange:
                self.consumption = self.minCons * far_node
                self.t_range = far_node

    def in_range(self, node):
        min_bound = (self.t_range - node.t_range) ** 2  # minimum value for condition to be true
        max_bound = (self.t_range + node.t_range) ** 2  # maximum value for condition to be true
        calc_range = (self.x_pos - node.x_pos) ** 2 + (self.y_pos - node.y_pos) ** 2  # actual range
        # if calc_range >= min_bound and calc_range <= max_bound:
        if min_bound <= calc_range <= max_bound and calc_range <= self.maxRange ** 2:
            return math.sqrt(calc_range)
        else:
            return False

    # def add_neighbor(self, neighbor, weight=0):
    def add_neighbor(self, neighbor):
        dist = self.in_range(neighbor)
        if dist:
            self.neighbors[neighbor] = dist

    def get_weight(self, neighbor):
        return self.neighbors[neighbor]

    def set_predecessor(self, prev):
        self.predecessor = prev

    def get_neighbors(self, list_f=1):
        if list_f:
            return list(self.neighbors.keys())
        else:
            return self.neighbors.keys()

    def prepare_msg(self, source, destination, message, power=0, message_id=Message.message_num):
        self.buffer.append(Message(self, power, source, destination, message, message_id))
        if message_id not in self.message_id:
            self.message_id.append(message_id)

    def send_msg(self):
        msg = dequeue(self.buffer)
        if msg.source == msg.destination:
            msg = dequeue(self.buffer)
            del msg
        else:
            self.prepare_msg(msg.source, msg.destination, msg.content, msg.power, msg.message_id)
            try:
                stats = \
                    [self.neighbors[node] for node in self.neighbors.keys() if node.name == self.buffer[0].target_node][
                        0]
            except:
                j = 1
            else:
                self.t_range = stats
            self.buffer[0].power += self.t_range * self.minCons
            del msg
            return dequeue(self.buffer)

    def receive_msg(self, message, textarea=None):
        if message.target_node != self.name and (-1 * message.message_id) not in self.message_id:
            self.message_id.append(-1 * message.message_id)
            if textarea is not None:
                textarea.setTextColor(Qt.red)
                textarea.append("Not mine, discarding.. " + self.name)
                textarea.setTextColor(Qt.white)
            print("Not mine, discarding.. " + self.name)
            return
        if message.fwd_node in self.get_neighbors() and self != message.destination \
                and message.message_id not in self.message_id:
            self.buffer.append(message)
            print("Forwarded to " + message.target_node + " successfully.")
            if textarea is not None:
                textarea.setTextColor(Qt.blue)
                textarea.append("Forwarded to " + message.target_node + " successfully.")
                textarea.setTextColor(Qt.white)
        if message.destination == self:
            self.message_id.append(message.message_id)
            print("Total power dissipated: " + str(message.power) + " mwh")
            print("Got it, I'm " + self.name)
            if textarea is not None:
                textarea.setTextColor(Qt.green)
                textarea.append("Got it, I'm " + self.name)
                textarea.append("Total power dissipated: " + str(message.power) + " mwh")
                textarea.setTextColor(Qt.white)
            return message.power
            # return message.power

    def generate_rt(self, grid):
        neighbor_list = [n_node.name for n_node in self.neighbors]
        far_nodes = list(grid.node_dictionary.keys() - neighbor_list - set(self.name))
        paths = []
        for dst_node in far_nodes:
            for src_node in neighbor_list:
                paths.append(aug_spf(grid, grid.get_node(src_node)
                                     , grid.get_node(dst_node)))
            print("Source Node: " + str(self))
            paths = sorted(paths, key=itemgetter(1))
            print(paths)
            next_hop = list(paths[0][0])
            self.RT[dst_node] = next_hop[0]

    @classmethod
    def get_nodes(cls):
        dead = set()
        for reference in cls.instances:
            node = reference()
            if node is not None:
                yield node
            else:
                dead.add(reference)
        cls.instances -= dead
