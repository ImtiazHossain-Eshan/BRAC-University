input_file = open("input3.txt","r")
output_file = open("output3.txt", "w")
n=int(input_file.readline())

history = {0:0,1:1,2:2}
def frogClimber(n):
    if n in history:
        return history[n]
    history[n]=frogClimber(n-1)+frogClimber(n-2)
    return history[n]
output_file.write(f"{frogClimber(n)}")