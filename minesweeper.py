import random
import math
import tkinter as tk

## LOGIC ########################

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

    #set 2s to 1s
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
    if grid[x][y] == -1:
        print("BOOM!")

def FlagTile(x, y):
    if gridMask[x][y] == 0:
        gridMask[x][y] = -1
    elif gridMask[x][y] == -1:
        gridMask[x][y] == 0

## INTERACTION ##################

def KeyPress(key):

    if key.keycode == 87 or key.keycode == 38: #w, uparrow
        movement[0] = 1
    if key.keycode == 65 or key.keycode == 37: #a, leftarrow
        movement[1] = 1
    if key.keycode == 83 or key.keycode == 40: #s, downarrow
        movement[2] = 1
    if key.keycode == 68 or key.keycode == 39: #d, rightarrow
        movement[3] = 1

    if key.keycode == 13: #enter
        global playing
        print("SWEEP")

        crds = canvas.coords(cursor)
        x = math.floor(crds[1] / 80)
        y = math.floor(crds[0] / 80)
        canvas.delete(tileGrid[x][y])
        if playing:
            SweepTile(x, y)
        else:
            GenerateGrid(x, y)
            DisplayGrid()
            playing = True
    if key.keycode == 8: #backspace
        print("FLAG")

        crds = canvas.coords(cursor)
        x = math.floor(crds[1] / 80)
        y = math.floor(crds[0] / 80)
        canvas.itemconfig(tileGrid[x][y], image=flag)
        FlagTile(x, y)

    Move()

def KeyRelease(key):

    if key.keycode == 87 or key.keycode == 38:
        movement[0] = 0
    if key.keycode == 65 or key.keycode == 37:
        movement[1] = 0
    if key.keycode == 83 or key.keycode == 40:
        movement[2] = 0
    if key.keycode == 68 or key.keycode == 39:
        movement[3] = 0

def Move():
    crds = canvas.coords(cursor)
    x = crds[0] + 8 * (movement[3] - movement[1])
    y = crds[1] + 8 * (movement[2] - movement[0])
    canvas.coords(cursor, x, y)

## INTERFACE ####################

def DisplayGrid():
    
    for r in range(l):
        for c in range(l):
            #grid
            if gridMask[r][c] == 0:
                canvas.create_text(41 + c*80, 41 + r*80, text="?")
            elif gridMask[r][c] == -1:
                canvas.create_text(41 + c*80, 41 + r*80, text="!")
            else:
                if grid[r][c] == -1:
                    canvas.create_text(41 + c*80, 41 + r*80, text="X")
                else:
                    canvas.create_text(41 + c*80, 41 + r*80, text=str(grid[r][c]))

            #gridmask
            if gridMask[r][c] == 1:
                canvas.delete(tileGrid[r][c])

window = tk.Tk()
window.title = "Minesweeper"
window.geometry("640x640")

tile = tk.PhotoImage(file="tile.png")
flag = tk.PhotoImage(file="flag.png")
crss = tk.PhotoImage(file="crosshair.png")

canvas = tk.Canvas(window, width=640, height=640)

tileGrid = [[None for c in range(8)] for r in range(8)]
for r in range(8):
    for c in range(8):
        tileGrid[r][c] = canvas.create_image(41 + c*80, 41 + r*80, image=tile)

movement = [0, 0, 0, 0,]

window.bind("<KeyPress>", KeyPress)
window.bind("<KeyRelease>", KeyRelease)

canvas.pack()
cursor = canvas.create_image(320, 320, image=crss)

## MAIN #########################        

#l = int(input("Dimension of Grid: "))
l = 8
grid = [[0 for i in range(l)] for i in range(l)] #holds locations of bombs and number indicators
gridMask = [[0 for i in range(l)] for i in range(l)] #stores which tiles are 'visible' to the user 
numberOfBombs = int(l*l / 8)

playing = False

temp = canvas.create_text(40, 40, text="test")
canvas.tag_lower(temp)

window.mainloop()