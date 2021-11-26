#1920x1080
import random
import math
import tkinter as tk

## LOGIC ##############################

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

    global numberOfTiles
    numberOfTiles -= removals

    print('done')

def SweepTile(x, y):
    if gridMask[x][y] == 1: #if tile alreadys sweeped
        return

    if gridMask[x][y] == -1: #if tile flagged
        global numberOfFlags
        numberOfFlags += 1
        scoreArea.itemconfig(flagText, text="Flags: " + str(numberOfFlags))

    gridMask[x][y] = 1 #sweep
    global numberOfTiles
    numberOfTiles -= 1
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
                SweepTile(x +deltaX, y +deltaY) #ripple tiles recursively
    else:
        gameArea.tag_raise(textGrid[x][y])

def FlagTile(x, y):
    global numberOfFlags
    if gridMask[x][y] == 0 and numberOfFlags > 0:
        gridMask[x][y] = -1
        text = gameArea.create_text(40 + y*80, 40 + x*80, text="!", fill="red", font=('Helvetica', 16, 'bold'))
        flagGrid[x][y] = text
        numberOfFlags -= 1

    elif gridMask[x][y] == -1:
        gridMask[x][y] = 0
        gameArea.delete(flagGrid[x][y])
        numberOfFlags += 1
    scoreArea.itemconfig(flagText, text="Flags: " + str(numberOfFlags))

def CheckWin():
    if numberOfFlags == 0:
        if numberOfTiles == numberOfBombs:
            GameOver(True)

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

def UpdateScore(): #clock
    if not paused:
        global score
        score += 1
        scoreArea.itemconfigure(timerText, text="Time: " + str(score))
    if active:
        window.after(1000, UpdateScore)

## INTERACTION ########################

def KeyPress(key):
    
    global firstSweep

    if binding[1]: #keybinding
        BindKey(key)
        return

    if active: #if not game over

        if key.keycode == 9: #tab
            ToggleBossKey()
            return
        elif key.keycode == 27: #esc
            TogglePause()
            return

        #MOVEMENT
        if key.keycode == upKey[0]:
            movement[0] = 1
            return
        elif key.keycode == leftKey[0]:
            movement[1] = 1
            return
        elif key.keycode == downKey[0]:
            movement[2] = 1
            return
        elif key.keycode == rightKey[0]:
            movement[3] = 1
            return   
                 
        #CHEAT
        global ctrl, fkey
        if key.keycode == 17:
            ctrl = True
            if fkey:
                ShowAllBombs()
        elif key.keycode == 70:
            fkey = True
            if ctrl:
                ShowAllBombs()

        if not paused:
            crds = gameArea.coords(cursor)
            x = math.floor(crds[1] / 80)
            y = math.floor(crds[0] / 80)

            #SWEEP
            if key.keycode == 13: #enter
                print("SWEEP")

                if firstSweep:
                    GenerateGrid(x, y)
                    DisplayGrid()
                    firstSweep = False
                    UpdateScore()
                else:     
                    SweepTile(x, y)
                    CheckWin()
                return
            #FLAG
            elif key.keycode == 8: #backspace
                print("FLAG")

                FlagTile(x, y)
                CheckWin()

        else: #PAUSEMENU
            #QUIT TO MENU
            if key.keycode == 8: #backspace
                ReturnToStartMenu(pauseMenu)
                print("exit")

    elif firstSweep == False: #ENDSCREEN
        global playerName

        #NAME INPUT
        if key.keycode == 8: #backspace
            playerName = playerName[0:-1]
        elif key.keycode >= 65 and key.keycode <= 90: #a-z
            if len(playerName) < 3:
                playerName += key.char.upper()
        
        delta = 3 - len(playerName)
        endMenu.itemconfig(playerNameText, text="Name: " + playerName + " _"*delta)

        if delta > 0:
            endMenu.itemconfig(endPromptText, text = "[ ENTER NAME TO CONTINUE ]")
        else:
            endMenu.itemconfig(endPromptText, text = "[ PRESS ENTER TO CONTINUE ]")
            if key.keycode == 13: #enter
                print("restart")
                ReturnToStartMenu(endMenu)

                if not cheat:
                    SaveScore()
        
    else: #MENUS
        #RETURN TO MAIN MENU
        ws = window.winfo_width() #window width
        hs = window.winfo_height() #window height
        try:
            leaderboardMenu.place_forget()
            settingsMenu.place_forget()
            startMenu.place(x=ws/2 - 120, y=hs/2 - 160)
        except:
            startMenu.place(x=ws/2 - 120, y=hs/2 - 160)

