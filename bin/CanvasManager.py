"""collection of some methods that involve the canvas"""

from tkinter import *

from tkinter import PhotoImage
from settings import *


def makeCanvas(window):
    """create the canvas"""
    canvas = Canvas(window, background=CANVAS_COLOR, width=WINDOW_WIDTH,
                    height=WINDOW_HEIGHT, highlightthickness=0)
    return canvas


def setImage(path):
    """set an image"""
    image = PhotoImage(path)
    return image


def make_lines(canvas):
    """create the lines"""
    lines = []
    for i in range(0, GRID_COLUMNS + 1):
        lines.append(
            canvas.create_line(GRID_START_X + CELL_WIDTH * i, GRID_START_Y,
                               GRID_START_X + CELL_WIDTH * i, GRID_STOP_Y,
                               fill="white"))

    for i in range(0, GRID_ROWS + 1):
        lines.append(
            canvas.create_line(GRID_START_X, GRID_START_Y + CELL_HEIGHT * i,
                               GRID_STOP_X,
                               GRID_START_Y + CELL_HEIGHT * i, fill="white"))
    for line in lines:
        canvas.itemconfigure(line, state='hidden')
    return lines


def display_scores(canvas, score, high_score):
    """display the score and the high score"""
    scoreText = canvas.create_text(
        SCORE_POS_X, SCORE_POS_Y,
        fill="white",
        font="Algerian",
        text=f'SCORE: {score}'
    )
    highScoreText = canvas.create_text(
        HIGH_SCORE_POS_X, HIGH_SCORE_POS_Y, fill="white",
        font="Algerian",
        text=f'HIGH SCORE: {high_score}'
    )
    return scoreText, highScoreText


def update_score(canvas, scoreText, score):
    """update the score"""
    txt = "SCORE: " + str(score)
    canvas.itemconfigure(scoreText, text=txt)


def move_grid(sprite, positions):
    """move the grid"""
    sprite.canvas.coords(sprite.grid,
                         ((positions[0] +
                           CELL_WIDTH // 2) // CELL_WIDTH) * CELL_WIDTH + 4,
                         ((positions[1] +
                           CELL_HEIGHT // 2) // CELL_HEIGHT) * CELL_HEIGHT + 6,
                         ((positions[2] +
                           CELL_WIDTH // 2) // CELL_WIDTH) * CELL_WIDTH + 4,
                         ((positions[3] +
                           CELL_HEIGHT // 2) // CELL_HEIGHT) * CELL_HEIGHT + 6)
