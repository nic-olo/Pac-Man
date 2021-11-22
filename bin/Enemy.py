from settings import *
from random import randint
from CanvasManager import move_grid


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
            else NORMAL_ENEMY_SPEEDS[self.enemy_number - 1]
        self.enemy_color = ENEMY_COLORS[self.enemy_number - 1]
        self.make_enemy()
        self.make_enemy_grid()

    def make_enemy(self):
        """create the enemy"""
        if self.app.state == 'continue':
            self.enemy = self.canvas.create_oval(
                self.app.enemies_coords[self.enemy_number - 1],
                fill=self.enemy_color)
            return
        file = open(MAZE_COORDINATES_PATH, 'r')

        for i in range(GRID_ROWS):
            line = file.readline()
            for j in range(GRID_COLUMNS):
                if line[j] == str(self.enemy_number):
                    self.enemy_pos = [j, i]
                    break

        file.close()

        self.enemy = self.canvas.create_oval(
            GRID_START_X + CELL_WIDTH * self.enemy_pos[0] + ENEMY_X1,
            GRID_START_Y + CELL_HEIGHT * self.enemy_pos[1] + ENEMY_Y1,
            GRID_START_X + CELL_WIDTH * (self.enemy_pos[0]) + ENEMY_X2,
            GRID_START_Y + CELL_HEIGHT * (self.enemy_pos[1]) + ENEMY_Y2,
            fill=self.enemy_color)

    def make_enemy_grid(self):
        """create the grid that surrounds the enemy"""
        self.grid = self.canvas.create_rectangle(RECTANGLE_X1, RECTANGLE_Y1,
                                                 RECTANGLE_X2, RECTANGLE_Y2,
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
                    GRID_START_X + CELL_WIDTH * (wall[0] + 1))) < 3:
                if abs(self.enemy_coords[1] - (
                        GRID_START_Y + CELL_HEIGHT * wall[1])) < 12:
                    self.direction = None
                    return 1

            elif self.direction == 'right' and abs(self.enemy_coords[2] - (
                    GRID_START_X + CELL_WIDTH * wall[0])) < 3:
                if abs(self.enemy_coords[1] - (
                        GRID_START_Y + CELL_HEIGHT * wall[1])) < 12:
                    self.direction = None
                    return 2

            elif self.direction == 'up' and abs(
                    self.enemy_coords[1] - (
                            GRID_START_Y + CELL_HEIGHT * (wall[1] + 1))) < 3:
                if abs(self.enemy_coords[0] - (
                        GRID_START_X + CELL_WIDTH * wall[0])) < 12:
                    self.direction = None
                    return 3

            elif self.direction == 'down' and abs(self.enemy_coords[3] - (
                    GRID_START_Y + CELL_HEIGHT * wall[1])) < 3:
                if abs(self.enemy_coords[0] - (
                        GRID_START_X + CELL_WIDTH * wall[0])) < 12:
                    self.direction = None
                    return 4

    def move_enemy(self):
        """check the position of the enemy and move it"""
        self.enemy_coords = self.canvas.coords(self.enemy)

        def inGrid():
            """check if the enemy is in the grid"""
            if self.app.state == 'start' or self.app.state == 'resume':
                if self.direction == 'up' or self.direction == 'down':
                    offset = abs(((self.enemy_coords[0] -
                                   GRID_START_X) % CELL_WIDTH) - CELL_WIDTH)
                    if 2 < offset < 16:
                        self.direction = self.prev_direction

                if self.direction == 'left' or self.direction == 'right':
                    offset = abs(((self.enemy_coords[1] -
                                   GRID_START_Y) % CELL_HEIGHT) - CELL_HEIGHT)
                    if 2 < offset < 16:
                        self.direction = self.prev_direction

        def move():
            """actually move the player"""
            grid_pos = self.app.canvas.coords(self.grid)
            next_cell = self.app.player_coords
            xdirection = int(next_cell[0]) - grid_pos[0]
            ydirection = int(next_cell[1]) - grid_pos[1]
            self.set_direction(xdirection, ydirection)

        self.target = self.app.player_coords
        move()
        inGrid()
        _ = self.can_move()

        if self.direction == 'left':
            self.canvas.move(self.enemy, -self.enemy_speed, 0)

        elif self.direction == 'right':
            self.canvas.move(self.enemy, self.enemy_speed, 0)

        elif self.direction == 'up':
            self.canvas.move(self.enemy, 0, -self.enemy_speed)

        elif self.direction == 'down':
            self.canvas.move(self.enemy, 0, self.enemy_speed)

        move_grid(self, self.enemy_coords)

        self.prev_direction = self.direction
        self.player_collision()

    def player_collision(self):
        """check for a collision with the player"""
        if self.enemy_coords[0] < self.target[2] and self.enemy_coords[2] > \
                self.target[0] and \
                self.enemy_coords[1] < self.target[3] and \
                self.enemy_coords[3] > self.target[1]:
            if self.app.state == 'start' or self.app.state == 'resume':
                self.app.states_manager('GameOver')

    def set_direction(self, xdir, ydir):
        """set the direction of the enemy"""
        if xdir < -5 and self.can_move() != 1:
            xdir = 'left'
        elif self.can_move() != 2:
            xdir = 'right'
        if ydir < -5 and self.can_move() != 3:
            ydir = 'up'
        elif self.can_move() != 4:
            ydir = 'down'

        if randint(0, 2) == 1:
            self.direction = xdir
        else:
            self.direction = ydir
