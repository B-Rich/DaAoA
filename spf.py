import heapq as heq
import queue


def shortest(node, path):
    if node.predecessor:
        path.append(node.predecessor.name)
        shortest(node.predecessor, path)
    return


def dijkstra(grid, src):
    src.distance = 0

    unvisited_queue = [(node.distance, node) for node in grid]
    heq.heapify(unvisited_queue)

    while len(unvisited_queue):
        unvisited_nodes = heq.heappop(unvisited_queue)
        # print(unvisited_nodes[0])
        current = unvisited_nodes[1]
        current.visited = True

        for next_node in current.neighbors:
            if next_node.visited:
                continue
            new_dist = current.distance + current.get_weight(next_node)

            if new_dist < next_node.distance:
                next_node.distance = new_dist
                next_node.predecessor = current

        while len(unvisited_queue):
            heq.heappop(unvisited_queue)

        unvisited_queue = [(node.distance, node) for node in grid if not node.visited]
        heq.heapify(unvisited_queue)

    for node in grid.node_dictionary.values():
        # print(node)
        node.visited = False


def aug_spf(grid, src, dst):
    q = queue.PriorityQueue()
    parents = {}
    distances = {}
    start_distance = float("inf")

    for node in grid.node_dictionary.values():
        distance = start_distance
        if src is node:
            distances[src.name] = 0
            src.distance = 0
        else:
            distances[node.name] = distance
        parents[node.name] = None

    q.put(([0, src]))
    while not q.empty():
        node_tuple = q.get()
        node = node_tuple[1]
        for neighbor in node.neighbors:
            candidate_distance = distances[node.name] + node.neighbors[neighbor]
            if distances[neighbor.name] > candidate_distance:
                distances[neighbor.name] = candidate_distance
                parents[neighbor.name] = node.name
                # primitive but effective negative cycle detection
                if candidate_distance < -1000:
                    raise Exception("Negative cycle detected")
                q.put(([distances[neighbor.name], neighbor]))
    shortest_path = []
    end = dst.name
    while end is not None:
        shortest_path.append(end)
        end = parents[end]

    shortest_path.reverse()

    return shortest_path, distances[dst.name]
