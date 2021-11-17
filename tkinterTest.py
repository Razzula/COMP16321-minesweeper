import tkinter as tk

window = tk.Tk()
window.title = "test"
window.geometry("640x640")

img = tk.PhotoImage(file="tile.png")
crss = tk.PhotoImage(file="crosshair.png")

canvas = tk.Canvas(window, width=640, height=640)

grid = [[None for c in range(8)] for r in range(8)]

for r in range(8):
    for c in range(8):
        grid[r][c] = canvas.create_image(41 + c*80, 41 + r*80, image=img)

movement = [0, 0, 0, 0,]

def KeyPress(key):
    #print(key.char + ' pressed')

    #u38 87, l37 65, d40 83, r39 68
    if key.keycode == 87 or key.keycode == 38:
        movement[0] = 1
    if key.keycode == 65 or key.keycode == 37:
        movement[1] = 1
    if key.keycode == 83 or key.keycode == 40:
        movement[2] = 1
    if key.keycode == 68 or key.keycode == 39:
        movement[3] = 1

    #enter: 13, backspace: 8
    if key.keycode == 13:
        print("SWEEP")
        canvas.delete(grid[0][0])
    if key.keycode == 8:
        print("FLAG")

    Move()

def KeyRelease(key):
    #print(key.char + ' relesed')

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

window.bind("<KeyPress>", KeyPress)
window.bind("<KeyRelease>", KeyRelease)

canvas.pack()
cursor = canvas.create_image(320, 320, image=crss)

window.mainloop()