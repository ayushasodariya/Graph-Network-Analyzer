"""Core graph algorithms implemented for the DAA project."""
import heapq
import math


def dijkstra(graph, source, target):
    """Return (distance, path) between source and target using non-negative weights."""
    if source not in graph or target not in graph:
        return math.inf, []
    distances = {node: math.inf for node in graph.nodes()}
    previous = {}
    distances[source] = 0
    queue = [(0, source)]
    while queue:
        current_distance, node = heapq.heappop(queue)
        if current_distance != distances[node]:
            continue
        if node == target:
            break
        for neighbor, data in graph[node].items():
            weight = float(data.get("weight", 1))
            if weight < 0:
                raise ValueError("Dijkstra's algorithm requires non-negative weights.")
            candidate = current_distance + weight
            if candidate < distances[neighbor]:
                distances[neighbor] = candidate
                previous[neighbor] = node
                heapq.heappush(queue, (candidate, neighbor))
    if math.isinf(distances[target]):
        return math.inf, []
    path, current = [], target
    while current != source:
        path.append(current)
        current = previous[current]
    path.append(source)
    path.reverse()
    return distances[target], path


def floyd_warshall(graph):
    """Return a nested dict of all-pairs shortest distances."""
    nodes = list(graph.nodes())
    dist = {u: {v: math.inf for v in nodes} for u in nodes}
    for u in nodes:
        dist[u][u] = 0
    for u, v, data in graph.edges(data=True):
        weight = float(data.get("weight", 1))
        if weight < 0:
            raise ValueError("This project expects non-negative edge weights.")
        dist[u][v] = min(dist[u][v], weight)
        dist[v][u] = min(dist[v][u], weight)
    for k in nodes:
        for i in nodes:
            if math.isinf(dist[i][k]):
                continue
            for j in nodes:
                candidate = dist[i][k] + dist[k][j]
                if candidate < dist[i][j]:
                    dist[i][j] = candidate
    return dist


def kruskal_mst(graph):
    """Return (selected_edges, total_weight) using Kruskal and disjoint sets."""
    parent = {node: node for node in graph.nodes()}
    rank = {node: 0 for node in graph.nodes()}

    def find(node):
        while parent[node] != node:
            parent[node] = parent[parent[node]]
            node = parent[node]
        return node

    def union(a, b):
        root_a, root_b = find(a), find(b)
        if root_a == root_b:
            return False
        if rank[root_a] < rank[root_b]:
            parent[root_a] = root_b
        elif rank[root_a] > rank[root_b]:
            parent[root_b] = root_a
        else:
            parent[root_b] = root_a
            rank[root_a] += 1
        return True

    edges = sorted(
        [(float(data.get("weight", 1)), u, v) for u, v, data in graph.edges(data=True)],
        key=lambda item: item[0],
    )
    selected, total = [], 0.0
    for weight, u, v in edges:
        if union(u, v):
            selected.append((u, v, weight))
            total += weight
    return selected, total
