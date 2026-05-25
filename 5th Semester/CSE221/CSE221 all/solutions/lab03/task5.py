def partition(arr,low,high):
    pivot = arr[low]
    i = low
    for j in range(i+1,high):
        if arr[j] < pivot:
            i += 1
            arr[i],arr[j] = arr[j],arr[i]
    arr[i] , arr[low] = pivot , arr[i]
    return i
def quick_sort(arr,low,high):
    if low < high:
        p = partition(arr,low,high)
        quick_sort(arr,low,p)
        quick_sort(arr,p+1,high)

input_file = open("input5.txt","r")
output_file = open("output5.txt","w")
length = int(input_file.readline())
arr = [int(i) for i in input_file.readline().split()]
result = quick_sort(arr, 0, length)
for i in arr:
    output_file.write(f'{i} ')