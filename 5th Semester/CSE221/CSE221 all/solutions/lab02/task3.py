input_file = open("input3.txt", "r")
output_file = open("output3.txt","w")

length = int(input_file.readline())
info= []
for i in range(length):
    start, end = [int(i) for i in input_file.readline().split()]
    info.append((start, end))

sorted_info = sorted(info,key = lambda x:x[1])

job_count = 1
job_list = []
current_start, current_end = sorted_info[0][0], sorted_info[0][1]
job_list.append((current_start,current_end))

for i in range(1,len(sorted_info)):
    if sorted_info[i][0] >= current_end:
        current_start, current_end = sorted_info[i][0], sorted_info[i][1]
        job_list.append((current_start,current_end))
        job_count += 1

output_file.write(f"{job_count}\n")
for i in job_list:
    output_file.write(f"{i[0]} {i[1]}\n")

output_file.close()