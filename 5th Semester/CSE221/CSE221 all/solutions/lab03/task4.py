def max_possible(arr,var=0):
    mid=len(arr) // 2
    i=0
    list1=[]
    if len(arr)==1:
        return arr,var
    if len(arr)>1 and len(arr)<=2:
        temp=arr[0] + pow(arr[1], 2)
        if temp>=var:
            var=temp
        return arr,var
    left_arr=arr[:mid]
    right_arr=arr[mid:]
    l1,left_max = max_possible(left_arr,var)
    r1,right_max = max_possible(right_arr,var)
    if right_max>=left_max:
        var=right_max
    else:
        var=left_max
    high=max(l1)
    while i<len(r1):
        if var<=high+pow(r1[i],2):
            var=high+pow(r1[i],2)
        i+=1
    list1.extend(l1)
    list1.extend(r1)
    return list1,var

input_file = open("input4.txt","r")
output_file = open("output4.txt","w")
length = int(input_file.readline())
arr= [int(i) for i in input_file.readline().split()]
output_file.write(f'{str(max_possible(arr)[1])}')