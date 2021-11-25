from settings import *
from random import randint
from time import time


class Enemy:
    def __init__(self, app, enemy_number):
        """initialize the enemy"""
        self.walls = []
        self.app = app
        self.direction = None
        self.prev_direction = None
        self.enemy_number = enemy_number
        self.canvas = self.app.canvas
        self.enemy_coords = []
        self.target = None
        self.enemy_speed = HARD_ENEMY_SPEEDS[self.enemy_number - 1] if \
            self.app.settings['difficulty'] == 'hard' \
            else NORMAL_ENEMY_SPEEDS[self.enemy_number - 1]  # set the speed
        # of the enemies according to the difficulty of the game
        self.enemy_color = ENEMY_COLORS[self.enemy_number - 1]
        self.make_enemy()
        self.make_enemy_grid()
        self.prev_time = time()

    def make_enemy(self):
        """create the enemy"""
        if self.app.state == 'continue':
            self.enemy = self.canvas.create_oval(
                self.app.enemies_coords[self.enemy_number - 1],
                fill=self.enemy_color)
            return

        with open(MAZE_COORDINATES_PATH, 'r') as file:
            # reads a txt file that contains the coordinates of the enemies
            # which are then displaced accordingly
            for i in range(GRID_ROWS):
                line = file.readline()
                for j in range(GRID_COLUMNS):
                    if line[j] == str(self.enemy_number):
                        enemy_pos = [j, i]
                        break

        self.enemy = self.canvas.create_oval(
            GRID_START_X + CELL_WIDTH * enemy_pos[0] + ENEMY_X1,
            GRID_START_Y + CELL_HEIGHT * enemy_pos[1] + ENEMY_Y1,
            GRID_START_X + CELL_WIDTH * (enemy_pos[0]) + ENEMY_X2,
            GRID_START_Y + CELL_HEIGHT * (enemy_pos[1]) + ENEMY_Y2,
            fill=self.enemy_color
        )

    def make_enemy_grid(self):
        """create a grid that surrounds the enemy"""
        self.grid = self.canvas.create_rectangle(
            GRID_X1,
            GRID_Y1,
            GRID_X2, GRID_Y2,
            outline=self.enemy_color
        )

        self.canvas.itemconfigure(self.grid, state='hidden')

    def update(self):
        """update the enemy movement"""
        self.move_enemy()
        if self.app.state == 'start' or self.app.state == 'resume':
            self.app.window.after(DELAY, self.update)

    def can_move(self):
        """block the player from passing through a wall"""
        for wall in self.app.walls:
            if self.direction == 'left' and abs(self.enemy_coords[0] - (
                    GRID_START_X + CELL_WIDTH * (wall[0] + 1))) < 5 and \
                    abs(
                        self.enemy_coords[1] - (GRID_START_Y +
                                                CELL_HEIGHT * wall[1])) < 12:
                self.direction = None

            elif self.direction == 'right' and abs(self.enemy_coords[2] - (
                    GRID_START_X + CELL_WIDTH * wall[0])) < 5 and \
                    abs(
                        self.enemy_coords[1] - (GRID_START_Y +
                                                CELL_HEIGHT * wall[1])) < 12:
                self.direction = None

            elif self.direction == 'up' and abs(
                    self.enemy_coords[1] - (GRID_START_Y + CELL_HEIGHT *
                                            (wall[1] + 1))) < 5 and \
                    abs(
                        self.enemy_coords[0] - (GRID_START_X +
                                                CELL_WIDTH * wall[0])) < 12:
                self.direction = None

            elif self.direction == 'down' and abs(
                    self.enemy_coords[3] - (GRID_START_Y +
                                            CELL_HEIGHT * wall[1])) < 5 and \
                    abs(
                        self.enemy_coords[0] - (GRID_START_X +
                                                CELL_WIDTH * wall[0])) < 12:
                self.direction = None

    def move_enemy(self):
        """check the position of the enemy and move it"""
        self.enemy_coords = self.canvas.coords(self.enemy)

        def move_grid():
            """move the grid"""
            self.canvas.coords(
                self.grid,
                ((self.enemy_coords[0] + CELL_WIDTH // 2) // CELL_WIDTH) *
                CELL_WIDTH + 4,
                ((self.enemy_coords[1] + CELL_HEIGHT // 2) // CELL_HEIGHT) *
                CELL_HEIGHT + 6,
                ((self.enemy_coords[2] + CELL_WIDTH // 2) // CELL_WIDTH) *
                CELL_WIDTH + 4,
                ((self.enemy_coords[3] + CELL_HEIGHT // 2) // CELL_HEIGHT) *
                CELL_HEIGHT + 6
            )

        def inGrid():
            """check if the enemy is in the grid"""
            if self.app.state == 'start' or self.app.state == 'resume':
                if self.direction == 'up' or self.direction == 'down':
                    offset = abs(((self.enemy_coords[0] - GRID_START_X) %
                                  CELL_WIDTH) - CELL_WIDTH)
                    if 2 < offset < 16:
                        self.direction = self.prev_direction

                if self.direction == 'left' or self.direction == 'right':
                    offset = abs(
                        ((self.enemy_coords[1] - GRID_START_Y) %
                         CELL_HEIGHT) - CELL_HEIGHT)
                    if 2 < offset < 16:
                        self.direction = self.prev_direction

        def move():
            """move the player"""
            grid_pos = self.app.canvas.coords(self.grid)
            next_cell = self.app.player_coords
            xdirection = int(next_cell[0]) - grid_pos[0]
            ydirection = int(next_cell[1]) - grid_pos[1]
            self.set_direction(xdirection, ydirection)

        self.target = self.app.player_coords
        move()
        inGrid()
        self.can_move()
        now = time()
        delta_time = now - self.prev_time
        self.enemy_weighted_speed = self.enemy_speed * delta_time
        self.prev_time = now

        if self.direction == 'left':
            self.canvas.move(self.enemy, -self.enemy_weighted_speed, 0)

        elif self.direction == 'right':
            self.canvas.move(self.enemy, self.enemy_weighted_speed, 0)

        elif self.direction == 'up':
            self.canvas.move(self.enemy, 0, -self.enemy_weighted_speed)

        elif self.direction == 'down':
            self.canvas.move(self.enemy, 0, self.enemy_weighted_speed)

        move_grid()

        self.prev_direction = self.direction
        self.player_collision()

    def player_collision(self):
        """check for a collision with the player"""
        if self.enemy_coords[0] < self.target[2] and \
                self.enemy_coords[2] > self.target[0] and \
                self.enemy_coords[1] < self.target[3] and \
                self.enemy_coords[3] > self.target[1]:
            if self.app.state == 'start' or self.app.state == 'resume':
                self.app.states_manager('GameOver')

    def set_direction(self, xdir, ydir):
        """set the direction of the enemy"""
        if xdir < -5:
            xdir = 'left'

        else:
            xdir = 'right'

        if ydir < -5:
            ydir = 'up'

        else:
            ydir = 'down'

        if randint(0, 2) == 1:
            self.direction = xdir

        else:
            self.direction = ydir
