inp2 = open("input2.txt","r")
out2_1 = open("output2_1.txt","w")

length_1 = int(inp2.readline())
lst_1 = [int(i) for i in inp2.readline().split()]
length_2 = int(inp2.readline())
lst_2 = [int(i) for i in inp2.readline().split()]

for i in lst_2:
  lst_1.append(i)
lst_1.sort()
for i in lst_1:
  out2_1.write(f"{i} ")