import pygame
import random
import math
pygame.init()



pygame.display.set_caption("MineVenture")
pygame.display.set_icon(pygame.image.load("MinaSinFondoCuadrada.png"))

totalBees = 30
screen_size = (400, 400)
screen = pygame.display.set_mode(screen_size)
cell_size = 18

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
F_RED = (211,73,78)
Y_GREEN = (214,232,101)
P_BLUE = (48, 16, 107)
BLUE = (0, 255, 255)
GREEN = (0,255,0)
YELLOW = (255, 234, 0)
ORANGE = (242, 140, 40)
RED = (255, 15, 0)

cols = None
rows = None
grid = None

def draw():
    screen.fill(P_BLUE)
    for i in range(cols):
        for j in range(rows):
            grid[i][j].show()

class Cell:

    def __init__(self, i, j, w):
        self.i = i
        self.j = j
        self.x = i * w
        self.y = j * w
        self.w = w
        self.neighborCount = 0

        self.bee = False
        self.revealed = False

    def show(self):
        pygame.draw.rect(screen, F_RED, (self.x, self.y, self.w, self.w), 1)
        if self.revealed:
            if self.bee:
                mina_1 = pygame.image.load("MinaCuadrada.png")
                mina_1 = pygame.transform.scale(mina_1, (self.w * 1.01, self.w * 1.01))
                screen.blit(mina_1, (self.x - self.w * 0.05,self.y - self.w * 0.05))
            else:
                pygame.draw.rect(screen, Y_GREEN, (self.x, self.y, self.w, self.w), 1)
                if self.neighborCount > 0:
                    font = pygame.font.SysFont(None, 20)
                    if self.neighborCount == 1:
                        text = font.render(str(self.neighborCount), True, BLUE)
                    elif self.neighborCount == 2:
                        text = font.render(str(self.neighborCount), True, GREEN)
                    elif self.neighborCount == 3:
                        text = font.render(str(self.neighborCount), True, YELLOW)
                    elif self.neighborCount == 4:
                        text = font.render(str(self.neighborCount), True, ORANGE)
                    elif self.neighborCount == 5:
                        text = font.render(str(self.neighborCount), True, RED)
                    else:
                        text = font.render(str(self.neighborCount), True, WHITE)
                    text_rect = text.get_rect(center=(self.x + self.w * 0.5, self.y + self.w * 0.5))
                    screen.blit(text, text_rect)

    def countBees(self):
        if self.bee:
            self.neighborCount = -1
            return
        total = 0
        for xoff in range(-1, 2):
            i = self.i + xoff
            if i < 0 or i >= cols:
                continue
            for yoff in range(-1, 2):
                j = self.j + yoff
                if j < 0 or j >= rows:
                    continue
                neighbor = grid[i][j]
                if neighbor.bee:
                    total += 1
        self.neighborCount = total

    def contains(self, x, y):
        return self.x < x < self.x + self.w and self.y < y < self.y + self.w

    def reveal(self):
        self.revealed = True
        if self.neighborCount == 0:
            self.floodFill()

    def floodFill(self):
        for xoff in range(-1, 2):
            i = self.i + xoff
            if i < 0 or i >= cols:
                continue
            for yoff in range(-1, 2):
                j = self.j + yoff
                if j < 0 or j >= rows:
                    continue
                neighbor = grid[i][j]
                if not neighbor.revealed:
                    neighbor.reveal()

def make2DArray(cols, rows):
    arr = [[None for _ in range(cols)] for _ in range(rows)]
    return arr

def setup(cell_size):
    global cols, rows, grid
    cols = math.floor(screen_size[0] / cell_size)
    rows = math.floor(screen_size[1] / cell_size)
    grid = make2DArray(cols, rows)
    for i in range(cols):
        for j in range(rows):
            grid[i][j] = Cell(i, j, cell_size)

    # Pick totalBees spots
    options = []
    for i in range(cols):
        for j in range(rows):
            options.append([i, j])

    for n in range(totalBees):
        index = math.floor(random.random() * len(options))
        choice = options[index]
        i = choice[0]
        j = choice[1]
        # Deletes that spot so it's no longer an option
        del options[index]
        grid[i][j].bee = True


    for i in range(cols):
        for j in range(rows):
            grid[i][j].countBees()

def gameOver():
    for i in range(cols):
        for j in range(rows):
            grid[i][j].revealed = True

def mousePressed():
    for i in range(cols):
        for j in range(rows):
            if grid[i][j].contains(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                grid[i][j].reveal()

                if grid[i][j].bee:
                    gameOver()

setup(20)

finished = False

while not finished:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            mousePressed()

    draw()

    pygame.display.flip()

pygame.quit()
