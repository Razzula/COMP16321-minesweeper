import random
import math
import tkinter as tk


## LOGIC ########################

def GenerateGrid(inputX, inputY):
    gridMask[inputX][inputY] = 1

    #PLACE BOMBS
    counter = 0
    while counter < numberOfBombs:
        x = random.randint(0, h-1)
        y = random.randint(0, w-1)
        if gridMask[x][y] == 0 and grid[x][y] == 0: #ensure tile is not starting tile, or already a bomb
            grid[x][y] = -1
            counter += 1
    removals = 1

    print('bombs placed')

    #SET NUMBER INDICATORS
    for x in range(h):
        for y in range(w):
            
            if grid[x][y] == -1: #if tile is bomb

                #update numbers of surronding tiles
                for deltaX in range(-1, 2):
                    if x + deltaX > h-1 or x + deltaX < 0:
                        continue
                    for deltaY in range(-1, 2):
                        if y + deltaY > w-1 or y + deltaY < 0:
                            continue

                        if grid[x + deltaX][y + deltaY] > -1: #if tile not a bomb
                            grid[x + deltaX][y + deltaY] += 1

    print('numbers set')

    #CREATE START AREA
    #set ring around start area as 2s
    for deltaX in range(-1, 2):
        if inputX + deltaX > h-1 or inputX + deltaX < 0:
            continue
        for deltaY in range(-1, 2):
            if inputY + deltaY > w-1 or inputY + deltaY < 0:
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
        for x in range(h):
            for y in range(w):

                if gridMask[x][y] == 2:
                    if grid[x][y] == 0:
                        gridMask[x][y] = 1
                        removals += 1
                        flag = True

                        for deltaX in range(-1, 2):
                            if x + deltaX < 0 or x + deltaX >= h:
                                continue
                            for deltaY in range(-1, 2):
                                if y + deltaY < 0 or y + deltaY >= w:
                                    continue

                                if gridMask[x+deltaX][y+deltaY] == 0:
                                    gridMask[x+deltaX][y+deltaY] = 2
    
    print('blanks set to 1')

    #set 2s to 1s
    flag = True 
    while flag:
        flag = False

        for x in range(h):
            for y in range(w):

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
            if x + deltaX < 0 or x + deltaX >= h:
                continue
            for deltaY in range(-1, 2):
                if y + deltaY < 0 or y + deltaY >= w:
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

def TogglePause():
    global paused
    paused = not paused

    if paused:
        gameArea.pack_forget()
        pauseMenu.place(x=(w*40)-120, y=80*(h-6))
    else:
        pauseMenu.place_forget()
        gameArea.pack()

def ToggleBossKey():
    global bossKey
    bossKey = not bossKey

    global bossSheet

    if bossKey:
        if not paused:
            TogglePause()
        window.maxsize(1920,970)
        window.geometry("1920x970")
        bossSheet = tk.Canvas(window, height=970, width=1920)
        bossSheet.create_image(960, 450, image=bossDecoy)
        bossSheet.place(x=0, y=0)
    else:
        bossSheet.destroy()
        window.maxsize(80*w,80*h+60)
        window.geometry(str(80*w) + "x" + str(80*h+60))

