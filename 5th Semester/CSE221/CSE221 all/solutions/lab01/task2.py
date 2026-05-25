input_file = open("input2.txt","r")
output_file = open("output2.txt","w")

length = int(input_file.readline())
arr = [int(i) for i in input_file.readline().split()]

def bubbleSort(arr):                                                    
    for i in range(len(arr)-1):
        flag = False
        for j in range(len(arr)-i-1): 
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                flag = True
        if flag == True:
            break
    return arr

for i in (bubbleSort(arr)):
    output_file.write(f'{i} ')
output_file.close()