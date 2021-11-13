import os
import pickle
from settings import *


def save_game(coords, coins_removed, button):
    if not os.path.exists('../save/'):
        os.mkdir('../save')
    with open("../save/gameSave.pickle", "wb+") as game_save:
        pickle.dump({'player_coords': coords, 'coins_removed': coins_removed}, game_save)

    button.configure(background='blue', text='Saved!', state='disabled')


def play_game():
    if os.path.exists("../save/gameSave.pickle"):
        with open("../save/gameSave.pickle", 'rb') as game_save:
            old_save = pickle.load(game_save)
        return old_save['player_coords'], old_save['coins_removed']
    else:
        return PLAYER_COORDINATES, []