def KeyPress(key):
    
    global active
    global firstSweep
    if active: #gameplay
        global paused

        if key.keycode == 9:
            ToggleBossKey()
        if key.keycode == 27: #esc
            TogglePause()

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
                print("SWEEP")

                crds = gameArea.coords(cursor)
                x = math.floor(crds[1] / 80)
                y = math.floor(crds[0] / 80)
                if firstSweep:
                    GenerateGrid(x, y)
                    DisplayGrid()
                    firstSweep = False
                    UpdateTimer()
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
        else:
            if key.keycode == 8: #backspace
                active = False
                firstSweep = True
                scoreArea.pack_forget()
                gameArea.destroy()
                pauseMenu.place_forget()
                startMenu.place(x=200, y=160)
                print("exit")
                window.maxsize(640, 680)
        
        
        global ctrl, fkey
        if key.keycode == 17:
            ctrl = True
            if fkey:
                
                for x in range(h):
                    for y in range(w):
                        if grid[x][y] == -1:
                            gameArea.tag_raise(textGrid[x][y])
        elif key.keycode == 70:
            fkey = True
            if ctrl:
                for x in range(h):
                    for y in range(w):
                        if grid[x][y] == -1:
                            gameArea.tag_raise(textGrid[x][y])

    elif firstSweep == False: #endScreen
        global playerName
        if key.keycode == 8:
            playerName = playerName[0:-1]
        elif key.keycode >= 65 and key.keycode <= 90:
            if len(playerName) < 3:
                playerName += key.char.upper()
        
        delta = 3 - len(playerName)
        endMenu.itemconfig(playerNameText, text="Name: " + playerName + " _"*delta)

        if delta > 0:
            endMenu.itemconfig(endPromptText, text = "[ ENTER NAME TO CONTINUE ]")
        else:
            endMenu.itemconfig(endPromptText, text = "[ PRESS ENTER TO CONTINUE ]")
            if key.keycode == 13:
                print("restart")
                active = False
                firstSweep = True
                scoreArea.pack_forget()
                gameArea.destroy()
                endMenu.place_forget()
                startMenu.place(x=200, y=160)
                window.maxsize(640, 680)

                try:
                    leaderboard = []
                    file = open("leaderboard.txt", "r")
                    data = file.readlines()
                    for line in data:
                        leaderboard.append(line.split())
                    file.close()

                    #insert new score
                    for i in range(len(leaderboard)):
                        if int(leaderboard[i][1]) == numberOfBombsFound:
                            if numberOfBombsFound > int(leaderboard[i][2]):
                                leaderboard.insert(i, [playerName, numberOfBombsFound, score])
                                break
                        elif int(leaderboard[i][1]) < numberOfBombsFound:
                            leaderboard.insert(i, [playerName, numberOfBombsFound, score])
                            break

                    file = open("leaderboard.txt", "w")
                    for i in range(len(leaderboard)):
                        if i < 5:
                            file.write(leaderboard[i][0] + " " + str(leaderboard[i][1]) + " " + str(leaderboard[i][2]) + "\n")
                    file.close()

                except:
                    file = open("leaderboard.txt", "w")
                    file.write(playerName + " " + str(numberOfBombsFound) + " " + str(score) + "\n___ 0 999"*4)
                    file.close()
        
    else:
        try:
            leaderboardMenu.place_forget()
            settingsMenu.place_forget()
            startMenu.place(x=200, y=160)
        except:
            startMenu.place(x=200, y=160)

def KeyRelease(key):

    if key.keycode == 87 or key.keycode == 38:
        movement[0] = 0
    if key.keycode == 65 or key.keycode == 37:
        movement[1] = 0
    if key.keycode == 83 or key.keycode == 40:
        movement[2] = 0
    if key.keycode == 68 or key.keycode == 39:
        movement[3] = 0

    global ctrl, fkey
    if key.keycode == 17:
        ctrl = False
    elif key.keycode == 70:
        fkey = False

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
    if active:
        window.after(50, Move)

def MouseMove(mouse):
    if not paused and mouseControls:
        x = mouse.x
        y = mouse.y
        gameArea.coords(cursor, x, y)
        gameArea.coords(sweeper, x-126, y-126, x+126, y+126)

def ToggleMouseControls(button):
    global mouseControls
    mouseControls = not mouseControls

    if mouseControls:
        button.configure(fg="#13e843", activeforeground="red")
    else:
        button.configure(fg="red", activeforeground="#13e843")

## INTERFACE ####################

def DisplayGrid():
    
    for r in range(h):
        for c in range(w):
            
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
            elif gridMask[r][c] == -1: #only used during LOAD, not NEW game
                gridMask[r][c] = 0
                FlagTile(r, c)

def DeleteItem(item, canvas):
    canvas.delete(item)

def GameOver(won):
    global paused
    global active
    paused = True
    active = False

    text = scoreArea.create_text(320, 30, text="GAME OVER", fill="#13e843")
    window.after(2000, DeleteItem, text, scoreArea)

    global numberOfBombsFound
    if won:
        print("YAAY!")
        numberOfBombsFound = numberOfBombs
        DisplayEndMenu(True, numberOfBombs)
    else:
        print("BOOM!")
        numberOfBombsFound = 0

        for x in range(h):
            for y in range(w):
                if grid[x][y] == -1:
                    if gridMask[x][y] == -1:
                        gameArea.itemconfig(textGrid[x][y], fill="#13e843")
                        gameArea.delete(flagGrid[x][y])
                        numberOfBombsFound += 1
                    gameArea.tag_raise(textGrid[x][y])
        window.after(2000, DisplayEndMenu, False, numberOfBombsFound)

def DisplayEndMenu(won, numberOfBombsFound):
    global endMenu
    endMenu = tk.Canvas(window, height=320, width=240, bg="#002305", highlightthickness=0)
    endMenu.place(x=(w*40)-120, y=80*(h-6))

    if won:
        endMenu.create_text(120, 20, text="VICTORY", fill="#13e843")
    else:
        endMenu.create_text(120, 20, text="DEFEAT", fill="#13e843")

    global playerNameText
    playerNameText = endMenu.create_text(120, 80, text="Name:  _ _ _", fill="#13e843")
    endMenu.create_text(120, 110, text="Total Bombs: " +str(numberOfBombs), fill="#13e843")
    endMenu.create_text(120, 130, text="Bombs Found: " + str(numberOfBombsFound), fill="#13e843")
    endMenu.create_text(120, 170, text="Time: " + str(score), fill="#13e843")

    global endPromptText
    endPromptText = endMenu.create_text(120, 280, text="[ ENTER NAME TO CONTINUE ]", fill="#13e843")