def KeyRelease(key):

    if active:
        #MOVEMENT
        if key.keycode == upKey[0]:
            movement[0] = 0
        elif key.keycode == leftKey[0]:
            movement[1] = 0
        elif key.keycode == downKey[0]:
            movement[2] = 0
        elif key.keycode == rightKey[0]:
            movement[3] = 0

        #CHEAT
        global ctrl, fkey
        if key.keycode == 17:
            ctrl = False #key no longer held, prevents cheat code from triggering
        elif key.keycode == 70:
            fkey = False

def Move():
    if not paused:
        crds = gameArea.coords(cursor)
        x = crds[0] + 8 * (movement[3] - movement[1])
        y = crds[1] + 8 * (movement[2] - movement[0])

        #restrict to canvas
        if x < 0 or x > w*80:
            x = crds[0]
        if y < 0 or y > h*80:
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

def BindKey(key):
    global binding, upKey, leftKey, downKey, rightKey
    
    binding[1] = False      
    binding[2].configure(fg="#13e843") #selected button green
    if key.keycode in [9, 27, 13, 8, upKey, leftKey, downKey, rightKey]: #forbidden keys
        errorMessage = settingsMenu.create_text(120, 240, text="INVALID KEY", fill="red")
        window.after(1000, DeleteItem, errorMessage, settingsMenu)
        return
    elif binding[0] == "u":
        upKey[0] = key.keycode
        upKey[1] = str(key.char.upper())
    elif binding[0] == "l":
        leftKey[0] = key.keycode
        leftKey[1] = str(key.char.upper())
    elif binding[0] == "d":
        downKey[0] = key.keycode
        downKey[1] = str(key.char.upper())
    else:
        rightKey[0] = key.keycode
        rightKey[1] = str(key.char.upper())
    binding[2].configure(text=key.char.upper()) #update button text

def ToggleMouseControls(button):
    global mouseControls
    mouseControls = not mouseControls

    if mouseControls:
        button.configure(fg="#13e843", activeforeground="red")
    else:
        button.configure(fg="red", activeforeground="#13e843")

def TogglePause():
    global paused
    paused = not paused

    if paused:
        gameArea.pack_forget()
        ws = window.winfo_width() #window width
        hs = gameArea.winfo_height() #gameArea height
        pauseMenu.place(x=ws/2 - 120, y=hs/2 - 160)
    else:
        pauseMenu.place_forget()
        gameArea.pack()

## INTERFACE ##########################

def DisplayGrid():
    
    for x in range(h):
        for y in range(w):
            
            #display numbers and bombs
            if grid[x][y] != 0:
                if grid[x][y] == -1:
                    text = gameArea.create_text(40 + y*80, 40 + x*80, text="💣", fill="red")
                else:
                    text = gameArea.create_text(40 + y*80, 40 + x*80, text=str(grid[x][y]), fill="#13e843")
                gameArea.tag_lower(text)
                textGrid[x][y] = text

            #reveal visible values
            if gridMask[x][y] == 1:
                gameArea.delete(tileGrid[x][y])
                if textGrid[x][y] != None:
                    gameArea.tag_raise(textGrid[x][y])
            elif gridMask[x][y] == -1: #only used during LOAD, not NEW game
                gridMask[x][y] = 0
                FlagTile(x, y)

