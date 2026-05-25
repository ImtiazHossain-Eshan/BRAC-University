input_num = open("input1.txt", "r")
output_num = open("output1_1.txt","w")

length,target= [int(i) for i in input_num.readline().split()]
lst = [int(i) for i in input_num.readline().split()]

def lst_sum(length,target,lst):
  for i in range(length):
    for j in range(i+1,length):
      if lst[i]+lst[j] == target:
        return i+1,j+1
  return "Impossible"
sol=lst_sum(length,target,lst)
if type(sol)==str:
  output_num.write(f"{sol}")
else:
  output_num.write(f"{sol[0]} {sol[1]}")
output_num.close()