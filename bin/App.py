import pickle
from tkinter import Button

import os

from CanvasManager import *  # specify the modules!!!!
from WindowManager import *
from MazeRender import *
from SavingMananger import *
from Enemy import Enemy


# from Player import Player


class App:
    def __init__(self):
        self.texts = []
        self.buttons = []
        self.window = makeWindow()
        self.canvas = makeCanvas(self.window)
        # self.image = setImage(MAZE_PATH)
        self.load_default_key_settings()
        self.configure_controls()
        self.player_coords, self.coins_removed = play_game()
        self.direction = None
        self.leaderboard = load_leaderboard()
        self.prev_direction = None
        self.isPause = True
        self.state = "menu"
        self.score = 0
        self.enemies = []

    def load_default_key_settings(self):
        if os.path.exists("../save/settings.pickle"):
            with open("../save/settings.pickle", 'rb') as key_settings:
                self.keySettings = pickle.load(key_settings)
        else:
            self.keySettings = DEFAULT_KEY_SETTINGS

    def startUp(self):
        # self.gameBoard = self.canvas.create_image(640, 320, anchor=CENTER, image=self.image)
        self.lines = makeLines(self.canvas)
        self.makeRectangle()
        self.playerSpeed = PLAYER_SPEED
        self.walls = make_walls(MAZE_COORDINATES_PATH, self.canvas)
        self.coins = coinsRender(MAZE_COORDINATES_PATH, self.canvas, self.coins_removed, self.state)
        self.scoreText, self.highScoreText = display_scores(self.canvas)
        self.make_enemies()
        self.makePlayer()

    def run(self):
        self.canvas.pack()
        self.display_menu()
        self.window.mainloop()

    def states_manager(self, state):
        self.state = state
        for button in self.buttons:
            button.destroy()
        for text in self.texts:
            self.canvas.delete(text)

        self.buttons = []
        self.texts = []

        if self.state == 'start' or self.state == 'continue' or self.state == 'resume':
            self.isPause = False
            self.play_game()

        else:
            self.isPause = True
            if self.state == 'menu':
                self.display_menu()

            if self.state == 'GameOver':
                self.display_game_over_menu()

            elif self.state == 'pause':
                self.display_pause_menu()

            elif self.state == 'leaderboard':
                self.display_leaderboard()

            elif self.state == 'controls':
                self.display_controls_menu()

    def play_game(self):
        if self.state == 'start' or self.state == 'continue':
            if self.state == 'start':
                self.coins_removed = []
            self.startUp()
        elif self.state == 'resume':
            self.change_objects_state('normal')
        for enemy in self.enemies:
            enemy.update()
        self.move_player()

    def make_enemies(self):
        for i in range(4):
            self.enemies.append(Enemy(self, i + 1))

    def makePlayer(self):
        if self.state == 'start' or self.state == 'resume':
            self.player = self.canvas.create_oval(PLAYER_COORDINATES, fill=PLAYER_COLOR)
        else:
            self.player = self.canvas.create_oval(self.player_coords, fill=PLAYER_COLOR)
            self.state = 'start'

    def makeRectangle(self):
        self.grid = self.canvas.create_rectangle(RECTANGLE_X1, RECTANGLE_Y1,
                                                 RECTANGLE_X2, RECTANGLE_Y2, outline="orange")

    def configure_controls(self):
        def moveLeft(event):
            self.direction = "left"

        def moveRight(event):
            self.direction = "right"

        def moveUp(event):
            self.direction = "up"

        def moveDown(event):
            self.direction = "down"

        def escKey(event):
            if self.state == 'start' or self.state == 'resume':
                self.states_manager('pause')

        def cheatKey(event):
            if self.playerSpeed < 4:
                self.playerSpeed += 0.2

        def bossKey(event):
            if not self.isPause:
                self.states_manager('pause')
            hide_window(self.window)

        self.canvas.bind(self.keySettings['left'], moveLeft)
        self.canvas.bind(self.keySettings['right'], moveRight)
        self.canvas.bind(self.keySettings['up'], moveUp)
        self.canvas.bind(self.keySettings['down'], moveDown)
        self.canvas.bind(self.keySettings['escape'], escKey)
        self.canvas.bind(self.keySettings['cheat'], cheatKey)
        self.canvas.bind(self.keySettings['boss'], bossKey)
        self.canvas.focus_set()

    def can_move(self):
        player_coords = self.canvas.coords(self.player)
        for wall in self.walls:
            if self.direction == 'left' and \
                    abs(player_coords[0] - (GRID_START_X + CELL_WIDTH * (wall[0] + 1))) < 2:
                if abs(player_coords[1] - (GRID_START_Y + CELL_HEIGHT * wall[1])) < 8:
                    self.direction = None

            elif self.direction == 'right' and abs(player_coords[2] - (GRID_START_X + CELL_WIDTH * wall[0])) < 3:
                if abs(player_coords[1] - (GRID_START_Y + CELL_HEIGHT * wall[1])) < 10:
                    self.direction = None

            elif self.direction == 'up' and abs(player_coords[1] - (GRID_START_Y + CELL_HEIGHT * (wall[1] + 1))) < 2:
                if abs(player_coords[0] - (GRID_START_X + CELL_WIDTH * wall[0])) < 4:
                    self.direction = None

            elif self.direction == 'down' and abs(player_coords[3] - (GRID_START_Y + CELL_HEIGHT * wall[1])) < 2:
                if abs(player_coords[0] - (GRID_START_X + CELL_WIDTH * wall[0])) < 4:
                    self.direction = None

    def move_player(self):
        def move_grid():
            """moving the rectangle"""
            if self.state == 'start' or self.state == 'resume':
                self.canvas.coords(self.grid,
                                   ((positions[0] + CELL_WIDTH // 2 - 1) // CELL_WIDTH) * CELL_WIDTH - 2,
                                   ((positions[1] + CELL_HEIGHT // 2 - 1) // CELL_HEIGHT) * CELL_HEIGHT + 6,
                                   ((positions[2] + CELL_WIDTH // 2 + 1) // CELL_WIDTH) * CELL_WIDTH - 2,
                                   ((positions[3] + CELL_HEIGHT // 2 + 1) // CELL_HEIGHT) * CELL_HEIGHT + 6)
                self.player_coords = self.canvas.coords(self.grid)

        def inGrid():
            if self.state == 'start' or self.state == 'resume':

                if self.direction == 'up' or self.direction == 'down':
                    offset = abs(((positions[0] - GRID_START_X) % CELL_WIDTH) - CELL_WIDTH)
                    if 3 < offset < 15:
                        self.direction = self.prev_direction

                if self.direction == 'left' or self.direction == 'right':
                    offset = abs(((positions[1] - GRID_START_Y) % CELL_HEIGHT) - CELL_HEIGHT)
                    if 3 < offset < 15:
                        self.direction = self.prev_direction

        self.canvas.pack()
        positions = self.canvas.coords(self.player)
        inGrid()
        coin_collision(self)
        self.can_move()

        if self.direction == 'left':
            self.canvas.move(self.player, -self.playerSpeed, 0)

        elif self.direction == 'right':
            self.canvas.move(self.player, self.playerSpeed, 0)

        elif self.direction == 'up':
            self.canvas.move(self.player, 0, -self.playerSpeed)

        elif self.direction == 'down':
            self.canvas.move(self.player, 0, self.playerSpeed)

        self.prev_direction = self.direction
        move_grid()

        if self.state == 'start' or self.state == 'resume':
            self.window.after(DELAY, self.move_player)

    def display_menu(self):
        self.display_menu_buttons()

    def display_menu_buttons(self):
        self.buttons.append(Button(self.window,
                                   text="New Game",
                                   width=BUTTON_WIDTH,
                                   height=BUTTON_HEIGHT,
                                   command=lambda: self.states_manager('start'))
                            )
        self.buttons[-1].place(x=BUTTON_1_X, y=BUTTON_1_Y)

        self.buttons.append(Button(self.window,
                                   text="Continue",
                                   width=BUTTON_WIDTH,
                                   height=BUTTON_HEIGHT,
                                   command=lambda: self.states_manager('continue')))
        self.buttons[-1].place(x=BUTTON_2_X, y=BUTTON_2_Y)

        self.buttons.append(Button(self.window,
                                   text="Leaderboard",
                                   width=BUTTON_WIDTH,
                                   height=BUTTON_HEIGHT,
                                   command=lambda: self.states_manager('leaderboard')))
        self.buttons[-1].place(x=BUTTON_3_X, y=BUTTON_3_Y)

        self.buttons.append(Button(self.window,
                                   text="Controls",
                                   width=BUTTON_WIDTH,
                                   height=BUTTON_HEIGHT,
                                   command=lambda: self.states_manager('controls')))
        self.buttons[-1].place(x=BUTTON_4_X, y=BUTTON_4_Y)

    def reset(self):
        self.direction = None
        self.prev_direction = None
        self.score = 0
        self.canvas.itemconfigure(self.player, state='hidden')
        # self.canvas.delete(self.gameBoard)
        self.canvas.delete(self.grid)
        for line in self.lines:
            self.canvas.delete(line)
        for enemy in self.enemies:
            enemy.direction = None
            self.canvas.itemconfigure(enemy.enemy, state='hidden')

        self.remove_coins()
        self.canvas.delete(self.scoreText)
        self.canvas.delete(self.highScoreText)

    def remove_coins(self):
        for coin in self.coins:
            self.canvas.delete(coin[2])

    def display_pause_menu(self):
        self.direction = None
        self.change_objects_state('hidden')
        self.display_pause_buttons()

    def change_objects_state(self, state):
        self.canvas.itemconfigure(self.player, state=state)
        # self.canvas.itemconfigure(self.gameBoard, state=state)
        self.canvas.itemconfigure(self.grid, state=state)
        for line in self.lines:
            self.canvas.itemconfigure(line, state=state)
        for enemy in self.enemies:
            enemy.direction = None
            self.canvas.itemconfigure(enemy.enemy, state=state)
            self.canvas.itemconfigure(enemy.grid, state=state)
        for wall in self.walls:
            self.canvas.itemconfigure(wall[2], state=state)
        for coin in self.coins:
            self.canvas.itemconfigure(coin[2], state=state)
        self.canvas.itemconfigure(self.scoreText, state=state)
        self.canvas.itemconfigure(self.highScoreText, state=state)

    def display_pause_buttons(self):
        self.buttons.append(Button(self.window,
                                   text="Resume",
                                   width=BUTTON_WIDTH,
                                   height=BUTTON_HEIGHT,
                                   command=lambda: self.states_manager('resume'))
                            )
        self.buttons[-1].place(x=BUTTON_1_X, y=BUTTON_1_Y)

        self.buttons.append(Button(self.window,
                                   text="Save",
                                   width=BUTTON_WIDTH,
                                   height=BUTTON_HEIGHT,
                                   command=lambda: save_game(self.canvas.coords(self.player),
                                                             self.coins_removed,
                                                             self.buttons[1]))
                            )
        self.buttons[-1].place(x=BUTTON_2_X, y=BUTTON_2_Y)

        self.buttons.append(Button(self.window,
                                   text="Menu",
                                   width=BUTTON_WIDTH,
                                   height=BUTTON_HEIGHT,
                                   command=lambda: self.states_manager('menu'))
                            )
        self.buttons[-1].place(x=BUTTON_3_X, y=BUTTON_3_Y)

    def display_controls_menu(self):

        self.buttons.append(Button(self.window,
                                   text=self.keySettings['left'],
                                   width=BUTTON_WIDTH,
                                   height=BUTTON_HEIGHT,
                                   font=('Arial', BUTTON_TEXT_SIZE),
                                   command=lambda: self.onButtonPress('left'))
                            )
        self.buttons[-1].place(x=BUTTON_1_X, y=BUTTON_1_Y)

        self.texts.append(self.canvas.create_text(CONTROL_TEXTS_X,
                                                  BUTTON_1_Y + TEXTS_OFFSET,
                                                  font=('Arial', TEXTS_SIZE),
                                                  text='Left Direction',
                                                  fill='white'))

        self.buttons.append(Button(self.window,
                                   text=self.keySettings['right'],
                                   width=BUTTON_WIDTH,
                                   height=BUTTON_HEIGHT,
                                   font=('Arial', BUTTON_TEXT_SIZE),
                                   command=lambda: self.onButtonPress('right'))
                            )
        self.buttons[-1].place(x=BUTTON_2_X, y=BUTTON_2_Y)

        self.texts.append(self.canvas.create_text(CONTROL_TEXTS_X,
                                                  BUTTON_2_Y + TEXTS_OFFSET,
                                                  font=('Arial', TEXTS_SIZE),
                                                  text='Right Direction',
                                                  fill='white'))

        self.buttons.append(Button(self.window,
                                   text=self.keySettings['up'],
                                   width=BUTTON_WIDTH,
                                   height=BUTTON_HEIGHT,
                                   font=('Arial', BUTTON_TEXT_SIZE),
                                   command=lambda: self.onButtonPress('up'))
                            )
        self.buttons[-1].place(x=BUTTON_3_X, y=BUTTON_3_Y)

        self.texts.append(self.canvas.create_text(CONTROL_TEXTS_X,
                                                  BUTTON_3_Y + TEXTS_OFFSET,
                                                  font=('Arial', TEXTS_SIZE),
                                                  text='Up Direction',
                                                  fill='white'))

        self.buttons.append(Button(self.window,
                                   text=self.keySettings['down'],
                                   width=BUTTON_WIDTH,
                                   height=BUTTON_HEIGHT,
                                   font=('Arial', BUTTON_TEXT_SIZE),
                                   command=lambda: self.onButtonPress('down'))
                            )
        self.buttons[-1].place(x=BUTTON_4_X, y=BUTTON_4_Y)

        self.texts.append(self.canvas.create_text(CONTROL_TEXTS_X,
                                                  BUTTON_4_Y + TEXTS_OFFSET,
                                                  font=('Arial', TEXTS_SIZE),
                                                  text='Down Direction',
                                                  fill='white'))

        self.buttons.append(Button(self.window,
                                   text=self.keySettings['escape'],
                                   width=BUTTON_WIDTH,
                                   height=BUTTON_HEIGHT,
                                   font=('Arial', BUTTON_TEXT_SIZE),
                                   command=lambda: self.onButtonPress('escape'))
                            )
        self.buttons[-1].place(x=BUTTON_5_X, y=BUTTON_5_Y)

        self.texts.append(self.canvas.create_text(CONTROL_TEXTS_X,
                                                  BUTTON_5_Y + TEXTS_OFFSET,
                                                  font=('Arial', TEXTS_SIZE),
                                                  text='Pause',
                                                  fill='white'))

        self.buttons.append(Button(self.window,
                                   text=self.keySettings['cheat'],
                                   width=BUTTON_WIDTH,
                                   height=BUTTON_HEIGHT,
                                   font=('Arial', BUTTON_TEXT_SIZE),
                                   command=lambda: self.onButtonPress('cheat'))
                            )
        self.buttons[-1].place(x=BUTTON_6_X, y=BUTTON_6_Y)

        self.texts.append(self.canvas.create_text(CONTROL_TEXTS_X - 100,
                                                  BUTTON_6_Y + TEXTS_OFFSET,
                                                  font=('Arial', TEXTS_SIZE),
                                                  text='Cheat (increase Player speed)',
                                                  fill='white'))

        self.buttons.append(Button(self.window,
                                   text=self.keySettings['boss'],
                                   width=BUTTON_WIDTH,
                                   height=BUTTON_HEIGHT,
                                   font=('Arial', BUTTON_TEXT_SIZE),
                                   command=lambda: self.onButtonPress('boss'))
                            )
        self.buttons[-1].place(x=BUTTON_7_X, y=BUTTON_7_Y)

        self.texts.append(self.canvas.create_text(CONTROL_TEXTS_X,
                                                  BUTTON_7_Y + TEXTS_OFFSET,
                                                  font=('Arial', TEXTS_SIZE),
                                                  text='Boss Key',
                                                  fill='white'))

        self.buttons.append(Button(self.window,
                                   text=self.keySettings['difficulty'],
                                   width=BUTTON_WIDTH,
                                   height=BUTTON_HEIGHT,
                                   font=('Arial', BUTTON_TEXT_SIZE),
                                   command=lambda: self.onButtonPress('difficulty'))
                            )
        self.buttons[-1].place(x=BUTTON_8_X, y=BUTTON_8_Y)

        self.texts.append(self.canvas.create_text(CONTROL_TEXTS_X,
                                                  BUTTON_8_Y + TEXTS_OFFSET,
                                                  font=('Arial', TEXTS_SIZE),
                                                  text='Difficulty',
                                                  fill='white'))

        self.buttons.append(Button(self.window,
                                   text="Menu",
                                   width=BUTTON_WIDTH,
                                   height=BUTTON_HEIGHT,
                                   command=lambda: self.states_manager('menu'))
                            )
        self.buttons[-1].place(x=100, y=100)

    def onButtonPress(self, key):
        if key == 'difficulty':
            self.keySettings[key] = 'hard' if self.keySettings[key] == 'normal' else 'normal'
            self.buttons[7].configure(text=self.keySettings[key])
            update_default_key_settings(self.keySettings)

        else:
            for i, (_, control_name) in enumerate(self.keySettings.items()):
                self.buttons[i].configure(background='white', text=control_name)

            button_index = list(self.keySettings).index(key)
            self.buttons[button_index].configure(text='Press a Key')

            self.new_key = self.window.bind('<Key>', lambda event: change_key(event))

        def change_key(event, callfrom):
            key_name = '<' + event.keysym + '>'
            if key_name == '<??>':
                self.buttons[button_index].configure(background='red', text='Error!')

            elif key_name in self.keySettings.values():
                self.buttons[button_index].configure(background='red', text='Already Used!')

            else:
                self.window.unbind('<Key>', self.new_key)
                self.buttons[button_index].configure(text=key_name)
                self.keySettings[key] = key_name

            self.configure_controls()
            update_default_key_settings(self.keySettings)

    def display_leaderboard(self):
        self.texts.append(self.canvas.create_text(LEADERBOARD_X_POSITION,
                                                  LEADERBOARD_Y_POSITION,
                                                  font=('Arial', 40),
                                                  text='Leaderboard (Top 5)',
                                                  fill='green'))

        self.texts.append(self.canvas.create_text(NAMES_X_POSITION,
                                                  NAMES_Y_POSITION,
                                                  font=('Arial', 30),
                                                  text='Name',
                                                  fill='white'))

        self.texts.append(self.canvas.create_text(SCORES_X_POSITION,
                                                  SCORES_Y_POSITION,
                                                  font=('Arial', 30),
                                                  text='Scores',
                                                  fill='white'))

        self.buttons.append(Button(self.window,
                                   text="Menu",
                                   width=BUTTON_WIDTH,
                                   height=BUTTON_HEIGHT,
                                   command=lambda: self.states_manager('menu'))
                            )
        self.buttons[-1].place(x=100, y=100)

        for i in range(min(5, len(self.leaderboard))):
            name = self.leaderboard['names'][i]
            score = self.leaderboard['scores'][i]

            self.texts.append(self.canvas.create_text(NAMES_X_POSITION,
                                                      NAMES_Y_POSITION + 50 + i * 30,
                                                      text=str(i + 1),
                                                      font=('Arial', 22),
                                                      ))

            self.texts.append(self.canvas.create_text(NAMES_X_POSITION,
                                                      NAMES_Y_POSITION + 50 + i * 30,
                                                      text=name,
                                                      font=('Arial', 22),
                                                      ))

            self.texts.append(self.canvas.create_text(SCORES_X_POSITION,
                                                      SCORES_Y_POSITION + 50 + i * 30,
                                                      anchor='center',
                                                      text=score,
                                                      font=('Arial', 22),
                                                      ))

    def display_game_over_menu(self):
        self.direction = None
        self.change_objects_state('hidden')
        img = PhotoImage(file="../GameBoard/GAME_OVER.png")
        self.canvas.create_image(200, 200, anchor=NW, image=img)
        self.buttons.append(Button(self.window,
                                   text="Menu",
                                   width=BUTTON_WIDTH,
                                   height=BUTTON_HEIGHT,
                                   command=lambda: self.states_manager('menu'))
                            )
        self.buttons[-1].place(x=100, y=100)




