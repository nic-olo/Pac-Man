from tkinter import *

from PIL import Image, ImageTk

from settings import *


def makeCanvas(window):
    canvas = Canvas(window, bg="black", width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
    return canvas


def setImage(path):
    image = Image.open(path)
    image = image.resize((IMG_WIDTH, IMG_HEIGHT), Image.ANTIALIAS)
    image = ImageTk.PhotoImage(image)
    return image


def makeLines(canvas):
    lines = []
    for i in range(0, GRID_COLUMNS+1):
        lines.append(canvas.create_line(GRID_START_X + CELL_WIDTH * i, GRID_START_Y,
                           GRID_START_X + CELL_WIDTH * i, GRID_STOP_Y, fill="white"))

    for i in range(0, GRID_ROWS+1):
        lines.append(canvas.create_line(GRID_START_X, GRID_START_Y + CELL_HEIGHT * i, GRID_STOP_X,
                           GRID_START_Y + CELL_HEIGHT * i,  fill="white"))
    return lines


def display_scores(canvas):
    scoreText = canvas.create_text(
        SCORE_POS_X, SCORE_POS_Y,
        fill="white",
        font="Algerian",
        text='SCORE: 0'
    )
    highScoreText = canvas.create_text(
        HIGH_SCORE_POS_X, HIGH_SCORE_POS_Y, fill="white",
        font="Algerian",
        text='HIGH SCORE: 0'
    )
    return scoreText, highScoreText


def update_score(canvas, scoreText, score):
    txt = "SCORE: " + str(score)
    canvas.itemconfigure(scoreText, text=txt)


def move_player(window, canvas, player):
    canvas.pack()
    positions = [canvas.coords(player[0])]
    canvas.move(player[0], -2, 0)





