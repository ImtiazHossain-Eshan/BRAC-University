import heapq

def dijkstra(graph, start):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    heap = [(0, start)]

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

def find_meeting_point(graph, alice_start, bob_start):
    alice_distances = dijkstra(graph, alice_start)
    bob_distances = dijkstra(graph, bob_start)

    max_min_time = -1
    meeting_point = None

    for node in graph:
        if alice_distances[node] != float('inf') and bob_distances[node] != float('inf'):
            min_time = max(alice_distances[node], bob_distances[node])
            if min_time > max_min_time:
                max_min_time = min_time
                meeting_point = node

    return max_min_time, meeting_point

input_file = open("input2.txt", "r")
output_file = open("output2.txt", "w")
N, M = map(int, input_file.readline().split())
graph = {i: {} for i in range(1, N + 1)}

for i in range(M):
    u, v, w = map(int, input_file.readline().split())
    if v not in graph[u]:
        graph[u][v] = w

alice_start, bob_start = map(int, input_file.readline().split())

min_time, meeting_point = find_meeting_point(graph, alice_start, bob_start)


if meeting_point:
    output_file.write(f"Time {min_time}\n")
    output_file.write(f"Node {meeting_point}")
else:
    output_file.write("Impossible")
