from settings import *


class Player:
    def __init__(self, canvas):
        self.player = canvas.create_oval(PLAYER_X1, PLAYER_X2,
                                         PLAYER_Y1, PLAYER_Y2, fill="yellow")

    def makePlayer(self, canvas):
        self.player = canvas.create_oval(PLAYER_X1, PLAYER_X2,
                                         PLAYER_Y1, PLAYER_Y2, fill="yellow")
