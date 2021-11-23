import random
import math
import tkinter as tk
from tkinter.font import BOLD

## LOGIC ########################

def GenerateGrid(inputX, inputY):
    gridMask[inputX][inputY] = 1

    #PLACE BOMBS
    counter = 0
    while counter < numberOfBombs:
        x = random.randint(0, l-1)
        y = random.randint(0, l-1)
        if gridMask[x][y] == 0 and grid[x][y] == 0: #ensure tile is not starting tile, or already a bomb
            grid[x][y] = -1
            counter += 1
    removals = 1

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
                        removals += 1
                        flag = True

                        for deltaX in range(-1, 2):
                            if x + deltaX < 0 or x + deltaX >= l:
                                continue
                            for deltaY in range(-1, 2):
                                if y + deltaY < 0 or y + deltaY >= l:
                                    continue

                                if gridMask[x+deltaX][y+deltaY] == 0:
                                    gridMask[x+deltaX][y+deltaY] = 2
    
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
                        removals += 1
                    else:
                        gridMask[x][y] = 0
                    flag = True

    global tiles
    tiles -= removals

    print('done')

def SweepTile(x, y):
    if gridMask[x][y] == 1: #if tile alreadys sweeped
        return

    if gridMask[x][y] == -1: #if tile flagged
        global flags
        flags += 1
        scoreArea.itemconfig(flagText, text="Flags: " + str(flags))

    gridMask[x][y] = 1 #sweep
    global tiles
    tiles -= 1
    gameArea.delete(tileGrid[x][y])

    if grid[x][y] == -1: #loss condition
        GameOver(False)
        return
    
    if grid[x][y] == 0: #if blank tile, ripple
        for deltaX in range(-1, 2):
            if x + deltaX < 0 or x + deltaX >= l:
                continue
            for deltaY in range(-1, 2):
                if y + deltaY < 0 or y + deltaY >= l:
                    continue
                SweepTile(x +deltaX, y +deltaY) #ripple
    else:
        gameArea.tag_raise(textGrid[x][y])

def FlagTile(x, y):
    global flags
    if gridMask[x][y] == 0 and flags > 0:
        gridMask[x][y] = -1
        text = gameArea.create_text(40 + y*80, 40 + x*80, text="!", fill="red", font=('Helvetica', 16, 'bold'))
        flagGrid[x][y] = text
        flags -= 1

    elif gridMask[x][y] == -1:
        gridMask[x][y] = 0
        gameArea.delete(flagGrid[x][y])
        flags += 1
    scoreArea.itemconfig(flagText, text="Flags: " + str(flags))

def CheckWin():
    if flags == 0:
        if tiles == numberOfBombs:
            GameOver(True)

## INTERACTION ##################

def KeyPress(key):

    if key.keycode == 27: #esc
        if active:
            global paused
            paused = not paused
            
            if paused:
                gameArea.pack_forget()
            else:
                gameArea.pack()

    if key.keycode == 87 or key.keycode == 38: #w, uparrow
        movement[0] = 1
    if key.keycode == 65 or key.keycode == 37: #a, leftarrow
        movement[1] = 1
    if key.keycode == 83 or key.keycode == 40: #s, downarrow
        movement[2] = 1
    if key.keycode == 68 or key.keycode == 39: #d, rightarrow
        movement[3] = 1

    if not paused:
        if key.keycode == 13: #enter
            global firstSweep
            print("SWEEP")

            crds = gameArea.coords(cursor)
            x = math.floor(crds[1] / 80)
            y = math.floor(crds[0] / 80)
            if firstSweep:
                GenerateGrid(x, y)
                DisplayGrid()
                firstSweep = False
                UpdateTimer(0)
            else:     
                SweepTile(x, y)
                CheckWin()
        if key.keycode == 8: #backspace
            print("FLAG")

            crds = gameArea.coords(cursor)
            x = math.floor(crds[1] / 80)
            y = math.floor(crds[0] / 80)
            FlagTile(x, y)
            CheckWin()

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
    if not paused:
        crds = gameArea.coords(cursor)
        x = crds[0] + 8 * (movement[3] - movement[1])
        y = crds[1] + 8 * (movement[2] - movement[0])

        if x < 0 or x > 640:
            x = crds[0]
        if y < 0 or y > 640:
            y = crds[1]
            
        gameArea.coords(cursor, x, y)
        gameArea.coords(sweeper, x-126, y-126, x+126, y+126)
    window.after(50, Move)