def DisplayEndMenu(won, numberOfBombsFound):
    global endMenu
    endMenu = tk.Canvas(window, height=320, width=240, bg="#002305", highlightthickness=0)

    ws = window.winfo_width() #window width
    hs = gameArea.winfo_height() #gameArea height
    endMenu.place(x=ws/2 - 120, y=hs/2 - 160)

    if won:
        endMenu.create_text(120, 20, text="VICTORY", fill="#13e843")
        if cheat:
            endMenu.create_text(120, 40, text="...but at what cost?", fill="red")
    else:
        endMenu.create_text(120, 20, text="DEFEAT", fill="#13e843")

    global playerNameText
    playerNameText = endMenu.create_text(120, 80, text="Name:  _ _ _", fill="#13e843")
    #stats
    endMenu.create_text(120, 110, text="Total Bombs: " +str(numberOfBombs), fill="#13e843")
    endMenu.create_text(120, 130, text="Bombs Found: " + str(numberOfBombsFound), fill="#13e843")
    endMenu.create_text(120, 170, text="Time: " + str(score), fill="#13e843")

    global endPromptText
    endPromptText = endMenu.create_text(120, 280, text="[ ENTER NAME TO CONTINUE ]", fill="#13e843")

def ReturnToStartMenu(currentMenu):
    global active, firstSweep
    active = False
    firstSweep = True

    ws = window.winfo_width() #window width
    hs = window.winfo_height() #window height
    startMenu.place(x=ws/2 - 120, y=hs/2 - 160)

    currentMenu.place_forget()
    scoreArea.pack_forget()
    gameArea.destroy()

def CreatePauseMenu():
    #GENERATE
    global pauseMenu
    pauseMenu = tk.Canvas(window, height=320, width=240, bg="#002305", highlightthickness=0)
    pauseMenu.create_text(120, 20, text="PAUSED", fill="#13e843")

    tk.Button(pauseMenu, text="SAVE", command=SaveGame, bg="#002305", activebackground="#002305", fg="#13e843", activeforeground="#13e843", bd=1).place(x=100, y=80)

    pauseMenu.create_text(120, 280, text="[ PRESS ESC TO UNPAUSE ]", fill="#13e843")
    pauseMenu.create_text(120, 300, text="[ PRESS BACKSPACE TO QUIT ]", fill="#13e843")

def DisplayLeaderboard():
    #GENERATE
    global leaderboardMenu
    leaderboardMenu = tk.Canvas(window, height=320, width=240, bg="#002305", highlightthickness=0)
    leaderboardMenu.create_text(120, 20, text="LEADERBOARD", fill="#13e843")

    file = open("leaderboard.txt", "r")
    data = file.readlines()
    leaderboardMenu.create_text(120, 60, text="NAME \t BOMBS \t TIME \n -------------------------", fill="#13e843")
    for i in range(len(data)):
        line = data[i].split()
        if line[0] == "___":
            line[2] = "0"
        leaderboardMenu.create_text(120, 100 + (i * 30), text=line[0] + " \t" + line[1] + " \t" + line[2], fill="#13e843")
    leaderboardMenu.create_text(120, 300, text="[ PRESS BACKSPACE TO RETURN ]", fill="#13e843")

    #DISPLAY
    startMenu.place_forget()
    ws = window.winfo_width() #window width
    hs = window.winfo_height() #window height
    leaderboardMenu.place(x=ws/2 - 120, y=hs/2 - 160)

def DisplaySettings():
    #GENERATE
    global settingsMenu
    settingsMenu = tk.Canvas(window, height=320, width=240, bg="#002305", highlightthickness=0)
    settingsMenu.create_text(120, 20, text="SETTINGS", fill="#13e843")

    #mouse control button
    button = tk.Button(settingsMenu, text="MOUSE CONTROLS", bg="#002305", activebackground="#002305", bd=1)
    if mouseControls:
        button.configure(fg="#13e843", activeforeground="red")
    else:
        button.configure(fg="red", activeforeground="#13e843")
        
    button.configure(command=lambda: ToggleMouseControls(button))
    button.place(x=65, y=80)

    #keybind buttons
    up = tk.Button(settingsMenu, width=2, text=upKey[1], bg="#002305", activebackground="#002305", fg="#13e843", activeforeground="yellow", bd=1)
    up.configure(command= lambda: SetActiveBind("u", up)) 
    up.place(x=110, y=120)
    left = tk.Button(settingsMenu, width=2, text=leftKey[1], bg="#002305", activebackground="#002305", fg="#13e843", activeforeground="yellow", bd=1)
    left.configure(command= lambda: SetActiveBind("l", left)) 
    left.place(x=90, y=145)
    down = tk.Button(settingsMenu, width=2, text=downKey[1], bg="#002305", activebackground="#002305", fg="#13e843", activeforeground="yellow", bd=1)
    down.configure(command= lambda: SetActiveBind("d", down)) 
    down.place(x=110, y=145)
    right = tk.Button(settingsMenu, width=2, text=rightKey[1], bg="#002305", activebackground="#002305", fg="#13e843", activeforeground="yellow", bd=1)
    right.configure(command= lambda: SetActiveBind("r", right)) 
    right.place(x=130, y=145)
    
    settingsMenu.create_text(120, 300, text="[ PRESS BACKSPACE TO RETURN ]", fill="#13e843")

    #DISPLAY
    startMenu.place_forget()
    ws = window.winfo_width() #window width
    hs = window.winfo_height() #window height
    settingsMenu.place(x=ws/2 - 120, y=hs/2 - 160)

