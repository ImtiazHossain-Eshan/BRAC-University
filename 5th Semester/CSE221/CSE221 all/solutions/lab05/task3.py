from queue import LifoQueue
input_file = open("input3.txt","r")
output_file = open("output3.txt","w")

nodes, edges = [int(i) for i in input_file.readline().split()]

def dfs(node,adj_list,visited,component=None):
    visited[node]=True
    if component!=None:
        component.append(str(node))
    for i in adj_list[node]:
        if not visited[i]:
            dfs(i,adj_list,visited,component)
    stack.put(node)
    return component
adj_list={}
reverse_adj_list = {}
for i in range(1,nodes+1):
    adj_list[i] = []
    reverse_adj_list[i] = []
for i in range(edges):
    source, destination = [int(i) for i in input_file.readline().split()]
    adj_list[source].append(destination)
    reverse_adj_list[destination].append(source)

visited = {}
reverse_visted={}
for i in adj_list.keys():
    visited[i] = False
    reverse_visted[i]=False

stack = LifoQueue()
for node in adj_list.keys():
    if not visited[node]:
        dfs(node,adj_list,visited)
result = []
while not stack.empty():
    component=[]
    node = stack.get()
    if not reverse_visted[node]:
        dfs(node,reverse_adj_list,reverse_visted,component)
        result.append(component)
        component=[]
for i in result:
    x = " ".join(i)
    output_file.write(f"{x}\n")