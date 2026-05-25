import heapq

def dijkstra(graph, start, end):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    heap = [(0, start)]

    while heap:
        current_danger, current_node = heapq.heappop(heap)

        if current_node == end:
            return current_danger

        for neighbor, danger in graph[current_node].items():
            max_danger = max(current_danger, danger)
            if max_danger < distances[neighbor]:
                distances[neighbor] = max_danger
                heapq.heappush(heap, (max_danger, neighbor))

    return -1

input_file = open("input2.txt", "r")
output_file = open("output2.txt", "w")
N, M = map(int, input_file.readline().split())
graph = {i: {} for i in range(1, N + 1)}

for i in range(M):
    u, v, w = map(int, input_file.readline().split())
    if v not in graph[u]:
        graph[u][v] = w
destination = N

min_danger = dijkstra(graph, 1, destination)

if min_danger != -1:
    output_file.write(str(min_danger))
else:
    output_file.write("Impossible")