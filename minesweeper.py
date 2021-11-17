import random

def GenerateGrid(inputX, inputY):
    gridMask[inputX][inputY] = 1

    #PLACE BOMBS
    counter = 0
    while counter < numberOfBombs:
        x = random.randint(0, l-1)
        y = random.randint(0, l-1)
        if gridMask[x][y] == 0: #ensure tile is not starting tile, or already a bomb
            grid[x][y] = -1
            counter += 1

    print('bombs placed')

    #SET NUMBER INDICATORS
    for x in range(l):
        for y in range(l):
            
            if grid[x][y] == -1: #if tile is bomb

                #update numbers of surronding tiles
                for deltaX in range(-1, 2):
                    if x + deltaX > l-1 or x + deltaX < 0:
                        continue
                    for deltaY in range(-1, 2):
                        if y + deltaY > l-1 or y + deltaY < 0:
                            continue

                        if grid[x + deltaX][y + deltaY] > -1: #if tile not a bomb
                            grid[x + deltaX][y + deltaY] += 1

    print('numbers set')

    #CREATE START AREA
    #set ring around start area as 2s
    for deltaX in range(-1, 2):
        if inputX + deltaX > l-1 or inputX + deltaX < 0:
            continue
        for deltaY in range(-1, 2):
            if inputY + deltaY > l-1 or inputY + deltaY < 0:
                continue

            if deltaX == 0 and deltaY == 0: #if starting co-ords
                continue

            gridMask[inputX + deltaX][inputY + deltaY] = 2

    print('2 ring')
    
    #set blanks as 1s
    flag = True
    while flag:
        flag = False

        #search playergrid for 2s
        for x in range(l):
            for y in range(l):

                if gridMask[x][y] == 2:
                    if grid[x][y] == 0:
                        gridMask[x][y] = 1
                        flag = True

                        if y > 0:
                            if gridMask[x][y-1] == 0:
                                gridMask[x][y-1] = 2
                        if x < l-1:
                            if gridMask[x+1][y] == 0:
                                gridMask[x+1][y] = 2
                        if y < l-1:
                            if gridMask[x][y+1] == 0:
                                gridMask[x][y+1] = 2
                        if x > 0:
                            if gridMask[x-1][y] == 0:
                                gridMask[x-1][y] = 2
    
    print('blanks set to 1')

    #set numbers as 1
    flag = True 
    while flag:
        flag = False

        for x in range(l):
            for y in range(l):

                if gridMask[x][y] == 2:
                    if grid[x][y] > -1:
                        gridMask[x][y] = 1
                    else:
                        gridMask[x][y] = 0
                    flag = True

    print('done')

def SweepTile(x, y):
    gridMask[x][y] = 1

def FlagTile(x, y):
    if gridMask[x][y] == 0:
        gridMask[x][y] = -1
    elif gridMask[x][y] == -1:
        gridMask[x][y] == 0

def DisplayGrid():
    temp = '    '
    for i in range(l):
        temp += str(i) + ' '
    print(temp)
    temp = '   --' + '--'*l
    print(temp)

    for r in range(l):
        temp = str(r) + ' |'
        for c in range(l):
            if gridMask[r][c] == 0:
                temp += ' ?'
            elif gridMask[r][c] == -1:
                temp += ' !'
            else:
                if grid[r][c] == 0:
                    temp += '  '
                elif grid[r][c] == -1:
                    temp += ' X'
                else:
                    temp += ' ' + str(grid[r][c])
        print(temp)
                    
l = int(input("Dimension of Grid: "))
grid = [[0 for i in range(l)] for i in range(l)] #holds locations of bombs and number indicators
gridMask = [[0 for i in range(l)] for i in range(l)] #stores which tiles are 'visible' to the user 
numberOfBombs = l*l / 8

GenerateGrid(4, 4)
while True:
    print("\n")
    DisplayGrid()
    print("\n[! or ?] [x] [y], (! for flag, ? for sweep)")
    inp = input().split()
    if inp[0] == '!':
        FlagTile(int(inp[2]), int(inp[1]))
    elif inp[0] == '?':
        SweepTile(int(inp[2]), int(inp[1]))