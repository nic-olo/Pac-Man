import os
import pickle
from settings import *


def update_default_key_settings(keySettings):
    if not os.path.exists('../save/'):
        os.mkdir('../save')
    with open("../save/settings.pickle", "wb") as key_settings:
        pickle.dump(keySettings, key_settings)


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


def save_score(leaderboard):
    if not os.path.exists('../save/'):
        os.mkdir('../save')
    with open("../save/leaderboard.pickle", "wb+") as game_save:
        pickle.dump({'names': leaderboard['names'], 'score': leaderboard['score']}, game_save)


def load_leaderboard():
    if os.path.exists("../save/leaderboard.pickle"):
        with open("../save/leaderboard.pickle", 'rb') as leaderboard:
            topPlayers = pickle.load(leaderboard)
    else:
        topPlayers = []

    return topPlayers
