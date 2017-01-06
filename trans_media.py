def dequeue(_list):
    _list.reverse()
    item = _list.pop()
    _list.reverse()
    return item


class SignalCarrier:
    def __init__(self):
        self.sending_node = None
        self.message = None
        self.transmit_to = None
        self.total_power = 0

    def propagate(self, textarea=None):
        if self.message:
            for node in self.transmit_to:
                # print(node)
                node.receive_msg(self.message, textarea)
            self.message = None
        else:
            return 'No message transmitted'

    def carry(self, message):
        self.sending_node = message.fwd_node
        self.message = message
        self.transmit_to = [node for node in message.fwd_node.neighbors
                            if node.name == message.target_node]
        print(self.transmit_to[0].name)