def MouseMove(mouse):
    if not paused:
        x = mouse.x
        y = mouse.y
        gameArea.coords(cursor, x, y)
        gameArea.coords(sweeper, x-126, y-126, x+126, y+126)

## INTERFACE ####################

def DisplayGrid():
    
    for r in range(l):
        for c in range(l):
            
            #display numbers and bombs
            if grid[r][c] != 0:
                if grid[r][c] == -1:
                    text = gameArea.create_text(40 + c*80, 40 + r*80, text="💣", fill="red")
                else:
                    text = gameArea.create_text(40 + c*80, 40 + r*80, text=str(grid[r][c]), fill="#13e843")
                gameArea.tag_lower(text)
                textGrid[r][c] = text

            #reveal visible values
            if gridMask[r][c] == 1:
                gameArea.delete(tileGrid[r][c])
                if textGrid[r][c] != None:
                    gameArea.tag_raise(textGrid[r][c])

def GameOver(won):
    global paused
    global active
    paused = True
    active = False

    # frame = tk.Frame(window, height=320, width=240)
    # frame.place(x=200, y=160)

    text = scoreArea.create_text(320, 20, text="GAME OVER", fill="#13e843")

    if won:
        print("YAAY!")
        DisplayEndMenu(True)
    else:
        print("BOOM!")
        #gameArea.destroy()
        
        for x in range(l):
            for y in range(l):
                if grid[x][y] == -1:
                    gameArea.tag_raise(textGrid[x][y])
        window.after(2000, DisplayEndMenu, False)
    
    #gameArea.create_image(320, 280, image=menu)

def DisplayEndMenu(won):
    endMenu = tk.Canvas(window, height=320, width=240, bg="#002305", highlightthickness=0)
    endMenu.place(x=200, y=160)

    if won:
        endMenu.create_text(120, 20, text="VICTORY", fill="#13e843")
    else:
        endMenu.create_text(120, 20, text="DEFEAT", fill="#13e843")

def UpdateTimer(time):
    if not paused:
        time += 1
        scoreArea.itemconfigure(timerText, text="Time: " + str(time))
    window.after(1000, UpdateTimer, time)

def Spin(angle):
    if not paused:
        crds = gameArea.coords(cursor)
        x = crds[0]
        y = crds[1]
        gameArea.itemconfig(sweeper, start=angle)
        angle -= 10
    window.after(40, Spin, angle)


window = tk.Tk()
window.title = "Minesweeper"
window.geometry("640x680") #wxh
window.configure(bg='#001703')

tile = tk.PhotoImage(file="tile.png")
crss = tk.PhotoImage(file="crosshair.png")

gameArea = tk.Canvas(window, width=635, height=635, bg='#001703', highlightthickness=5, highlightbackground='#06611b')
scoreArea = tk.Canvas(window, width=640, height=40, bg='#001703', highlightthickness=0)

tileGrid = [[None for c in range(8)] for r in range(8)]
flagGrid = [[None for c in range(8)] for r in range(8)]
textGrid = [[None for c in range(8)] for r in range(8)]
for r in range(8):
    for c in range(8):
        tileGrid[r][c] = gameArea.create_image(40 + c*80, 40 + r*80, image=tile)

timerText = scoreArea.create_text(580, 20, text="Time: 0", fill="#13e843")
flags = 0
flagText = scoreArea.create_text(500, 20, text="Flags: " + str(flags), fill="#13e843")

movement = [0, 0, 0, 0,]

window.bind("<KeyPress>", KeyPress)
window.bind("<KeyRelease>", KeyRelease)
window.bind('<Motion>', MouseMove)

scoreArea.pack()
gameArea.pack()
cursor = gameArea.create_image(320, 320, image=crss)

## MAIN #########################        

l = 8
grid = [[0 for i in range(l)] for i in range(l)] #holds locations of bombs and number indicators
gridMask = [[0 for i in range(l)] for i in range(l)] #stores which tiles are 'visible' to the user 

tiles = l*l
numberOfBombs = int(tiles / 8)
flags = numberOfBombs
scoreArea.itemconfig(flagText, text="Flags: " + str(flags))

firstSweep = True
paused = False
active = True
mouseControls = True

sweeper = gameArea.create_arc(320-126, 320-126, 320+126, 320+126, start=90, extent=90, outline="#0f3e15", fill="#0f3e15", width=4)

Move()
Spin(0)
window.mainloop()