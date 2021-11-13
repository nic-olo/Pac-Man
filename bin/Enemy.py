from settings import *
from random import randint


class Enemy:
    def __init__(self, app, enemy_number):
        self.app = app
        self.direction = None
        self.prev_direction = None
        self.enemy_number = enemy_number
        self.enemy_coords = []
        self.target = None
        self.enemy_speed = ENEMY_SPEEDS[self.enemy_number - 1]

    def make_enemy(self):
        file = open(MAZE_COORDINATES_PATH, 'r')

        for i in range(GRID_ROWS):
            line = file.readline()
            for j in range(GRID_COLUMNS):
                if line[j] == str(self.enemy_number):
                    self.enemy_coords = [j, i]
                    break

        file.close()

        self.enemy = self.app.canvas.create_oval(GRID_START_X + CELL_WIDTH * self.enemy_coords[0] + ENEMY_X1,
                                                 GRID_START_Y + CELL_HEIGHT * self.enemy_coords[1] + ENEMY_Y1,
                                                 GRID_START_X + CELL_WIDTH * (self.enemy_coords[0]) + ENEMY_X2,
                                                 GRID_START_Y + CELL_HEIGHT * (self.enemy_coords[1]) + ENEMY_Y2,
                                                 fill=ENEMY_COLORS[self.enemy_number - 1])

    def get_random_direction(self):
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
        enemy_coords = self.app.canvas.coords(self.enemy)
        for wall in self.app.walls:
            if self.direction == 'left' and \
                    abs(enemy_coords[0] - (GRID_START_X + CELL_WIDTH * (wall[0] + 1))) < 2:
                if abs(enemy_coords[1] - (GRID_START_Y + CELL_HEIGHT * wall[1])) < 4:
                    self.direction = None

            elif self.direction == 'right' and abs(enemy_coords[2] - (GRID_START_X + CELL_WIDTH * wall[0])) < 3:
                if abs(enemy_coords[1] - (GRID_START_Y + CELL_HEIGHT * wall[1])) < 10:
                    self.direction = None

            elif self.direction == 'up' and abs(enemy_coords[1] - (GRID_START_Y + CELL_HEIGHT * (wall[1] + 1))) < 2:
                if abs(enemy_coords[0] - (GRID_START_X + CELL_WIDTH * wall[0])) < 6:
                    self.direction = None

            elif self.direction == 'down' and abs(enemy_coords[3] - (GRID_START_Y + CELL_HEIGHT * wall[1])) < 3:
                if abs(enemy_coords[0] - (GRID_START_X + CELL_WIDTH * wall[0])) < 5:
                    self.direction = None

    def move_enemy(self):
        def inGrid():
            if self.app.state == 'start' or self.app.state == 'resume':

                if self.direction == 'up' or self.direction == 'down':
                    offset = abs(((positions[0] - GRID_START_X) % CELL_WIDTH) - CELL_WIDTH)
                    if 2 < offset < 16:
                        self.direction = self.prev_direction

                if self.direction == 'left' or self.direction == 'right':
                    offset = abs(((positions[1] - GRID_START_Y) % CELL_HEIGHT) - CELL_HEIGHT)
                    if 2 < offset < 16:
                        self.direction = self.prev_direction

        self.get_random_direction()
        positions = self.app.canvas.coords(self.enemy)
        inGrid()
        self.can_move()
        if self.direction == 'left':
            self.app.canvas.move(self.enemy, -self.enemy_speed, 0)

        elif self.direction == 'left':
            self.app.canvas.move(self.enemy, self.enemy_speed, 0)

        elif self.direction == 'up':
            self.app.canvas.move(self.enemy, 0, -self.enemy_speed)

        elif self.direction == 'up':
            self.app.canvas.move(self.enemy, 0, self.enemy_speed)

        if self.app.state == 'start' or self.app.state == 'resume':
            self.app.window.after(DELAY, self.move_enemy)

        self.prev_direction = self.direction


