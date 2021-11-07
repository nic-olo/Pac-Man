from tkinter import Tk, Button
from settings import *


def makeWindow():
    window = Tk()
    window.title("Pac-Man")
    window.geometry("%dx%d+%d+%d" %
                    (WIDTH, HEIGHT, X_WIN_POS, Y_WIN_POS))
    window = window
    return window


def display_menu(window):
    buttons = []
    display_buttons(window, buttons)


def display_buttons(window, buttons):
    buttons.append(Button(window,
                          text="New Game",
                          width=BUTTON_WIDTH,
                          height=BUTTON_HEIGHT))
    buttons[-1].place(x=BUTTON_1_X, y=BUTTON_1_Y)

    buttons.append(Button(window,
                          text="CONTINUE",
                          width=BUTTON_WIDTH,
                          height=BUTTON_HEIGHT))
    buttons[-1].place(x=BUTTON_2_X, y=BUTTON_2_Y)

    buttons.append(Button(window,
                          text="LEADERBOARD",
                          width=BUTTON_WIDTH,
                          height=BUTTON_HEIGHT))
    buttons[-1].place(x=BUTTON_3_X, y=BUTTON_3_Y)

    buttons.append(Button(window,
                          text="CONTROLS",
                          width=BUTTON_WIDTH,
                          height=BUTTON_HEIGHT))
    buttons[-1].place(x=BUTTON_4_X, y=BUTTON_4_Y)
