import random

gridWorld = [[0 for x in range(101)] for y in range(101)]


# 3060

coordinates = []

while len(coordinates) < 3060:
    x = random.randint(0, 100)
    y = random.randint(0, 100)
    randCoord = (x, y)
    if randCoord not in coordinates:
        gridWorld[x][y] = 1
        coordinates.append(randCoord)

startX = random.randint(0, 100)
startY = random.randint(0, 100)
endX = random.randint(0, 100)
endY = random.randint(0, 100)

gridWorld[startX][startY] = 2
print(str(startX) + " " + str(startY))
gridWorld[endX][endY] = 3
print(str(endX) + " " + str(endY))

count = 0
for i in range(101):
    while count < 100:
        print(str(gridWorld[i][count]), end=' ')
        count = count + 1
    print(str(gridWorld[i][count]))
    count = 0





