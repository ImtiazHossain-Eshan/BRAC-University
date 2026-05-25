from queue import Queue
input_file = open("input1b.txt","r")
output_file = open("output1b.txt","w")

nodes, edges = [int(i) for i in input_file.readline().split()]
adj_list={}
degree_info={}
result = []

for i in range(1,nodes+1):
    adj_list[i] = []
    degree_info[i] = 0

for i in range(edges):
    source, destination = [int(i) for i in input_file.readline().split()]
    degree_info[destination] += 1
    adj_list[source].append(destination)

q = Queue()
for i in adj_list.keys():
    if degree_info[i]==0:
        q.put(i)

while not q.empty():
    temp = q.get()
    result.append(temp)
    for node in adj_list[temp]:
        degree_info[node]-=1
        if degree_info[node]==0:
            q.put(node)

if len(list(adj_list))!=len(result):
    output_file.write("Impossible")
else:
    for i in result:
        output_file.write(f"{i} ")
