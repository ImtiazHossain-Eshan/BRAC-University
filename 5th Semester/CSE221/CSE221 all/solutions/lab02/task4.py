input_file = open("input4.txt", "r")
output_file = open("output4.txt","w")

length, member = [int(i) for i in input_file.readline().split()]
info= []
for i in range(length):
    start, end = [int(i) for i in input_file.readline().split()]
    info.append((start, end))

sorted_info = sorted(info,key = lambda x:x[1])
job_count= member
member_info=[0]*member
for i in range(0, member):
    member_info[i] = sorted_info[i][1]

for j in range(member, length):
    start_time, end_time = sorted_info[j][0], sorted_info[j][1]
    for k in range(len(member_info)-1,-1,-1):
        if start_time >= member_info[k]:
            member_info[k]=end_time
            job_count +=1
            break
output_file.write(f"{job_count}")
output_file.close()