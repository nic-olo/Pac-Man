from settings import *
from random import randint
from CanvasManager import move_grid


class Enemy:
    def __init__(self, app, enemy_number):
        self.walls = [[0 for x in range(GRID_COLUMNS)] for y in range(GRID_ROWS)]
        self.app = app
        self.direction = None
        self.prev_direction = None
        self.enemy_number = enemy_number
        self.canvas = self.app.canvas
        self.enemy_coords = []
        self.target = None
        self.enemy_speed = HARD_ENEMY_SPEEDS[self.enemy_number - 1] if self.app.keySettings['difficulty'] == 'hard' \
            else NORMAL_ENEMY_SPEEDS[self.enemy_number - 1]
        self.enemy_color = ENEMY_COLORS[self.enemy_number - 1]
        self.make_enemy()
        self.make_enemy_grid()

    def make_enemy(self):
        file = open(MAZE_COORDINATES_PATH, 'r')

        for i in range(GRID_ROWS):
            line = file.readline()
            for j in range(GRID_COLUMNS):
                if line[j] == str(self.enemy_number):
                    self.enemy_coords = [j, i]
                    break

        file.close()

        self.enemy = self.canvas.create_oval(GRID_START_X + CELL_WIDTH * self.enemy_coords[0] + ENEMY_X1,
                                             GRID_START_Y + CELL_HEIGHT * self.enemy_coords[1] + ENEMY_Y1,
                                             GRID_START_X + CELL_WIDTH * (self.enemy_coords[0]) + ENEMY_X2,
                                             GRID_START_Y + CELL_HEIGHT * (self.enemy_coords[1]) + ENEMY_Y2,
                                             fill=self.enemy_color)

    def make_enemy_grid(self):
        self.grid = self.canvas.create_rectangle(RECTANGLE_X1, RECTANGLE_Y1,
                                                 RECTANGLE_X2, RECTANGLE_Y2, outline=self.enemy_color)
        for cell in self.app.walls:
            if cell[0] < GRID_COLUMNS and cell[1] < GRID_ROWS:
                self.walls[int(cell[1])][int(cell[0])] = 1

    def set_random_direction(self):
        number = randint(0, 3)
        if number == 0:
            self.direction = 'left'
        elif number == 1:
            self.direction = 'right'
        elif number == 2:
            self.direction = 'up'
        else:
            self.direction = 'down'

    def can_move(self):
        enemy_coords = self.canvas.coords(self.enemy)
        for wall in self.app.walls:
            if self.direction == 'left' and \
                    abs(enemy_coords[0] - (GRID_START_X + CELL_WIDTH * (wall[0] + 1))) < 2:
                if abs(enemy_coords[1] - (GRID_START_Y + CELL_HEIGHT * wall[1])) < 4:
                    self.direction = None
                    return 1

            elif self.direction == 'right' and abs(enemy_coords[2] - (GRID_START_X + CELL_WIDTH * wall[0])) < 3:
                if abs(enemy_coords[1] - (GRID_START_Y + CELL_HEIGHT * wall[1])) < 10:
                    self.direction = None
                    return 2

            elif self.direction == 'up' and abs(enemy_coords[1] - (GRID_START_Y + CELL_HEIGHT * (wall[1] + 1))) < 2:
                if abs(enemy_coords[0] - (GRID_START_X + CELL_WIDTH * wall[0])) < 6:
                    self.direction = None
                    return 3

            elif self.direction == 'down' and abs(enemy_coords[3] - (GRID_START_Y + CELL_HEIGHT * wall[1])) < 3:
                if abs(enemy_coords[0] - (GRID_START_X + CELL_WIDTH * wall[0])) < 5:
                    self.direction = None
                    return 4

    def move_enemy(self):
        def inGrid():
            if self.app.state == 'start' or self.app.state == 'resume':

                if self.direction == 'up' or self.direction == 'down':
                    offset = abs(((self.enemy_coords[0] - GRID_START_X) % CELL_WIDTH) - CELL_WIDTH)
                    if 2 < offset < 16:
                        self.direction = self.prev_direction

                if self.direction == 'left' or self.direction == 'right':
                    offset = abs(((self.enemy_coords[1] - GRID_START_Y) % CELL_HEIGHT) - CELL_HEIGHT)
                    if 2 < offset < 16:
                        self.direction = self.prev_direction

        self.target = self.app.player_coords
        self.move()
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

        self.enemy_coords = self.canvas.coords(self.enemy)

        move_grid(self, self.enemy_coords)

        self.prev_direction = self.direction
        self.player_collision()

    def update(self):
        self.move_enemy()
        if self.app.state == 'start' or self.app.state == 'resume':
            self.app.window.after(DELAY, self.update)

    def player_collision(self):
        temp = False
        if self.direction == 'left' and abs(self.enemy_coords[0] - self.target[2]) < ENEMY_RANGE:
            if abs(self.enemy_coords[0] - self.target[0]) < 5:
                temp = True

        elif self.direction == 'right' and abs(self.enemy_coords[2] - self.target[0]) < ENEMY_RANGE:
            if abs(self.enemy_coords[1] - (self.target[1])) < 5:
                temp = True

        elif self.direction == 'up' and abs(self.enemy_coords[1] - (self.target[3])) < ENEMY_RANGE:
            if abs(self.enemy_coords[0] - (self.target[0])) < 5:
                temp = True

        elif self.direction == 'down' and abs(self.enemy_coords[3] - (self.target[1])) < ENEMY_RANGE:
            if abs(self.enemy_coords[0] - (self.target[0])) < 5:
                temp = True

        if temp:
            if self.app.state == 'start' or self.app.state == 'resume':
                self.app.states_manager('GameOver')

    def move(self):
        if self.enemy_number == 0:
            self.set_random_direction()
        else:
            self.set_path_direction(self.target)

    def set_path_direction(self, target):
        grid_pos = self.app.canvas.coords(self.grid)
        next_cell = self.app.player_coords
        xdirection = int(next_cell[0]) - grid_pos[0]
        ydirection = int(next_cell[1]) - grid_pos[1]
        self.set_direction(xdirection, ydirection)

    def set_direction(self, xdir, ydir):
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
