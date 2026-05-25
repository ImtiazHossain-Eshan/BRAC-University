import heapq

def dijkstra(graph, source):
    distances = {node: float('inf') for node in graph}
    distances[source] = 0
    heap = [(0, source)]

    while heap:
        current_distance, current_node = heapq.heappop(heap)

        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(heap, (distance, neighbor))

    return distances


input_file = open("input1.txt", "r")
output_file = open("output1.txt", "w")
N, M = map(int, input_file.readline().split())
graph = {i: {} for i in range(1, N + 1)}

for i in range(M):
    u, v, w = map(int, input_file.readline().split())
    if v not in graph[u]:
        graph[u][v] = w

source = int(input_file.readline())

distances = dijkstra(graph, source)

for i in range(1, N + 1):
    if distances[i] == float('inf'):
        output_file.write("-1 ")
    else:
        output_file.write(str(distances[i]) + " ")