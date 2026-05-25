def merge(a, b):        
    new_list=[]
    i, j = 0, 0
    while i<len(a) and j<len(b):
        if a[i]<b[j]:
            new_list.append(a[i])
            i+=1
        else:
            new_list.append(b[j])
            j+=1
    while i<len(a):
        new_list.append(a[i])
        i+=1
    while j<len(b):
        new_list.append(b[j])
        j+=1
    return new_list

def mergeSort(arr):
    if len(arr) <= 1:
        return arr
    else:
        mid = len(arr)//2
        a1 = mergeSort(arr[:mid]) 
        a2 = mergeSort(arr[mid:])
        return merge(a1, a2)
input_file = open("input1.txt","r")
output_file = open("output1.txt","w")
length = int(input_file.readline())
arr= [int(i) for i in input_file.readline().split()]
result=mergeSort(arr)
for i in result:
    output_file.write(f'{i} ')