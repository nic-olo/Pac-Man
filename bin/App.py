from CanvasManager import *  # TODO specify the modules!!!!
from WindowManager import *
from MazeRender import *
from SavingMananger import *
from sys import exit
from Enemy import Enemy
from Player import Player


class App:
    def __init__(self):
        """initialize the game"""
        self.hideWindow = False
        self.texts = []
        self.buttons = []
        self.window = makeWindow()
        self.canvas = makeCanvas(self.window)
        # self.image = setImage(MAZE_PATH)
        self.settings = load_settings()
        self.configure_controls()
        self.coins_removed = []
        self.player_direction = None
        self.leaderboard = load_leaderboard()
        self.prev_direction = None
        self.isPause = True
        self.state = "menu"
        self.score = 0
        self.enemies = []

    def run(self):
        """run the game"""
        self.canvas.pack()
        self.display_menu()
        self.window.mainloop()

    def startUp(self):
        self.canvas.bind()
        """creating all the objects needed to play"""
        # self.gameBoard = self.canvas.create_image(640, 320, anchor=CENTER, image=self.image)
        self.lines = make_lines(self.canvas)
        self.make_grid()
        self.walls = make_walls(MAZE_COORDINATES_PATH, self.canvas)
        self.coins = coins_renderer(MAZE_COORDINATES_PATH, self.canvas, self.coins_removed, self.state)

        try:
            self.scoreText, self.highScoreText = display_scores(self.canvas, self.score, self.leaderboard[0]['score'])
        except IndexError:
            self.scoreText, self.highScoreText = display_scores(self.canvas, self.score, 0)

        self.make_sprites()
        self.state = 'start'

    def states_manager(self, state):
        """This methods manages all the links between the various game windows by creating and destroying
        the objects accordingly by calling other methods"""

        """try:
            self.color.destroy()
        except:
            pass"""
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
            self.player_direction = None
            if self.state == 'menu':
                self.display_menu()

            if self.state == 'GameOver':
                self.display_game_over_menu()

            elif self.state == 'pause':
                self.display_pause_menu()

            elif self.state == 'leaderboard':
                self.display_leaderboard()

            elif self.state == 'controls':
                self.display_options_menu()

    def play_game(self):
        """start the game"""
        if self.state == 'continue':
            try:
                self.player_coords, self.enemies_coords, self.coins_removed, self.score = continue_game()

            except FileNotFoundError:
                self.state = 'start'
                self.coins_removed = []

            self.startUp()

        elif self.state == 'start':
            self.coins_removed = []
            self.startUp()

        elif self.state == 'resume':
            self.change_objects_state('normal')

        self.player.update()
        for enemy in self.enemies:
            enemy.update()

    def make_sprites(self):
        """create the player and the enemies"""
        for i in range(4):
            self.enemies.append(Enemy(self, i + 1))
        self.player = Player(self)

    def make_grid(self):
        """make the grid surrounding the player"""
        self.grid = self.canvas.create_rectangle(RECTANGLE_X1, RECTANGLE_Y1,
                                                 RECTANGLE_X2, RECTANGLE_Y2,
                                                 outline=PLAYER_COLOR
                                                 )
        self.canvas.itemconfigure(self.grid, state='hidden')

    def configure_controls(self):
        """binds the controls the linked action"""

        def moveLeft(event):
            self.player_direction = "left"

        def moveRight(event):
            self.player_direction = "right"

        def moveUp(event):
            self.player_direction = "up"

        def moveDown(event):
            self.player_direction = "down"

        def escKey(event):
            if self.state == 'start' or self.state == 'resume':
                self.states_manager('pause')

        def cheatKey(event):
            if self.player.player_speed < 4:
                self.player.player_speed += 0.2

        def bossKey(event):
            if not self.isPause:
                self.states_manager('pause')
            self.hide_window()

        self.canvas.bind(self.settings['left'], moveLeft)
        self.canvas.bind(self.settings['right'], moveRight)
        self.canvas.bind(self.settings['up'], moveUp)
        self.canvas.bind(self.settings['down'], moveDown)
        self.canvas.bind(self.settings['escape'], escKey)
        self.canvas.bind(self.settings['cheat'], cheatKey)
        self.canvas.bind(self.settings['boss'], bossKey)
        self.canvas.focus_set()

    def display_menu(self):
        """display the menu"""
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
                                   text="Options",
                                   width=BUTTON_WIDTH,
                                   height=BUTTON_HEIGHT,
                                   command=lambda: self.states_manager('controls')))
        self.buttons[-1].place(x=BUTTON_4_X, y=BUTTON_4_Y)

    def reset(self):
        """resets the game"""
        self.player_direction = None
        self.prev_direction = None
        self.score = 0
        self.canvas.itemconfigure(self.player.player, state='hidden')
        # self.canvas.delete(self.gameBoard)
        self.canvas.delete(self.grid)
        for line in self.lines:
            self.canvas.delete(line)
        for enemy in self.enemies:
            enemy.player_direction = None
            self.canvas.itemconfigure(enemy.enemy, state='hidden')

        self.remove_coins()
        self.canvas.delete(self.scoreText)
        self.canvas.delete(self.highScoreText)

    def remove_coins(self):
        """remove the coins when continuing an old game"""
        for coin in self.coins:
            self.canvas.delete(coin[2])

    def display_pause_menu(self):
        """display the menu when the game is paused"""
        self.player_direction = None
        self.change_objects_state('hidden')
        self.display_pause_buttons()

    def change_objects_state(self, state):
        """change the state of the objects between hidden and normal"""
        self.canvas.itemconfigure(self.player.player, state=state)
        # self.canvas.itemconfigure(self.gameBoard, state=state)
        # self.canvas.itemconfigure(self.grid, state=state)
        # for line in self.lines:
        # self.canvas.itemconfigure(line, state=state)
        for enemy in self.enemies:
            enemy.player_direction = None
            self.canvas.itemconfigure(enemy.enemy, state=state)
            # self.canvas.itemconfigure(enemy.grid, state=state)
        for wall in self.walls:
            self.canvas.itemconfigure(wall[2], state=state)
        for coin in self.coins:
            self.canvas.itemconfigure(coin[2], state=state)
        self.canvas.itemconfigure(self.scoreText, state=state)
        self.canvas.itemconfigure(self.highScoreText, state=state)

    def display_pause_buttons(self):
        """display the buttons when the game is paused"""
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
                                   command=lambda: save_game(self.canvas.coords(self.player.player),
                                                             list(self.canvas.coords(self.enemies[i].enemy) for i in
                                                                  range(4)),
                                                             self.coins_removed,
                                                             self.score,
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

    def display_options_menu(self):
        """display the options menu"""
        self.buttons.append(Button(self.window,
                                   text=self.settings['left'],
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
                                   text=self.settings['right'],
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
                                   text=self.settings['up'],
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
                                   text=self.settings['down'],
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
                                   text=self.settings['escape'],
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
                                   text=self.settings['cheat'],
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
                                   text=self.settings['boss'],
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
                                   text=self.settings['difficulty'],
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

        """self.buttons.append(Button(self.window,
                                   text='Confirm',
                                   width=BUTTON_WIDTH,
                                   height=BUTTON_HEIGHT,
                                   font=('Arial', BUTTON_TEXT_SIZE),
                                   command=lambda: self.change_color())
                            )
        self.buttons[-1].place(x=BUTTON_9_X, y=BUTTON_9_Y)

        self.color = Entry(self.window,
                           font=('Arial', 25),
                           width=9)

        self.color.place(x=COLOR_ENTRY_X, y=COLOR_ENTRY_Y)

        self.texts.append(self.canvas.create_text(CONTROL_TEXTS_X,
                                                  BUTTON_9_Y + TEXTS_OFFSET,
                                                  font=('Arial', TEXTS_SIZE),
                                                  text='Player Color',
                                                  fill='white'))"""

        self.buttons.append(Button(self.window,
                                   text="Menu",
                                   width=BUTTON_WIDTH,
                                   height=BUTTON_HEIGHT,
                                   command=lambda: self.states_manager('menu'))
                            )
        self.buttons[-1].place(x=100, y=100)

    """def change_color(self):
        new_color = self.color.get().strip()
        Button(background=new_color)
        self.player_color = new_color
        self.settings['color'] = new_color
        self.window.unbind('<Key>', self.color)
        update_settings(self.settings)"""

    def onButtonPress(self, key):
        """change the options when a button is pressed"""
        if key == 'difficulty':
            self.settings[key] = 'hard' if self.settings[key] == 'normal' else 'normal'
            self.buttons[7].configure(text=self.settings[key])
            update_settings(self.settings)

        else:
            for i, (_, control_name) in enumerate(self.settings.items()):
                self.buttons[i].configure(background='white', text=control_name)

            button_index = list(self.settings).index(key)
            self.buttons[button_index].configure(text='Press a Key')

            self.new_key = self.window.bind('<Key>', lambda event: change_key(event))

        def change_key(event):
            key_name = '<' + event.keysym + '>'
            self.window.unbind('<Key>', self.new_key)
            if key_name in self.settings.values():
                self.buttons[button_index].configure(background='red', text='Already Used!')
            else:
                self.buttons[button_index].configure(text=key_name)
                self.settings[key] = key_name

            self.configure_controls()
            update_settings(self.settings)

    def display_leaderboard(self):
        """display the leaderboard"""
        self.texts.append(self.canvas.create_text(LEADERBOARD_X_POSITION,
                                                  LEADERBOARD_Y_POSITION,
                                                  font=('Arial', 40),
                                                  text='Leaderboard (Top 8)',
                                                  fill='green'))

        self.texts.append(self.canvas.create_text(NAMES_X_POSITION,
                                                  NAMES_Y_POSITION,
                                                  font=('Arial', 30),
                                                  text='Name',
                                                  fill='white'))

        self.texts.append(self.canvas.create_text(SCORES_X_POSITION,
                                                  SCORES_Y_POSITION,
                                                  font=('Arial', 30),
                                                  text='Score',
                                                  fill='white'))

        self.buttons.append(Button(self.window,
                                   text="Menu",
                                   width=BUTTON_WIDTH,
                                   height=BUTTON_HEIGHT,
                                   command=lambda: self.states_manager('menu'))
                            )
        self.buttons[-1].place(x=100, y=100)

        for i in range(min(8, len(self.leaderboard))):
            name = self.leaderboard[i]['name']
            score = self.leaderboard[i]['score']

            self.texts.append(self.canvas.create_text(NAMES_X_POSITION - 180,
                                                      NAMES_Y_POSITION + 50 + i * 40,
                                                      text=str(i + 1),
                                                      font=('Arial', 22),
                                                      fill='white'
                                                      ))

            self.texts.append(self.canvas.create_text(NAMES_X_POSITION,
                                                      NAMES_Y_POSITION + 50 + i * 40,
                                                      text=name,
                                                      font=('Arial', 22),
                                                      fill='white'
                                                      ))

            self.texts.append(self.canvas.create_text(SCORES_X_POSITION,
                                                      SCORES_Y_POSITION + 50 + i * 40,
                                                      text=score,
                                                      font=('Arial', 22),
                                                      fill='white'
                                                      ))

    def display_game_over_menu(self):
        """display the menu when the game is over"""
        self.change_objects_state('hidden')
        image = GAME_OVER_IMAGE_PATH if self.coins else WINNER_IMAGE_PATH
        self.img = PhotoImage(file=image)
        self.image = self.canvas.create_image(WINDOW_WIDTH // 2 + 20, 320, image=self.img, anchor=CENTER)

        self.texts.append(self.canvas.create_text(GAME_OVER_SCORE_X,
                                                  GAME_OVER_SCORE_Y,
                                                  font=('Arial', 60, 'bold'),
                                                  text=f'SCORE: {self.score}',
                                                  fill='black'))

        self.texts.append(self.canvas.create_text(GAME_OVER_TEXT_ENTRY_X,
                                                  GAME_OVER_TEXT_ENTRY_Y,
                                                  font=('Arial', TEXTS_SIZE, 'bold'),
                                                  text='ENTER YOUR NAME',
                                                  fill='#000000'))

        self.user = Entry(self.window,
                          font='Arial',
                          width=20)

        self.user.place(x=GAME_OVER_ENTRY_X, y=GAME_OVER_ENTRY_Y)
        self.texts.append(self.canvas.create_text(GAME_OVER_SCORE_X,
                                                  ERROR_MESSAGE_Y,
                                                  font=('Arial', 30, 'bold'),
                                                  fill='red'))
        self.buttons.append(Button(self.window,
                                   text="Confirm",
                                   font='Arial',
                                   command=lambda: self.save_user()
                                   ))

        self.buttons[-1].place(x=GAME_OVER_BUTTON_X, y=GAME_OVER_BUTTON_Y)

    def save_user(self):
        """save the name and the score of the user"""
        user_entry = self.user.get().strip()

        if not user_entry:
            self.canvas.itemconfigure(self.texts[-1], text='Empty Name!')
            return
        if len(user_entry) > 12:
            self.canvas.itemconfigure(self.texts[-1], text='Name too Long!')
            return

        data = {'name': user_entry, 'score': self.score}
        for i in range(len(self.leaderboard)):
            if self.score > self.leaderboard[i]['score']:
                self.leaderboard.insert(i, data)
                break
        else:
            self.leaderboard.append(data)

        save_score(self.leaderboard)
        self.user.destroy()
        exit()

    def hide_window(self):
        if not self.hideWindow:
            self.hideCanvas = Canvas(self.window, background='black',
                                     width=WINDOW_WIDTH, height=WINDOW_HEIGHT, highlightthickness=0)
            self.hideCanvas.place(x=0, y=0)
            """hideWindow = Canvas(window,
                                width=WINDOW_WIDTH,
                                height=WINDOW_HEIGHT)"""
            self.window.title("ThingsToDo.txt")
            self.img = PhotoImage(file=BOSS_KEY_DOCUMENT_PATH)
            self.boss = self.hideCanvas.create_image(0, -25, image=self.img, anchor=NW)
            self.hideWindow = True

        else:
            self.hideCanvas.destroy()
            self.window.title("Pac-Man")
            self.hideWindow = False
