input_file = open("input3.txt",'r')
output_file = open("output3.txt","w")
vertices, edges = [int(i) for i in input_file.readline().split()]
adj_list= {}
for i in range(1,vertices+1):
    adj_list[i] = []

for i in range(edges):
    source, destination= [int(k) for k in input_file.readline().split()]
    adj_list[source].append((destination))

color = {}
start = list(adj_list)[0]
traversal_result = []
for node in adj_list.keys():
    color[node] = "W"

def dfs(source):
    color[source] = "G"
    traversal_result.append(source)
    for node in adj_list[source]:
        if color[node]=="W":
            dfs(node)
    color[source]="B"
dfs(start)

for elem in traversal_result:
    output_file.write(f"{elem} ")
    