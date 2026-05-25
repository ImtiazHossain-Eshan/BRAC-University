from queue import Queue

input_file = open("input2.txt",'r')
output_file = open("output2.txt","w")
vertices, edges = [int(i) for i in input_file.readline().split()]
adj_list= {}
for i in range(1,vertices+1):
    adj_list[i] = [] 

for i in range(edges):
    source, destination= [int(k) for k in input_file.readline().split()]
    adj_list[source].append((destination))

visited = {}
bfs_result = []
q = Queue()

for node in adj_list.keys():
    visited[node] = False

source = list(adj_list)[0]
q.put(source)
visited[source] = True

while not q.empty():
    temp = q.get()
    bfs_result.append(temp)

    for node in adj_list[temp]:
        if not visited[node]:
            visited[node] = True
            q.put(node)

for elem in bfs_result:
    output_file.write(f"{elem} ")