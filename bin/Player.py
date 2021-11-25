from settings import *
from MazeRender import coin_collision
from time import time


class Player:
    def __init__(self, app):
        """initialize the player"""
        self.app = app
        self.player_color = self.app.settings['color']
        self.player_speed = PLAYER_SPEED
        self.make_player()
        self.prev_time = time()

    def make_player(self):
        """create the player"""
        if self.app.state == 'start' or self.app.state == 'resume':
            with open(MAZE_COORDINATES_PATH, 'r') as file:
                for i in range(GRID_ROWS):
                    # read a file txt to get the coordinates of the player
                    line = file.readline()
                    for j in range(GRID_COLUMNS):
                        if line[j] == '5':
                            player_pos = [j, i]
                            break

            self.player = self.app.canvas.create_oval(
                GRID_START_X + CELL_WIDTH * player_pos[0] + PLAYER_X1,
                GRID_START_Y + CELL_HEIGHT * player_pos[1] + PLAYER_Y1,
                GRID_START_X + CELL_WIDTH * (player_pos[0]) + PLAYER_X2,
                GRID_START_Y + CELL_HEIGHT * (player_pos[1]) + PLAYER_Y2,
                fill=self.player_color
            )

        else:
            self.player = self.app.canvas.create_oval(
                self.app.player_coords,
                fill=self.player_color
            )

            self.app.state = 'start'

    def can_move(self):
        """block the player from passing through a wall"""
        player_coords = self.app.canvas.coords(self.player)
        for wall in self.app.walls:
            wall_coords = self.app.canvas.coords(wall[2])
            if self.app.player_direction == 'left' and \
                    abs(
                        player_coords[0] - (GRID_START_X + CELL_WIDTH *
                                            (wall[0] + 1))) < 5 and \
                    wall_coords[1] < player_coords[3] and \
                    wall_coords[3] > player_coords[1]:

                self.app.player_direction = None

            elif self.app.player_direction == 'right' and abs(
                    player_coords[2] - (
                            GRID_START_X + CELL_WIDTH * wall[0])) < 5 and \
                    wall_coords[1] < player_coords[3] and wall_coords[3] > \
                    player_coords[1]:

                self.app.player_direction = None

            elif self.app.player_direction == 'up' and abs(
                    player_coords[1] - (GRID_START_Y + CELL_HEIGHT * (
                            wall[1] + 1))) < 5 and \
                    wall_coords[0] < player_coords[2] and wall_coords[2] > \
                    player_coords[0]:

                self.app.player_direction = None

            elif self.app.player_direction == 'down' and abs(
                    player_coords[3] - (
                            GRID_START_Y + CELL_HEIGHT * wall[1])) < 5 and \
                    wall_coords[0] < player_coords[2] and wall_coords[2] > \
                    player_coords[0]:

                self.app.player_direction = None

    def move_player(self):
        """check the position of the player and move it"""

        def move_grid():
            """move the grid that surrounds the user"""
            if self.app.state == 'start' or self.app.state == 'resume':
                self.app.canvas.coords(
                    self.app.grid,
                    ((positions[0] + CELL_WIDTH // 2) //
                     CELL_WIDTH) * CELL_WIDTH + 4,
                    ((positions[1] + CELL_HEIGHT // 2) //
                     CELL_HEIGHT) * CELL_HEIGHT + 6,
                    ((positions[2] + CELL_WIDTH // 2) //
                     CELL_WIDTH) * CELL_WIDTH + 4,
                    ((positions[3] + CELL_HEIGHT // 2) //
                     CELL_HEIGHT) * CELL_HEIGHT + 6
                )

                self.app.player_coords = self.app.canvas.coords(self.app.grid)

        def in_grid():
            """check if the player is in the grid before moving the player"""
            if self.app.state == 'start' or self.app.state == 'resume':

                if self.app.player_direction == 'up' or \
                        self.app.player_direction == 'down':

                    offset = abs(
                        ((positions[0] - GRID_START_X) %
                         CELL_WIDTH) - CELL_WIDTH
                    )

                    if 3 < offset < 15:
                        self.app.player_direction = self.app.prev_direction

                if self.app.player_direction == 'left' or \
                        self.app.player_direction == 'right':

                    offset = abs(
                        ((positions[1] - GRID_START_Y) % CELL_HEIGHT) -
                        CELL_HEIGHT
                    )

                    if 3 < offset < 15:
                        self.app.player_direction = self.app.prev_direction

        self.app.canvas.pack()
        positions = self.app.canvas.coords(self.player)
        in_grid()
        coin_collision(self.app)
        self.can_move()
        now = time()
        delta_time = now - self.prev_time
        self.player_weighted_speed = self.player_speed * delta_time
        self.prev_time = now

        if self.app.player_direction == 'left':
            self.app.canvas.move(self.player, -self.player_weighted_speed, 0)

        elif self.app.player_direction == 'right':
            self.app.canvas.move(self.player, self.player_weighted_speed, 0)

        elif self.app.player_direction == 'up':
            self.app.canvas.move(self.player, 0, -self.player_weighted_speed)

        elif self.app.player_direction == 'down':
            self.app.canvas.move(self.player, 0, self.player_weighted_speed)

        self.app.prev_direction = self.app.player_direction
        move_grid()

    def update(self):
        """update the movement of the player"""
        self.move_player()
        if self.app.state == 'start' or self.app.state == 'resume':
            self.app.window.after(DELAY, self.update)
