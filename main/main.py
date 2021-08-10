from cmu_112_graphics import *
from Player import Player
from Block import Block
from Perlin import Perlin

def runTerraria():
    width, height = 800, 400
    runApp(width=width, height=height)


# TODO:
# make keyreleased work
# set random button to make a parabola jump?
# add citations
# proposal.txt
# how to procedurally generate
# update how blocks are generated and the blocks under it
# wall and ceiling collision
# cite images

def appStarted(app):
    app._root.resizable(False, False)
    app.timerDelay = 10
    app.rows = int(app.height / Block.height)
    app.cols = int(app.width / Block.width)

    app.player = Player(app)
    app.scrollX = 0
    app.scrollY = 0
    app.scrollDY = 0
    app.gravity = 1

    app.terrain = [[None] * app.cols for _ in range(app.rows)]
    midRow = int(app.rows / 2) + 2
    for col in range(len(app.terrain[0])):
        app.terrain[midRow][col] = Block(app, midRow, col, "grass_block")
        #addColumn(app.terrain, col, 10) # laggy

    for i in range(50):
        ampl = 20
        freq = 40
        y = int(Perlin.perlin(i / freq) * ampl)
        addColumn(app, app.terrain, len(app.terrain[0]) - 1, midRow + y)

def keyPressed(app, event):
    if event.key == "a":
        app.player.isMoving = True
        app.player.moveAnimation(-1)
    elif event.key == "d":
        app.player.isMoving = True
        app.player.moveAnimation(1)
    elif event.key == "s":
        app.player.isMoving = False
    elif event.key == "Space" and app.player.onGround(app):
        #app.player.jump(app)
        app.scrollDY = app.player.jumpSpeed
        app.scrollY += app.scrollDY

# runs even when key not released?
def keyReleased(app, event):
    #app.player.isMoving = False
    pass

def mousePressed(app, event):
    pass

def timerFired(app):
    if app.player.isMoving:
        app.player.moveAnimation(app.player.direction)
        if app.player.direction == -1:
            app.scrollX += app.player.speed 
        elif app.player.direction == 1:
            app.scrollX -= app.player.speed 

    if not app.player.onGround(app):
        app.player.fallAnimation(app.player.direction)
        app.scrollDY -= app.gravity
        app.scrollY += app.scrollDY

    if app.player.onGround(app) and not app.player.isMoving:
        app.player.standAnimation(app.player.direction)

    # procedurally generate to the right
    # if -app.scrollX + app.width / 2 > len(app.terrain) * Block.width:
    #     app.distanceTravelled += 0.1
    #     y = Perlin.perlin(app.distanceTravelled)
    #     addColumn(app, app.terrain, len(app.terrain) - 1, y * len(app.terrain))
    #     print("hi")


def redrawAll(app, canvas):
    drawBlocks(app, canvas)
    app.player.draw(app, canvas)
    drawPerlin(app, canvas)

def drawBlocks(app, canvas):
    for row in range(len(app.terrain)):
        for col in range(len(app.terrain[0])):
            block = app.terrain[row][col]
            if block != None:
                block.draw(app, canvas)

def drawPerlin(app, canvas):
    x = 0
    while x < 50:
        x += 0.1
        y = Perlin.perlin(x)
        canvas.create_oval(x*100, 100 + y*100, x*100 + 10, 100 + y*100 + 10, fill="black")
    
# adds a block in app.terrain at index i at height h
def addColumn(app, L, i, h):
    # for j in range(h, len(L)):
    #     row = L[j]
    #     row.insert(i, Block(app, j, i, "grass_block"))
    for j in range(len(L)):
        row = L[j]
        if j == h:
            row.append(Block(app, j, i, "grass_block"))
        else:
            row.append(None)


def main():
    runTerraria()

if __name__ == "__main__":
    main()