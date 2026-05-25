import heapq
input_file = open("input2.txt","r")
output_file = open("output2.txt","w")

nodes, edges = map(int, input_file.readline().split())
adj_list={i:[] for i in range(1,nodes+1)}
visited = {i: False for i in range(1, nodes+1)}
start= list(adj_list)[0]
for i in range(edges):
    u,v,w = map(int, input_file.readline().split())
    adj_list[u].append((v,w))
    adj_list[v].append((u, w))
min_heap = [(0, start)]
total_weight = 0
while min_heap:
    weight, node = heapq.heappop(min_heap)
    if visited[node]:
        continue
    visited[node] = True
    total_weight += weight
    for neighbor, edge_weight in adj_list[node]:
        if not visited[neighbor]:
            heapq.heappush(min_heap, (edge_weight, neighbor))

output_file.write(str(total_weight))
input_file.close()
output_file.close()