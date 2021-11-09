from tkinter import Tk, Button, Canvas
from settings import *


def makeWindow():
    window = Tk()
    window.title("Pac-Man")
    window.geometry("%dx%d+%d+%d" %
                    (WINDOW_WIDTH, WINDOW_HEIGHT, X_WIN_POS, Y_WIN_POS))
    window = window
    return window


hideWindow = None


def hide_window(window):
    global hideWindow
    if not hideWindow:
        hideWindow = Canvas(window,
                            width=WINDOW_WIDTH,
                            height=WINDOW_HEIGHT,
                            highlightthickness=0)
        window.title("Project")
        window.attributes("-alpha", 0)

    else:
        hideWindow.destroy()
        window.title("Pac-Man")
        window.attributes("-alpha", 1)
        hideWindow = None
