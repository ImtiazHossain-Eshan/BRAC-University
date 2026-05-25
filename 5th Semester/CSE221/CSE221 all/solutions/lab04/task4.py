input_file = open("input4.txt",'r')
output_file = open("output4.txt","w")
vertices, edges = [int(i) for i in input_file.readline().split()]
adj_list= {}
for i in range(1,vertices+1):
    adj_list[i] = []

for i in range(edges):
    source, destination= [int(k) for k in input_file.readline().split()]
    adj_list[source].append((destination))

color = {}
start = list(adj_list)[0]
has_cycle = False

for node in adj_list.keys():
    color[node] = "W"

def dfs(source):
    global has_cycle
    color[source] = "G"
    for node in adj_list[source]:
        if color[node]=="W":
            dfs(node)
        elif color[node] == "G":
            has_cycle = True
            break
    color[source]="B"
dfs(start)
output_file.write(f"{has_cycle}")