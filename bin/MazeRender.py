"""collection of all the methods that modify the maze"""
from settings import *
from CanvasManager import update_score


def make_walls(path, canvas):
    """create the walls of the maze"""
    walls = []
    with open(path, 'r') as file:
        for i in range(GRID_ROWS):
            line = file.readline()
            for j in range(GRID_COLUMNS):
                if line[j] == 'W':
                    walls.append([j, i])

    for i in range(len(walls)):
        wall_id = canvas.create_rectangle(
            GRID_START_X + CELL_WIDTH * walls[i][0],
            GRID_START_Y + CELL_HEIGHT * walls[i][1],
            GRID_START_X + CELL_WIDTH * (walls[i][0] + 1),
            GRID_START_Y + CELL_HEIGHT * (walls[i][1] + 1),
            fill=MAZE_COLOR)
        walls[i].append(wall_id)

    return walls


def coins_renderer(path, canvas, coins_removed, state):
    """create the coins"""
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
        coin_id = canvas.create_oval(
            GRID_START_X + CELL_WIDTH * coins[i][0] + COIN_SIZE_X,
            GRID_START_Y + CELL_HEIGHT * coins[i][1] + COIN_SIZE_Y,
            GRID_START_X + CELL_WIDTH * (coins[i][0] + 1) - COIN_SIZE_X,
            GRID_START_Y + CELL_HEIGHT * (coins[i][1] + 1) - COIN_SIZE_Y,
            fill=COINS_COLOR)
        coins[i].append(coin_id)

    return coins


def coin_collision(app):
    """check for a collision between a coin and the player"""
    coins = app.coins
    canvas = app.canvas

    for coin in coins:
        player_coords = canvas.coords(app.player.player)
        coin_coords = canvas.coords(coin[2])
        if coin_coords[0] < player_coords[2] and coin_coords[2] > \
                player_coords[0] and \
                coin_coords[1] < player_coords[3] and coin_coords[3] > \
                player_coords[1]:
            canvas.delete(coin[2])
            app.coins_removed.append(coin)
            coins.remove(coin)
            app.score += 1
            update_score(canvas, app.scoreText, app.score)

    if not coins:
        app.coins = coins_renderer(MAZE_COORDINATES_PATH, canvas, [],
                                   'start')
