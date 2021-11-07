from tkinter import Tk, Button
from settings import *


def makeWindow():
    window = Tk()
    window.title("Pac-Man")
    window.geometry("%dx%d+%d+%d" %
                    (WIDTH, HEIGHT, X_WIN_POS, Y_WIN_POS))
    window = window
    return window



