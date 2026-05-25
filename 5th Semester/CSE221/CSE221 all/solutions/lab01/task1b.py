input_file = open("input1b.txt","r")
output_file = open("output1b.txt","w")

length =  int(input_file.readline())

for i in range(length):
    info = input_file.readline().split()
    operation = f"{info[1]} {info[2]} {info[3]}"
    if info[2] == "+":
        result = int(info[1])+int(info[3])
    elif info[2] == "-":
        result = int(info[1])-int(info[3])
    elif info[2] == "*":
        result = int(info[1])*int(info[3])
    elif info[2] == "/":
        result = int(info[1])/int(info[3])
    
    output_file.write(f"The result of {operation} is {result}\n")

output_file.close()