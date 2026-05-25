input_file = open("input6.txt",'r')
output_file = open("output6.txt","w")
maze = []
row, column = [int(i) for i in input_file.readline().split()]
for i in range(row):
    line = input_file.readline().strip()
    maze.append(line)

def dfs(x,y):
    global diamond_count
    if x<0 or x>=row or y<0 or y>=column or maze[x][y] == "#" or visited[x][y]:
        return
    
    visited[x][y]=True
    if maze[x][y] == "D":
        diamond_count += 1
    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        dfs(x + dx, y + dy)
    
max_diamond_count= 0
visited = [[False] * column for i in range(row)]

for i in range(row):
    for j in range(column):
        if maze[i][j]== '.' and not visited[i][j]:
            diamond_count= 0
            dfs(i, j)
            max_diamond_count= max(max_diamond_count, diamond_count)

output_file.write(str(max_diamond_count))