def Spin(angle):
    if not paused:
        crds = gameArea.coords(cursor)
        x = crds[0]
        y = crds[1]
        gameArea.itemconfig(sweeper, start=angle)
        angle -= 10
    if active:
        window.after(40, Spin, angle)

def ShowAllBombs():
    global cheat
    cheat = True
    for x in range(h):
        for y in range(w):
            if grid[x][y] == -1:
                gameArea.tag_raise(textGrid[x][y])

    text = scoreArea.create_text(320, 30, text="X-RAY ACTIVE. SCORE WILL NOT COUNT!", fill="red")
    window.after(4000, DeleteItem, text, scoreArea)

def ToggleBossKey():
    global bossKeyActive
    bossKeyActive = not bossKeyActive

    global bossSheet

    if bossKeyActive:
        if not paused:
            TogglePause()
        bossSheet = tk.Canvas(window, height=1080, width=1920, bd=0)
        bossSheet.create_image(960, 540, image=bossDecoy)
        bossSheet.place(x=0, y=0)
    else:
        bossSheet.destroy()

def DeleteItem(item, canvas): #deletes an item, can be calledby .after() to give an item a lifespan
    canvas.delete(item)

def SetActiveBind(direction, button): #record the key that is currently being bound
    global binding
    if binding[2] != None:
        binding[2].configure(fg="#13e843") #if key already being bound, unhighlight it
    binding = [direction, True, button]
    button.configure(fg="yellow") #highlight key to user

## GAME STATE #########################

def NewGame(height, width):

    global h, w, score, firstSweep
    h, w = height, width
    score = -1

    StartGame()
    
    firstSweep = True

def LoadGame():

    #search for save
    try:
        code = codeInput.get()
        file = open("./saves/" + code + ".txt", "r")
    except:
        if code == '':
            text = startMenu.create_text(120, 155, text="ENTER GAME CODE", fill="red")
        else:
            text = startMenu.create_text(120, 155, text="INVALID CODE", fill="red")
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
    UpdateScore()

def StartGame():
    # GUI
    global tileGrid, gameArea, cursor, sweeper

    tileGrid = [[None for c in range(w)] for r in range(h)]
    gameArea = tk.Canvas(window, width=635, height=635, bg='#001703', highlightthickness=5, highlightbackground='#06611b')
    for r in range(h):
        for c in range(w):
            tileGrid[r][c] = gameArea.create_image(40 + c*80, 40 + r*80, image=tile)

    maxW, maxH = 80*w-5, 80*h-5
    gameArea.configure(height=maxH, width=maxW)

    startMenu.place_forget()
    scoreArea.pack()
    gameArea.pack()

    cursor = gameArea.create_image(320, 320, image=crss)
    sweeper = gameArea.create_arc(320-126, 320-126, 320+126, 320+126, start=90, extent=90, outline="#0f3e15", fill="#0f3e15", width=4)

    # GAMEPLAY
    global grid, gridMask, flagGrid, textGrid, numberOfTiles, numberOfBombs, numberOfFlags, movement
    grid = [[0 for i in range(w)] for i in range(h)] #holds locations of bombs and number indicators
    gridMask = [[0 for i in range(w)] for i in range(h)] #stores which tiles are 'visible' to the user
    flagGrid = [[None for c in range(w)] for r in range(h)]
    textGrid = [[None for c in range(w)] for r in range(h)]

    numberOfTiles = w*h
    numberOfBombs = int(numberOfTiles / 8)
    numberOfFlags = numberOfBombs
    movement = [0, 0, 0, 0,]

    # STATS
    scoreArea.itemconfig(flagText, text="Flags: " + str(numberOfFlags))
    scoreArea.itemconfig(timerText, text="Time: 0")

    global playerName
    playerName =  ''

    # SETTINGS
    global paused, active, cheat
    paused = False
    active = True
    cheat = False

    Move()
    Spin(0)

