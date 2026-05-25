from queue import Queue
input_file = open("input5.txt",'r')
output_file = open("output5.txt","w")

vertices, edges, end = [int(i) for i in input_file.readline().split()]
adj_list= {}
for i in range(1,vertices+1):
    adj_list[i] = [] 

for i in range(edges):
    source, destination= [int(k) for k in input_file.readline().split()]
    adj_list[source].append((destination))

visited = {}
bfs_result = []
level = {}
parent = {}
q = Queue()

for node in adj_list.keys():
    visited[node] = False
    parent[node] = None
    level[node] = -1

source = list(adj_list)[0]
q.put(source)
visited[source] = True
level[source] = 0

while not q.empty():
    temp = q.get()
    bfs_result.append(temp)

    for node in adj_list[temp]:
        if not visited[node]:
            visited[node] = True
            parent[node] = temp
            level[node] = level[temp]+1
            q.put(node)

path = []
time = level[end]
while end is not None:
    path.append(end)
    end = parent[end]

output_file.write(f"Time: {time}\n")
output_file.write(f"Shortest Path: ")
for i in range(len(path)-1,-1,-1):
    output_file.write(f"{path[i]} ")