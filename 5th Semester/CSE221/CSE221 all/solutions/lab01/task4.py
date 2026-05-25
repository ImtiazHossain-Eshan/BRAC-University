input_file = open("input4.txt","r")
output_file = open("output4.txt","w")

length = int(input_file.readline())
name, location, time = [], [], []

for i in range(length):
    info = input_file.readline().split()
    # print(info)
    name.append(info[0])
    location.append(info[4])
    time.append(info[6])
# print(name,location,time)

# if "ABCD" > "ABC":
#     print(True)

for i in range(length):
    min_idx=i
    for j in range(i,length):
        if name[min_idx]>name[j] or (name[j]==name[min_idx] and time[min_idx]<time[j]):
            min_idx=j
    name[i],name[min_idx] = name[min_idx],name[i]
    location[i],location[min_idx] = location[min_idx],location[i]
    time[i],time[min_idx] = time[min_idx],time[i]

for i in range(length):
    output_file.write(f'{name[i]} will departure for {location[i]} at {time[i]}\n')

output_file.close()