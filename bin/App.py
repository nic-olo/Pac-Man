from tkinter import CENTER

from CanvasManager import *
from WindowManager import *
from MazeRender import *


# from Player import Player


class App:
    def __init__(self):
        self.buttons = []
        self.window = makeWindow()
        self.canvas = makeCanvas(self.window)
        self.image = setImage(MAZE_PATH)
        self.direction = None
        self.prev_direction = None
        self.state = "menu"
        self.score = 0

    def startUp(self):
        self.gameBoard = self.canvas.create_image(640, 320, anchor=CENTER, image=self.image)
        self.lines = makeLines(self.canvas)
        self.makeRectangle()
        self.walls = wallsCoordinates(MAZE_COORDINATES_PATH)
        self.coins = coinsRender(MAZE_COORDINATES_PATH, self.canvas)
        self.scoreText, self.highScoreText = display_scores(self.canvas)
        self.makePlayer()
        self.configure_buttons()

    def run(self):
        self.canvas.pack()
        self.display_menu()
        self.window.mainloop()

    def states_manager(self, state):
        self.state = state
        if self.state == 'start' or self.state == 'resume':
            self.play_game()

        elif self.state == 'menu':
            self.reset()

            self.display_menu()

        if self.state == 'pause':
            self.display_pause_menu()

    def play_game(self):
        for button in self.buttons:
            button.destroy()
        if self.state == 'start':
            self.startUp()
        elif self.state == 'resume':
            self.change_objects_state('normal')
        self.movePlayer()

    def makePlayer(self):
        self.player = self.canvas.create_oval(PLAYER_X1, PLAYER_Y1, PLAYER_X2, PLAYER_Y2, fill=PLAYER_COLOR)

    def makeRectangle(self):
        self.grid = self.canvas.create_rectangle(RECTANGLE_X1, RECTANGLE_Y1,
                                                  RECTANGLE_X2, RECTANGLE_Y2, outline="orange")

    def leftKey(self, event):
        self.direction = "left"

    def rightKey(self, event):
        self.direction = "right"

    def upKey(self, event):
        self.direction = "up"

    def downKey(self, event):
        self.direction = "down"

    def escKey(self, event):
        if self.state == 'start' or self.state == 'resume':
            self.states_manager('pause')

    def configure_buttons(self):
        self.canvas.bind("<Left>", self.leftKey)
        self.canvas.bind("<Right>", self.rightKey)
        self.canvas.bind("<Up>", self.upKey)
        self.canvas.bind("<Down>", self.downKey)
        self.canvas.bind("<Escape>", self.escKey)
        self.canvas.focus_set()

    def inGrid(self):
        if self.state == 'start' or self.state == 'resume':
            if not (((self.positions[0] + self.positions[2]) // 2 - GRID_START_X) % CELL_WIDTH < 10):
                if self.direction == 'up' or self.direction == 'down':
                    self.direction = self.prev_direction

            elif not (((self.positions[1] + self.positions[3]) // 2 - GRID_START_Y) % CELL_HEIGHT < 10):
                if self.direction == 'left' or self.direction == 'right':
                    self.direction = self.prev_direction

    def canMove(self):
        player_coords = self.canvas.coords(self.player)
        for wall in self.walls:
            if self.direction == 'left' and \
                    abs(player_coords[0] - (GRID_START_X + CELL_WIDTH * (wall[0] + 1))) < 2:
                if abs(player_coords[1] - (GRID_START_Y + CELL_HEIGHT * wall[1])) < 10:
                    self.direction = None

            elif self.direction == 'right' and abs(player_coords[2] - (GRID_START_X + CELL_WIDTH * wall[0])) < 2:
                if abs(player_coords[1] - (GRID_START_Y + CELL_HEIGHT * wall[1])) < 10:
                    self.direction = None

            elif self.direction == 'up' and abs(player_coords[1] - (GRID_START_Y + CELL_HEIGHT * (wall[1] + 1))) < 2:
                if abs(player_coords[0] - (GRID_START_X + CELL_WIDTH * wall[0])) < 10:
                    self.direction = None

            elif self.direction == 'down' and abs(player_coords[3] - (GRID_START_Y + CELL_HEIGHT * wall[1])) < 2:
                if abs(player_coords[0] - (GRID_START_X + CELL_WIDTH * wall[0])) < 10:
                    self.direction = None

    def coinCollision(self):
        for coin in self.coins:
            player_coords = self.canvas.coords(self.player)
            t = False
            if self.direction == 'left' and \
                    abs(player_coords[0] - (GRID_START_X + CELL_WIDTH * coin[0] - COIN_SIZE_X)) < 20:
                if abs(player_coords[1] - (GRID_START_Y + CELL_HEIGHT * coin[1])) < 10:
                    t = True

            elif self.direction == 'right' and abs(
                    player_coords[2] - (GRID_START_X + CELL_WIDTH * coin[0] + COIN_SIZE_X)) < 2:
                if abs(player_coords[1] - (GRID_START_Y + CELL_HEIGHT * coin[1])) < 10:
                    t = True

            elif self.direction == 'up' and abs(
                    player_coords[1] - (GRID_START_Y + CELL_HEIGHT * coin[1] - COIN_SIZE_Y)) < 20:
                if abs(player_coords[0] - (GRID_START_X + CELL_WIDTH * coin[0])) < 10:
                    t = True

            elif self.direction == 'down' and abs(
                    player_coords[3] - (GRID_START_Y + CELL_HEIGHT * coin[1] + COIN_SIZE_Y)) < 2:
                if abs(player_coords[0] - (GRID_START_X + CELL_WIDTH * coin[0])) < 10:
                    t = True

            if t:
                self.canvas.delete(coin[2])
                self.coins.remove(coin)
                self.score += 1
                update_score(self.canvas, self.scoreText, self.score)

    #    (GRID_START_X + CELL_WIDTH * wall[0],
    #     GRID_START_Y + CELL_HEIGHT * wall[1],
    #     GRID_START_X + CELL_WIDTH * wall[0] + CELL_WIDTH,
    #     GRID_START_Y + CELL_HEIGHT * wall[1] + CELL_HEIGHT)

    def movePlayer(self):
        self.canvas.pack()
        self.positions = self.canvas.coords(self.player)
        self.inGrid()
        self.coinCollision()
        self.canMove()
        if self.direction == 'left':
            self.canvas.move(self.player, -PLAYER_SPEED, 0)

        elif self.direction == 'right':
            self.canvas.move(self.player, PLAYER_SPEED, 0)

        elif self.direction == 'up':
            self.canvas.move(self.player, 0, -PLAYER_SPEED)

        elif self.direction == 'down':
            self.canvas.move(self.player, 0, PLAYER_SPEED)

        self.prev_direction = self.direction

        """moving the rectangle"""
        self.move_grid()

        self.window.after(DELAY, self.movePlayer)

    def move_grid(self):
        if self.state == 'start' or self.state == 'resume':
            self.canvas.coords(self.grid,
                               ((self.positions[0] + CELL_WIDTH // 2 - 1) // CELL_WIDTH) * CELL_WIDTH - 2,
                               ((self.positions[1] + CELL_HEIGHT // 2 - 1) // CELL_HEIGHT) * CELL_HEIGHT + 6,
                               ((self.positions[2] + CELL_WIDTH // 2 + 1) // CELL_WIDTH) * CELL_WIDTH - 2,
                               ((self.positions[3] + CELL_HEIGHT // 2 + 1) // CELL_HEIGHT) * CELL_HEIGHT + 6)

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
                                   text="CONTINUE",
                                   width=BUTTON_WIDTH,
                                   height=BUTTON_HEIGHT))
        self.buttons[-1].place(x=BUTTON_2_X, y=BUTTON_2_Y)

        self.buttons.append(Button(self.window,
                                   text="LEADERBOARD",
                                   width=BUTTON_WIDTH,
                                   height=BUTTON_HEIGHT))
        self.buttons[-1].place(x=BUTTON_3_X, y=BUTTON_3_Y)

        self.buttons.append(Button(self.window,
                                   text="CONTROLS",
                                   width=BUTTON_WIDTH,
                                   height=BUTTON_HEIGHT))
        self.buttons[-1].place(x=BUTTON_4_X, y=BUTTON_4_Y)

    def reset(self):
        self.direction = None
        self.prev_direction = None
        self.score = 0
        self.canvas.itemconfigure(self.player, state='hidden')
        self.canvas.delete(self.gameBoard)
        self.canvas.delete(self.grid)
        for line in self.lines:
            self.canvas.delete(line)
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
        self.canvas.itemconfigure(self.gameBoard, state=state)
        self.canvas.itemconfigure(self.grid, state=state)
        for line in self.lines:
            self.canvas.itemconfigure(line, state=state)
        for coin in self.coins:
            self.canvas.itemconfigure(coin[2], state=state)
        self.canvas.itemconfigure(self.scoreText, state=state)
        self.canvas.itemconfigure(self.highScoreText, state=state)

    def display_pause_buttons(self):
        self.buttons.append(Button(self.window,
                                   text="Continue",
                                   width=BUTTON_WIDTH,
                                   height=BUTTON_HEIGHT,
                                   command=lambda: self.states_manager('resume'))
                            )
        self.buttons[-1].place(x=BUTTON_1_X, y=BUTTON_1_Y)

        self.buttons.append(Button(self.window,
                                   text="Save",
                                   width=BUTTON_WIDTH,
                                   height=BUTTON_HEIGHT)
                            )
        self.buttons[-1].place(x=BUTTON_2_X, y=BUTTON_2_Y)

        self.buttons.append(Button(self.window,
                                   text="Menu",
                                   width=BUTTON_WIDTH,
                                   height=BUTTON_HEIGHT)
                            )
        self.buttons[-1].place(x=BUTTON_3_X, y=BUTTON_3_Y)