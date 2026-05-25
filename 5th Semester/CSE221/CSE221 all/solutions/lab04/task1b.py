input_file = open("input1b.txt",'r')
output_file = open("output1b.txt","w")

vertices, edges = [int(i) for i in input_file.readline().split()]
adj_list= {}
for i in range(vertices+1):
    adj_list[i] = [] 

for i in range(edges):
    source, destination, weight = [int(k) for k in input_file.readline().split()]
    adj_list[source].append((destination,weight))

output_file.write(f"{adj_list}")