"""A collection of all the methods used to save the objects and
the settings of the game"""
import os
import pickle
from settings import *


def update_settings(keySettings):
    """update the settings"""
    if not os.path.exists(SAVE_PATH):
        os.mkdir(SAVE_PATH)
    with open(SETTINGS_PATH, "wb") as key_settings:
        pickle.dump(keySettings, key_settings)


def load_settings():
    """load the settings"""
    if os.path.exists(SETTINGS_PATH):
        with open(SETTINGS_PATH, 'rb') as key_settings:
            return pickle.load(key_settings)
    else:
        return DEFAULT_SETTINGS


def save_game(player, enemies, coins_removed, score, button):
    """save the game"""
    if not os.path.exists(SAVE_PATH):
        os.mkdir(SAVE_PATH)
    with open(GAME_SAVE_PATH, "wb+") as game_save:
        pickle.dump(
            {
                'player_coords': player,
                'enemies_coords': enemies,
                'coins_removed': coins_removed,
                'score': score
            },
            game_save
        )

    button.configure(background='blue', text='Saved!', state='disabled')


def continue_game():
    """retrieve an old game save"""
    with open(GAME_SAVE_PATH, 'rb') as game_save:
        old_save = pickle.load(game_save)
    return old_save['player_coords'], old_save['enemies_coords'], \
        old_save['coins_removed'], old_save['score']


def save_score(leaderboard):
    """save a score"""
    if not os.path.exists(SAVE_PATH):
        os.mkdir(SAVE_PATH)
    with open(LEADER_BOARD_PATH, "wb+") as game_save:
        pickle.dump(leaderboard, game_save)


def load_leaderboard():
    """load the leaderboard"""
    if os.path.exists(LEADER_BOARD_PATH):
        with open(LEADER_BOARD_PATH, 'rb') as leaderboard:
            return pickle.load(leaderboard)
    else:
        return []
