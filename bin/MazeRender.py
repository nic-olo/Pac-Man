from settings import *
from CanvasManager import update_score


def rendMaze(window):
    pass


def make_walls(path, canvas):
    walls = []
    with open(path, 'r') as file:
        for i in range(GRID_ROWS):
            line = file.readline()
            for j in range(GRID_COLUMNS):
                if line[j] == 'W':
                    walls.append([j, i])

    for i in range(len(walls)):
        wall_id = canvas.create_rectangle(GRID_START_X + CELL_WIDTH * walls[i][0],
                                          GRID_START_Y + CELL_HEIGHT * walls[i][1],
                                          GRID_START_X + CELL_WIDTH * (walls[i][0] + 1),
                                          GRID_START_Y + CELL_HEIGHT * (walls[i][1] + 1),
                                          fill=COINS_COLOR)
        walls[i].append(wall_id)

    return walls


def coinsRender(path, canvas, coins_removed, state):
    file = open(path, 'r')
    coins = []

    for i in range(GRID_ROWS):
        line = file.readline()
        for j in range(GRID_COLUMNS):
            temp = True
            if state == 'continue':
                for c in coins_removed:
                    if j == c[0] and i == c[1]:
                        temp = False
                        break
            if line[j] == 'C' and temp:
                coins.append([j, i])

    file.close()

    for i in range(len(coins)):
        coin_id = canvas.create_oval(GRID_START_X + CELL_WIDTH * coins[i][0] + COIN_SIZE_X,
                                     GRID_START_Y + CELL_HEIGHT * coins[i][1] + COIN_SIZE_Y,
                                     GRID_START_X + CELL_WIDTH * (coins[i][0] + 1) - COIN_SIZE_X,
                                     GRID_START_Y + CELL_HEIGHT * (coins[i][1] + 1) - COIN_SIZE_Y,
                                     fill=COINS_COLOR)
        coins[i].append(coin_id)

    return coins


def coin_collision(app):
    direction = app.direction
    coins = app.coins
    canvas = app.canvas

    for coin in coins:
        player_coords = canvas.coords(app.player)
        temp = False
        if direction == 'left' and \
                abs(player_coords[0] - (GRID_START_X + CELL_WIDTH * coin[0] - COIN_SIZE_X)) < 9:
            if abs(player_coords[1] - (GRID_START_Y + CELL_HEIGHT * coin[1])) < 13:
                temp = True

        elif direction == 'right' and abs(
                player_coords[2] - (GRID_START_X + CELL_WIDTH * coin[0] + COIN_SIZE_X)) < 3:
            if abs(player_coords[1] - (GRID_START_Y + CELL_HEIGHT * coin[1])) < 13:
                temp = True

        elif direction == 'up' and abs(
                player_coords[1] - (GRID_START_Y + CELL_HEIGHT * coin[1] - COIN_SIZE_Y)) < 18:
            if abs(player_coords[0] - (GRID_START_X + CELL_WIDTH * coin[0])) < 13:
                temp = True

        elif direction == 'down' and abs(
                player_coords[3] - (GRID_START_Y + CELL_HEIGHT * coin[1] + COIN_SIZE_Y)) < 3:
            if abs(player_coords[0] - (GRID_START_X + CELL_WIDTH * coin[0])) < 13:
                temp = True

        if temp:
            canvas.delete(coin[2])
            app.coins_removed.append(coin)
            coins.remove(coin)
            app.score += 1
            update_score(canvas, app.scoreText, app.score)