def CreatePauseMenu():
    global pauseMenu
    pauseMenu = tk.Canvas(window, height=320, width=240, bg="#002305", highlightthickness=0)
    pauseMenu.create_text(120, 20, text="PAUSED", fill="#13e843")

    tk.Button(pauseMenu, text="SAVE", command=Save, bg="#002305", activebackground="#002305", fg="#13e843", activeforeground="#13e843", bd=1).place(x=100, y=80)

    pauseMenu.create_text(120, 280, text="[ PRESS ESC TO UNPAUSE ]", fill="#13e843")
    pauseMenu.create_text(120, 300, text="[ PRESS BACKSPACE TO QUIT ]", fill="#13e843")

def DisplayLeaderboard():
    global leaderboardMenu
    leaderboardMenu = tk.Canvas(window, height=320, width=240, bg="#002305", highlightthickness=0)
    leaderboardMenu.create_text(120, 20, text="LEADERBOARD", fill="#13e843")

    file = open("leaderboard.txt", "r")
    data = file.readlines()
    for i in range(len(data)):
        line = data[i].split()
        if line[0] == "___":
            line[2] = "0"
        leaderboardMenu.create_text(120, 80 + (i * 30), text=line[0] + " " + line[1] + " " + line[2], fill="#13e843")
    leaderboardMenu.create_text(120, 300, text="[ PRESS BACKSPACE TO RETURN ]", fill="#13e843")

    startMenu.place_forget()
    leaderboardMenu.place(x=200, y=160)

def DisplaySettings():
    global settingsMenu
    settingsMenu = tk.Canvas(window, height=320, width=240, bg="#002305", highlightthickness=0)
    settingsMenu.create_text(120, 20, text="SETTINGS", fill="#13e843")

    button = tk.Button(settingsMenu, text="MOUSE CONTROLS", bg="#002305", activebackground="#002305", bd=1)
    if mouseControls:
        button.configure(fg="#13e843", activeforeground="red")
    else:
        button.configure(fg="red", activeforeground="#13e843")
        
    button.configure(command=lambda: ToggleMouseControls(button))
    button.place(x=65, y=80)
    
    settingsMenu.create_text(120, 300, text="[ PRESS BACKSPACE TO RETURN ]", fill="#13e843")

    startMenu.place_forget()
    settingsMenu.place(x=200, y=160)

def UpdateTimer():
    if not paused:
        global score
        score += 1
        scoreArea.itemconfigure(timerText, text="Time: " + str(score))
    if active:
        window.after(1000, UpdateTimer)

def Spin(angle):
    if not paused:
        crds = gameArea.coords(cursor)
        x = crds[0]
        y = crds[1]
        gameArea.itemconfig(sweeper, start=angle)
        angle -= 10
    if active:
        window.after(40, Spin, angle)

def Save():
    if not firstSweep:

        code = random.randint(1000, 9999)
        while True:
            try: #if code in use, generate new one
                tempfile = open("./saves/" + str(code) + ".txt", "r")
                tempfile.close()
                code = random.randint(1000, 9999)
            except:
                break

        file = open("./saves/" + str(code) + ".txt", "w")
        file.write(str(w) + " " + str(h) + " " + str(score) + "\n")
        #store grid
        for x in range(h):
            for y in range(w):
                file.write(str(grid[x][y]) + " ")
            file.write("\n")
        #store gridMask
        for x in range(h):
            for y in range(w):
                file.write(str(gridMask[x][y]) + " ")
            file.write("\n")
        file.close

        text = pauseMenu.create_text(120, 120, text="GAME SAVED AS " + str(code), fill="#13e843")
        window.after(3000, DeleteItem, text, pauseMenu)
    else:
        text = pauseMenu.create_text(120, 120, text="CANNOT SAVE BLANK GAME", fill="red")
        window.after(1000, DeleteItem, text, pauseMenu)

window = tk.Tk()
window.title = "Minesweeper"
window.geometry("640x680") #wxh
window.maxsize(640, 680)
window.configure(bg='#001703')

tile = tk.PhotoImage(file="tile.png")
crss = tk.PhotoImage(file="crosshair.png")
bossDecoy = tk.PhotoImage(file="bosskey.png")

scoreArea = tk.Canvas(window, width=640, height=60, bg='#001703', highlightthickness=0)

