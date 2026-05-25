input_file = open("input3.txt","r")
output_file = open("output3.txt","w")

length = int(input_file.readline())
ids = [int(i) for i in input_file.readline().split()]
marks = [int(i) for i in input_file.readline().split()]
# print(length, ids, marks)

for i in range(length):
    max_idx = i
    for j in range(i+1,length):
        if marks[max_idx] < marks[j] or ((marks[j]==marks[max_idx] and ids[j]<ids[max_idx])):
            max_idx = j
    marks[i],marks[max_idx] = marks[max_idx],marks[i]
    ids[i],ids[max_idx] = ids[max_idx],ids[i]

for i in range(length):
    output_file.write(f"ID: {ids[i]} Mark: {marks[i]}\n")

output_file.close()