def SaveGame():
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

def SaveScore():
    try:
        leaderboard = []
        file = open("leaderboard.txt", "r") #will jump to except if file does not exist
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
        #make new leaderbaord
        file = open("leaderboard.txt", "w")
        file.write(playerName + " " + str(numberOfBombsFound) + " " + str(score) + "\n___ 0 99999"*4)
        file.close()

## MAIN ###############################

window = tk.Tk()
window.title = "Minesweeper"
window.attributes("-fullscreen", True)
window.configure(bg='#001703')

#images
tile = tk.PhotoImage(file="./images/tile.png")
crss = tk.PhotoImage(file="./images/crosshair.png")
bossDecoy = tk.PhotoImage(file="./images/bosskey.png")

#START MENU
startMenu = tk.Canvas(window, height=320, width=240, bg='#002305', highlightthickness=0)

startMenu.create_text(120, 20, text="MINESWEEPER", fill="#13e843")

tk.Button(startMenu, text="EASY", command=lambda: NewGame(8, 8), bg="#002305", activebackground="#002305", fg="#13e843", activeforeground="#13e843", bd=1).place(x=50,y=60)
tk.Button(startMenu, text="MEDIUM", command=lambda: NewGame(10, 14), bg="#002305", activebackground="#002305", fg="#13e843", activeforeground="#13e843", bd=1).place(x=90,y=60)
tk.Button(startMenu, text="HARD", command=lambda: NewGame(12, 24), bg="#002305", activebackground="#002305", fg="#13e843", activeforeground="#13e843", bd=1).place(x=150,y=60)
tk.Button(startMenu, text="LOAD GAME", command=LoadGame, bg="#002305", activebackground="#002305", fg="#13e843", activeforeground="#13e843", bd=1).place(x=80,y=100)
codeInput = tk.Entry(startMenu, width=12, bg="#002305", fg="#13e843",justify="center")
codeInput.place(x=80,y=125)
tk.Button(startMenu, text="LEADERBOARD", command=DisplayLeaderboard, bg="#002305", activebackground="#002305", fg="#13e843", activeforeground="#13e843", bd=1).place(x=75,y=165)
tk.Button(startMenu, text="SETTINGS", command=DisplaySettings, bg="#002305", activebackground="#002305", fg="#13e843", activeforeground="#13e843", bd=1).place(x=85,y=205)
tk.Button(startMenu, text="QUIT", command=quit, bg="#002305", activebackground="#002305", fg="#13e843", activeforeground="red", bd=1).place(x=100,y=285)

startMenu.place(x=840, y=380)

#initalise globals
paused, firstSweep = True, True
active, bossKeyActive, mouseControls = False, False, False
ctrl, fkey, cheat = False, False, False

upKey = [87, "W"]
leftKey = [65, "A"]
downKey = [83, "S"]
rightKey = [68, "D"]
binding = ["", False, None]

scoreArea = tk.Canvas(window, width=640, height=60, bg='#001703', highlightthickness=0)
CreatePauseMenu()
leaderboardMenu = tk.Canvas()

timerText = scoreArea.create_text(580, 30, text="Time: 0", fill="#13e843")
flagText = scoreArea.create_text(500, 30, text="Flags: ", fill="#13e843")

#bind keys
window.bind("<KeyPress>", KeyPress)
window.bind("<KeyRelease>", KeyRelease)
window.bind('<Motion>', MouseMove)

#START
window.mainloop()