print("This is a pyramid program, please tellme how many levels for your piramid")

m:int=int(input())

#1      *       1  
#2     ***      3
#3    *****     5
#4   *******    7

#dots(m) = n_(m-1)+2

# m=2n-1  

width=2*m-1
grid=[["-" for _ in range(width)] for _ in range(m)]


change=m-1
grid[0][change]="*"

for i in range(1,m):
    change-=1
    end=change+2*(i)
    
    for j in range(change,end+1):
        grid[i][j]="*"
    
    
for y in range(m):
    print("".join(grid[y]))
    
for y in range(m):
    print(grid[y])    
