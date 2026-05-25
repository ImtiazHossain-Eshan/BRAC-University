from queue import LifoQueue
input_file = open("input1a.txt","r")
output_file = open("output1a.txt","w")

def dfs(node,adj_list,visited):
    visited[node]=True
    for i in adj_list[node]:
        if not visited[i]:
            dfs(i,adj_list,visited)
    stack.put(node)

nodes, edges = [int(i) for i in input_file.readline().split()]

adj_list={}
for i in range(1,nodes+1):
    adj_list[i] = []

for i in range(edges):
    source, destination = [int(i) for i in input_file.readline().split()]
    adj_list[source].append(destination)

visited = {}
for i in adj_list.keys():
    visited[i] = False

stack = LifoQueue()
for node in adj_list.keys():
    if not visited[node]:
        dfs(node,adj_list,visited)

if stack.qsize()!=len(list(visited)):
    output_file.write("Impossible")
else:
    while not stack.empty():
        out = stack.get()
        output_file.write(f"{out} ")