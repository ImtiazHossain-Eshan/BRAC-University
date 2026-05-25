def merge(arr, temp, left, mid, right):
    i = left
    j = mid + 1
    count = 0
    for k in range(left, right + 1):
        if i > mid:
            temp[k] = arr[j]
            j += 1
        elif j > right:
            temp[k] = arr[i]
            i += 1
        elif arr[i] <= arr[j]:
            temp[k] = arr[i]
            i += 1
        else:
            temp[k] = arr[j]
            j += 1
            count += (mid - i + 1)
    for k in range(left, right + 1):
        arr[k] = temp[k]
    return count
def divide_count(arr, temp, left, right):
    count = 0
    if left < right:
        mid = (left + right) // 2
        count += divide_count(arr, temp, left, mid)
        count += divide_count(arr, temp, mid + 1, right)
        count += merge(arr, temp, left, mid, right)
    return count

input_file = open("input3.txt","r")
output_file = open("output3.txt","w")
length = int(input_file.readline())
arr= [int(i) for i in input_file.readline().split()]
temp = [0] * length
result = divide_count(arr, temp, 0, length - 1)
output_file.write(f'{result}')