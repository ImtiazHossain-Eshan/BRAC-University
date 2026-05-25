input_file = open("input1.txt","r")
output_file = open("output1.txt", "w")

nodes, queries = map(int, input_file.readline().split())
parent = [i for i in range(nodes+1)]
size = [1]*(nodes+1)
def find(node):
    if parent[node] == node:
        return node
    return find(parent[node])
def union(u,v):
    u_parent = find(u)
    v_parent = find(v)
    if u_parent != v_parent:
        if size[u_parent] < size[v_parent]:
            u_parent, v_parent= v_parent, u_parent
        parent[v_parent] = u_parent
        size[u_parent] += size[v_parent]
        return size[u_parent]
    return size[u_parent]
for i in range(queries):
    u, v = map(int, input_file.readline().split())
    output_file.write(f"{union(u,v)}\n")