"""a collection of some methods that involve the main window"""
from tkinter import Tk, Canvas, PhotoImage, CENTER
from settings import *
import os


def makeWindow():
    """create the window"""
    window = Tk()
    window.title("Pac-Man")
    window.geometry("%dx%d+%d+%d" %
                    (WINDOW_WIDTH, WINDOW_HEIGHT, X_WIN_POS, Y_WIN_POS))
    window = window
    return window


hideWindow = None
boss = None


