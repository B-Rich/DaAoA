class Message:

    message_num = 1

    def __init__(self, fwd_node, power, source, destination, content, message_id):
        self.message_id = message_id
        self.fwd_node = fwd_node
        self.power = power
        if fwd_node.RT.get(destination.name) is None:
            self.target_node = destination.name
        else:
            self.target_node = fwd_node.RT[destination.name]
        self.neighbor = fwd_node.get_neighbors()
        self.source = source
        self.destination = destination
        self.content = content
        Message.message_num += 1

    def __str__(self):
        return "ID: " + str(self.message_id) + "\nForwarding Node: \n" + str(self.fwd_node) + "\nNeighbors: " \
               + str([node.name for node in self.neighbor]) \
               + "\nContent: " + str(self.content) + "\nPower(mwh): " + str(self.power) \
               + "\nNext hop: " + str(self.target_node)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.source == other.source \
                   and self.destination == other.destination \
                   and self.content == other.content \
                   and self.id == other.id
        return None
