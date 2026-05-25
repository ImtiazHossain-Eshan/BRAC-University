inp2 = open("input2.txt","r")
out2_2 = open("output2_2.txt","w")

length_1 = int(inp2.readline())
lst_1 = [int(i) for i in inp2.readline().split()]
length_2 = int(inp2.readline())
lst_2 = [int(i) for i in inp2.readline().split()]


l1=0
l2=0
out_list=[]

# while l1<length_1 and l2<length_2:
#   if lst_1[l1] < lst_2[l2]:
#     out_list.append(lst_1[l1])
#     l1+=1
#   elif lst_2[l2] < lst_1[l1]:
#     out_list.append(lst_2[l2])
#     l2+=1
#   else:
#     out_list.append(lst_1[l1])
#     out_list.append(lst_2[l2])
#     l1+=1
#     l2+=1

# while l1<length_1:
#   out_list.append(lst_1[l1])
#   l1+=1

# while l2<length_2:
#   out_list.append(lst_2[l2])
#   l2+=1

while l1!=(length_1) or l2!=(length_2):
  if l1==length_1 and l2<length_2:
    out_list.append(lst_2[l2])
    if l2<length_2:
      l2+=1
  elif l1<length_1 and l2==length_2:
    out_list.append(lst_1[l1])
    if l1<length_1:
      l1+=1
  else:
    if lst_1[l1]<lst_2[l2]:
      out_list.append(lst_1[l1])
      l1+=1
    elif lst_2[l2]<lst_1[l1]:
      out_list.append(lst_2[l2])
      l2+=1
    else:
      out_list.append(lst_1[l1])
      out_list.append(lst_2[l2])
      l1+=1
      l2+=1
for i in out_list:
  out2_2.write(f"{i} ")
# print(f"{" ".join(out_list)}")
# out2_2.write(f"{" ".join(out_list)}")
out2_2.close()