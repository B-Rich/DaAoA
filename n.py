from node import Node as n
from trans_media import SignalCarrier as sc
from grid import Grid
import random
from spf import aug_spf, dijkstra, shortest

if __name__ == '__main__':
    Grid = Grid()
    Air = sc()
    Grid.add_node('A', 5, 5)
    Grid.add_node('B', 7, 8)
    Grid.add_node('C', 7, 27)
    Grid.add_node('D', 5.5, 5.5)
    Grid.add_node('E', 8, 10)
    # Grid.establish_conn()
    Grid.establish_conn(True)
    nd = Grid.node_dictionary
    A = nd['A']
    B = nd['B']
    C = nd['C']
    D = nd['D']
    E = nd['E']
    for x in range(5):
        print("Transmission attempt: " + str(x+1))
        src = nd[random.choice(list(nd.keys()))]
        dst = nd[random.choice(list(nd.keys()))]
        while src is dst:
            dst = nd[random.choice(list(nd.keys()))]
        print("Sending from: " + src.name + " to " + dst.name)
        print("\n\n")
        src.prepare_msg(src, dst, 'Hi')
        # m1 = src.send_msg()
        # Air.carry(m1)
        while src.buffer:
            print(src)
            print(src.RT)
            print("Current Transmission range: " + str(src.t_range))
            Air.carry(src.send_msg())
            rcv = list(Air.transmit_to)
            print("Next hop: " + str(Air.message.target_node))
            Air.propagate()
            for node in rcv:
                if node.buffer:
                    src = node
            print("\n")
            # Air.carry(Grid.node_dictionary['B'].send_msg())
            # Air.propagate()
