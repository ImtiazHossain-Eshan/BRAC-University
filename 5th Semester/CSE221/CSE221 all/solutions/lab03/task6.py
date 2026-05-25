def partition(arr,low,high):
    pivot = arr[low]
    i = low
    for j in range(i+1,high):
        if arr[j] < pivot:
            i += 1
            arr[i],arr[j] = arr[j],arr[i]
    arr[i] , arr[low] = pivot , arr[i]
    return i

def kth_smallest(arr,low,high,k):
    if low < high:
        p = partition(arr,low,high)
        if p == k :
            return p
        elif k < p:
            return  kth_smallest(arr,low,p,k)
        else:
            return  kth_smallest(arr,p+1,high,k)

input_file = open("input6.txt","r")
output_file = open("output6.txt","w")
length= int((input_file.readline()).split(" ")[0])
arr = [int(i) for i in input_file.readline().split()]
query = int((input_file.readline()).split(" ")[0])
for i in range(query):
    num = int(input_file.readline())
    result =  kth_smallest(arr, 0, length,num-1)
    output_file.write(f"{arr[result]}\n")