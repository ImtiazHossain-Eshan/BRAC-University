input_file = open("input1a.txt","r")
output_file = open("output1a.txt","w")

num_count =  int(input_file.readline())
for i in range(num_count):
    number = int(input_file.readline())
    if number % 2 == 0:
        output_file.write(f"{number} is an Even number\n")
    else:
        output_file.write(f"{number} is an Odd number\n")
input_file.close()
output_file.close()