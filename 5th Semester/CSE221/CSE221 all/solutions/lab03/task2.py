def findMax(arr, p, q):
    if p==q:
        return arr[p]
    mid = (p + q) // 2
    left_max = findMax(arr,p,mid)
    right_max = findMax(arr,mid+1,q)
    if left_max>right_max:
        return left_max
    else:
        return right_max
input_file = open("input2.txt","r")
output_file = open("output2.txt","w")
length = int(input_file.readline())
arr= [int(i) for i in input_file.readline().split()]
result = findMax(arr,0,length-1)
output_file.write(f'{result}')