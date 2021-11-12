import os
import pickle
from settings import *


def save_game(coords, coins_removed, button):
    if not os.path.exists('../save/'):
        os.mkdir('../save')
    with open("../save/gameSave.pickle", "wb") as game_save:
        pickle.dump(
            {'player_coords': coords,
             'coins_removed': coins_removed}, game_save)
    button.configure(background='blue', text='Saved!', state='disabled')


def play_game():
    if os.path.exists("../save/gameSave.pickle"):
        with open("../save/gameSave.pickle", 'rb') as game_save:
            savedData = pickle.load(game_save)
        return savedData['player_coords'], savedData['coins_removed']
    else:
        return [PLAYER_X1, PLAYER_Y1, PLAYER_X2, PLAYER_Y2], coins_removed
