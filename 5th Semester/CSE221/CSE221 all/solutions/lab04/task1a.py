import numpy as np
input_file = open("input1a.txt",'r')
output_file = open("output1a.txt","w")

vertices, edges = [int(i) for i in input_file.readline().split()]
adj_mat = np.zeros((vertices+1,vertices+1),dtype=int)

for i in range(edges):
    row, col ,val = [int(i) for i in input_file.readline().split()]
    adj_mat[row][col] = val

output_file.write(f"{adj_mat}")