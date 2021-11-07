"""Declaring all the constants that I will need
while developing this project."""

WIDTH = 1280
HEIGHT = 720

IMG_WIDTH = 560
IMG_HEIGHT = 620

GRID_START_X = 360
GRID_STOP_X = 920
GRID_START_Y = 6
GRID_STOP_Y = 632

GRID_ROWS = 31
GRID_COLUMNS = 31

CELL_WIDTH = (GRID_STOP_X-GRID_START_X)/GRID_COLUMNS
CELL_HEIGHT = (GRID_STOP_Y-GRID_START_Y)/GRID_ROWS

MAZE_PATH = "../GameBoard/GameBoard.png"
MAZE_COORDINATES_PATH = "../GameBoard/GameBoardWalls.txt"

X_WIN_POS = 0  # (ws/2) - (w/2) # calculate center
Y_WIN_POS = 0  # (hs/2) - (h/2) # TO FIX

PLAYER_DIMENSIONS = 25
PLAYER_X1 = 632
PLAYER_X2 = 648
PLAYER_Y1 = 472
PLAYER_Y2 = 488

RECTANGLE_X1 = 631
RECTANGLE_X2 = 649
RECTANGLE_Y1 = 470
RECTANGLE_Y2 = 491

COINS_RATIO = 7
COIN_SIZE_X = CELL_WIDTH/CELL_HEIGHT * COINS_RATIO
COIN_SIZE_Y = CELL_HEIGHT/CELL_HEIGHT * COINS_RATIO


PLAYER_COLOR = '#FFFF00'
COINS_COLOR = '#FFD700'

PLAYER_SPEED = 1.5
# TODO bind PLAYER_SPEED and FPS
FPS = 60
DELAY = int(1000 / FPS)  # round the number to avoid errors


SCORE_POS_X = 180
SCORE_POS_Y = 200
HIGH_SCORE_POS_X = 1100
HIGH_SCORE_POS_Y = 200