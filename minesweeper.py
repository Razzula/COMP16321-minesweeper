import random

grid = [[0 for i in range(8)] for i in range(8)]
playerGrid = [[0 for i in range(8)] for i in range(8)]

numberOfBombs = 8

def GenerateGrid(inputX, inputY):
    playerGrid[inputX][inputY] = 1

    #PLACE BOMBS
    counter = 0
    while counter < numberOfBombs:
        x = random.randint(0, 7)
        y = random.randint(0, 7)
        if playerGrid[x][y] == 0: #ensure tile is not starting tile, or already a bomb
            grid[x][y] = -1
            counter += 1

    print('bombs placed')

    #SET NUMBER INDICATORS
    for x in range(8):
        for y in range(8):
            
            if grid[x][y] == -1: #if tile is bomb

                #update numbers of surronding tiles
                for deltaX in range(-1, 2):
                    if x + deltaX > 7 or x + deltaX < 0:
                        continue
                    for deltaY in range(-1, 2):
                        if y + deltaY > 7 or y + deltaY < 0:
                            continue

                        if grid[x + deltaX][y + deltaY] > -1: #if tile not a bomb
                            grid[x + deltaX][y + deltaY] += 1

    print('numbers set')

    #CREATE START AREA
    #set ring around start area as 2s
    for deltaX in range(-1, 2):
        if inputX + deltaX > 7 or inputX + deltaX < 0:
            continue
        for deltaY in range(-1, 2):
            if inputY + deltaY > 7 or inputY + deltaY < 0:
                continue

            if deltaX == 0 and deltaY == 0: #if starting co-ords
                continue

            playerGrid[inputX + deltaX][inputY + deltaY] = 2

    print('2 ring')
    
    #set blanks as 1s
    flag = True
    while flag:
        flag = False

        #search playergrid for 2s
        for x in range(8):
            for y in range(8):

                if playerGrid[x][y] == 2:
                    if grid[x][y] == 0:
                        playerGrid[x][y] = 1
                        flag = True

                        if y > 0:
                            if playerGrid[x][y-1] == 0:
                                playerGrid[x][y-1] = 2
                        if x < 7:
                            if playerGrid[x+1][y] == 0:
                                playerGrid[x+1][y] = 2
                        if y < 7:
                            if playerGrid[x][y+1] == 0:
                                playerGrid[x][y+1] = 2
                        if x > 0:
                            if playerGrid[x-1][y] == 0:
                                playerGrid[x-1][y] = 2
    
    print('blanks set to 1')

    #set numbers as 1
    flag = True 
    while flag:
        flag = False

        for x in range(8):
            for y in range(8):

                if playerGrid[x][y] == 2:
                    if grid[x][y] > -1:
                        playerGrid[x][y] = 1
                    else:
                        playerGrid[x][y] = 0
                    flag = True

    print('done')

def SweepTile(x, y):
    playerGrid[x][y] = 1

def FlagTile(x, y):
    playerGrid[x][y] = -1

def DisplayGrid():
    print('     0 1 2 3 4 5 6 7')
    print('   -----------------')
    for r in range(8):
        temp = str(r) + ' |'
        for c in range(8):
            if playerGrid[r][c] == 0:
                temp += ' ?'
            elif playerGrid[r][c] == -1:
                temp += ' !'
            else:
                if grid[r][c] == 0:
                    temp += '  '
                elif grid[r][c] == -1:
                    temp += ' X'
                else:
                    temp += ' ' + str(grid[r][c])
        print(temp)
                    

GenerateGrid(4, 4)
while True:
    print("\n")
    DisplayGrid()
    inp = input().split()
    if inp[0] == '!':
        FlagTile(int(inp[2]), int(inp[1]))
    elif inp[0] == '?':
        SweepTile(int(inp[2]), int(inp[1]))