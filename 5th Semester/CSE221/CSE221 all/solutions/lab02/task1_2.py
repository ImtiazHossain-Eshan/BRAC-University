input_num = open("input1.txt", "r")
output_num = open("output1_2.txt","w")

length,target= [int(i) for i in input_num.readline().split()]
lst = [int(i) for i in input_num.readline().split()]

def lst_sum(length,target,lst):
  left = 0
  right = length-1
  while left < right:
    counted_sum=lst[left]+lst[right]
    if counted_sum > target:
      right -= 1
    elif counted_sum<target:
      left += 1
    elif counted_sum == target:
      return left+1, right+1
  return "Impossible"
sol=lst_sum(length,target,lst)
if type(sol)==str:
  output_num.write(f"{sol}")
else:
  output_num.write(f"{sol[0]} {sol[1]}")
output_num.close()