timerText = scoreArea.create_text(580, 30, text="Time: 0", fill="#13e843")
flagText = scoreArea.create_text(500, 30, text="Flags: ", fill="#13e843")

mouseControls = True

## MAIN ######################### 

CreatePauseMenu()

def NewGame(height, width):

    global h, w
    h, w = height, width
    global score
    score = -1

    StartGame()

    global firstSweep 
    firstSweep = True

def LoadGame():

    #search for save
    try:
        code = codeInput.get()
        file = open("./saves/" + code + ".txt", "r")
    except:
        text = startMenu.create_text(120, 110, text="SAVE NOT FOUND", fill="red")
        window.after(1000, DeleteItem, text, startMenu)
        return

    code = codeInput.get()
    file = open("./saves/" + code + ".txt", "r")

    data = file.readlines()
    line = data[0].split()

    global w, h
    w = int(line[0])
    h = int(line[1])
    global score
    score = int(line[2]) -1
    
    StartGame()

    global grid
    global gridMask

    #grid
    for x in range(h):
        line = data[x+1].split()
        for y in range(w):
            grid[x][y] = int(line[y])

    #gridMask
    for x in range(h):
        line = data[x+1+h].split()
        for y in range(w):
            gridMask[x][y] = int(line[y])
    
    global firstSweep 
    firstSweep = False

    DisplayGrid()
    UpdateTimer()

def StartGame():
    global gameArea
    global tileGrid
    tileGrid = [[None for c in range(w)] for r in range(h)]
    gameArea = tk.Canvas(window, width=635, height=635, bg='#001703', highlightthickness=5, highlightbackground='#06611b')
    for r in range(h):
        for c in range(w):
            tileGrid[r][c] = gameArea.create_image(40 + c*80, 40 + r*80, image=tile)

    startMenu.place_forget()
    scoreArea.pack()
    gameArea.pack()

    global cursor
    cursor = gameArea.create_image(320, 320, image=crss)
    global sweeper
    sweeper = gameArea.create_arc(320-126, 320-126, 320+126, 320+126, start=90, extent=90, outline="#0f3e15", fill="#0f3e15", width=4)

    global movement
    movement = [0, 0, 0, 0,]

    global grid
    grid = [[0 for i in range(w)] for i in range(h)] #holds locations of bombs and number indicators
    global gridMask
    gridMask = [[0 for i in range(w)] for i in range(h)] #stores which tiles are 'visible' to the user
    global flagGrid
    flagGrid = [[None for c in range(w)] for r in range(h)]
    global textGrid
    textGrid = [[None for c in range(w)] for r in range(h)]

    global tiles
    tiles = w*h
    global numberOfBombs
    numberOfBombs = int(tiles / 8)
    global flags
    flags = numberOfBombs

    scoreArea.itemconfig(flagText, text="Flags: " + str(flags))

    global playerName
    playerName =  ''

    scoreArea.itemconfig(timerText, text="Time: 0")

    global paused
    paused = False
    global active
    active = True

    maxW = 80*w
    maxH = 80*h + 60
    window.maxsize(maxW, maxH)
    window.geometry(str(maxW)+"x"+str(maxH))
    gameArea.configure(height=maxW, width=maxW)

    Move()
    Spin(0)

startMenu = tk.Canvas(window, height=320, width=240, bg='#002305', highlightthickness=0)
startMenu.place(x=200, y=160)

tk.Button(startMenu, text="NEW GAME", command=lambda: NewGame(8, 8), bg="#002305", activebackground="#002305", fg="#13e843", activeforeground="#13e843", bd=1).place(x=0,y=0)
tk.Button(startMenu, text="LOAD GAME", command=LoadGame, bg="#002305", activebackground="#002305", fg="#13e843", activeforeground="#13e843", bd=1).place(x=0,y=40)
codeInput = tk.Entry(startMenu)
codeInput.place(x=0,y=80)
tk.Button(startMenu, text="LEADERBOARD", command=DisplayLeaderboard, bg="#002305", activebackground="#002305", fg="#13e843", activeforeground="#13e843", bd=1).place(x=0,y=120)
tk.Button(startMenu, text="SETTINGS", command=DisplaySettings, bg="#002305", activebackground="#002305", fg="#13e843", activeforeground="#13e843", bd=1).place(x=0,y=160)
tk.Button(startMenu, text="QUIT", command=quit, bg="#002305", activebackground="#002305", fg="#13e843", activeforeground="red", bd=1).place(x=0,y=200)

paused = True
active = False
firstSweep = True
bossKey = False

ctrl = False
fkey = False

window.bind("<KeyPress>", KeyPress)
window.bind("<KeyRelease>", KeyRelease)
window.bind('<Motion>', MouseMove)

leaderboardMenu = tk.Canvas()

window.mainloop()