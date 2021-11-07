from settings import *


def rendMaze(window):
    pass


def wallsCoordinates(path):
    file = open(path, 'r')
    walls = []
    for i in range(GRID_ROWS):
        line = file.readline()
        for j in range(GRID_COLUMNS):
            if line[j] == '1':
                walls.append([j, i])
    return walls


def coinsRender(path, canvas):
    file = open(path, 'r')
    coins = []
    for i in range(GRID_ROWS):
        line = file.readline()
        for j in range(GRID_COLUMNS):
            if line[j] == 'C':
                coins.append([j, i])

    for i in range(len(coins)):
        coin_id = canvas.create_oval(GRID_START_X + CELL_WIDTH * coins[i][0] + COIN_SIZE_X,
                                     GRID_START_Y + CELL_HEIGHT * coins[i][1] + COIN_SIZE_Y,
                                     GRID_START_X + CELL_WIDTH * (coins[i][0] + 1) - COIN_SIZE_X,
                                     GRID_START_Y + CELL_HEIGHT * (coins[i][1] + 1) - COIN_SIZE_Y,
                                     fill=COINS_COLOR)
        coins[i].append(coin_id)

    return coins