'''
def update(self):
    self.target = self.set_target()
    if self.target != self.grid_pos:
        self.pix_pos += self.direction * self.enemy_speed
        if self.time_to_move():
            self.move()

    # Setting grid position in reference to pix position
    self.grid_pos[0] = (self.pix_pos[0] - TOP_BOTTOM_BUFFER +
                        self.app.cell_width // 2) // self.app.cell_width + 1
    self.grid_pos[1] = (self.pix_pos[1] - TOP_BOTTOM_BUFFER +
                        self.app.cell_height // 2) // self.app.cell_height + 1

    def draw(self):
        pygame.draw.circle(self.app.screen, self.colour,
                           (int(self.pix_pos.x), int(self.pix_pos.y)), self.radius)

    def set_speed(self):
        if self.personality in ["speedy", "scared"]:
            speed = 2
        else:
            speed = 1
        return speed

    def set_target(self):
        if self.personality == "speedy" or self.personality == "slow":
            return self.app.player.grid_pos
        else:
            if self.app.player.grid_pos[0] > COLS // 2 and self.app.player.grid_pos[1] > ROWS // 2:
                return vec(1, 1)
            if self.app.player.grid_pos[0] > COLS // 2 and self.app.player.grid_pos[1] < ROWS // 2:
                return vec(1, ROWS - 2)
            if self.app.player.grid_pos[0] < COLS // 2 and self.app.player.grid_pos[1] > ROWS // 2:
                return vec(COLS - 2, 1)
            else:
                return vec(COLS - 2, ROWS - 2)

    def time_to_move(self):
        if int(self.pix_pos.x + TOP_BOTTOM_BUFFER // 2) % self.app.cell_width == 0:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0) or self.direction == vec(0, 0):
                return True
        if int(self.pix_pos.y + TOP_BOTTOM_BUFFER // 2) % self.app.cell_height == 0:
            if self.direction == vec(0, 1) or self.direction == vec(0, -1) or self.direction == vec(0, 0):
                return True
        return False

    def move(self):
        if self.personality == "random":
            self.direction = self.get_random_direction()
        if self.personality == "slow":
            self.direction = self.get_path_direction(self.target)
        if self.personality == "speedy":
            self.direction = self.get_path_direction(self.target)
        if self.personality == "scared":
            self.direction = self.get_path_direction(self.target)

    def get_path_direction(self, target):
        next_cell = self.find_next_cell_in_path(target)
        xdir = next_cell[0] - self.grid_pos[0]
        ydir = next_cell[1] - self.grid_pos[1]
        return vec(xdir, ydir)

    def find_next_cell_in_path(self, target):
        path = self.BFS([int(self.grid_pos.x), int(self.grid_pos.y)], [
            int(target[0]), int(target[1])])
        return path[1]

    def BFS(self, start, target):
        grid = [[0 for x in range(28)] for x in range(30)]
        for cell in self.app.walls:
            if cell.x < 28 and cell.y < 30:
                grid[int(cell.y)][int(cell.x)] = 1
        queue = [start]
        path = []
        visited = []
        while queue:
            current = queue[0]
            queue.remove(queue[0])
            visited.append(current)
            if current == target:
                break
            else:
                neighbours = [[0, -1], [1, 0], [0, 1], [-1, 0]]
                for neighbour in neighbours:
                    if neighbour[0] + current[0] >= 0 and neighbour[0] + current[0] < len(grid[0]):
                        if neighbour[1] + current[1] >= 0 and neighbour[1] + current[1] < len(grid):
                            next_cell = [neighbour[0] + current[0], neighbour[1] + current[1]]
                            if next_cell not in visited:
                                if grid[next_cell[1]][next_cell[0]] != 1:
                                    queue.append(next_cell)
                                    path.append({"Current": current, "Next": next_cell})
        shortest = [target]
        while target != start:
            for step in path:
                if step["Next"] == target:
                    target = step["Current"]
                    shortest.insert(0, step["Current"])
        return shortest
'''
