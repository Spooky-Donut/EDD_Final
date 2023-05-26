import pygame, sys
import math
import random
import time
from button import Button


sys.setrecursionlimit(10000)

pygame.display.set_caption("MineVenture")
pygame.display.set_icon(pygame.image.load("MinaSinFondoCuadrada.png"))

totalBees = 30
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
    pygame.draw.rect(SCREEN, P_BLUE, (560, 390, 780, 480))
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

        self.flagged = False
        self.bee = False
        self.revealed = False

    def flag(self):
        if not self.revealed:
            banderita = pygame.image.load("bandera cuadrada.png")
            banderita = pygame.transform.scale(banderita, (self.w * 1.01, self.w * 1.01))
            SCREEN.blit(banderita, (self.x + 563 - self.w * 0.05,self.y + 395 - self.w * 0.05))
            self.flagged = not self.flagged

    def show(self):
        pygame.draw.rect(SCREEN, F_RED, (self.x + 563, self.y + 395, self.w, self.w), 1)
        if self.revealed:
            if self.bee:
                mina_1 = pygame.image.load("MinaCuadrada.png")
                mina_1 = pygame.transform.scale(mina_1, (self.w * 1.01, self.w * 1.01))
                SCREEN.blit(mina_1, (self.x + 563 - self.w * 0.05, self.y + 395 - self.w * 0.05))
            else:
                pygame.draw.rect(SCREEN, Y_GREEN, (self.x + 563, self.y + 395, self.w, self.w), 1)
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
                    text_rect = text.get_rect(center=(self.x + 563 + self.w * 0.5, self.y + 395 + self.w * 0.5))
                    SCREEN.blit(text, text_rect)
        elif self.flagged:
            banderita = pygame.image.load("bandera cuadrada.png")
            banderita = pygame.transform.scale(banderita, (self.w * 1.01, self.w * 1.01))
            SCREEN.blit(banderita, (self.x + 563 - self.w * 0.05,self.y + 395 - self.w * 0.05))

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
        return self.x + 563 < x < self.x + 563 + self.w and self.y + 395 < y < self.y + 395 + self.w

    def reveal(self):
        if self.flagged:
            return None
        else:
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
    arr = [[None for _ in range(rows)] for _ in range(cols)]
    return arr

def setup(cell_size):
    global cols, rows, grid
    cols = math.floor(780 / cell_size)
    rows = math.floor(480 / cell_size)
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
    mouse_pos = pygame.mouse.get_pos()
    mouse_button = pygame.mouse.get_pressed()

    for i in range(cols):
        for j in range(rows):
            if grid[i][j].contains(mouse_pos[0], mouse_pos[1]):
                if mouse_button[0]:
                    if not grid[i][j].flagged:
                        grid[i][j].reveal()
                        if grid[i][j].bee:
                            gameOver()
                elif mouse_button[2]:
                    grid[i][j].flag()

setup(cell_size)


# ---------------------------------------------------------------------------------------------------


start_time = 0
elapsed_time = 0
paused = False
sw = 0
x = 550
y = 380
width_rect=800
height_rect=500
border_width = 10

pygame.init()

Whithe=(255,255,255)
Black=(0,0,0)
SCREEN = pygame.display.set_mode((1920, 1080))

BG = pygame.image.load("FondoPausa.png")

def get_font(size): 
    return pygame.font.Font("pixel.ttf", size)
bandera=pygame.image.load("bandera cuadrada.png")
nuevo_ancho = 40
nuevo_alto = 40
imagen_redimensionada = pygame.transform.scale(bandera, (nuevo_ancho, nuevo_alto))
BG = pygame.image.load("FondoPausa.png")

def pausa(sw, paused, start_time, elapsed_time):
    paused_elapsed_time = elapsed_time
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        PAUSE_TEXT = get_font(120).render("PAUSA", True, "#000000")
        PAUSE_RECT = PAUSE_TEXT.get_rect(center=(960 , 300))

        RESUME_BUTTON = Button(image=pygame.image.load("ResumeButton.png"), pos=(750, 500), 
                            text_input="REANUDAR", font=get_font(55), base_color="#d7fcd4", hovering_color="White")
        REINICIAR_BUTTON = Button(image=pygame.image.load("ResumeButton.png"), pos=(1140, 500), 
                            text_input="REINICIAR", font=get_font(55), base_color="#d7fcd4", hovering_color="White")
        MENU_BUTTON = Button(image=pygame.image.load("ResumeButton.png"), pos=(750, 650), 
                            text_input="MENÚ", font=get_font(55), base_color="#d7fcd4", hovering_color="White")
        COMOJUGAR_BUTTON = Button(image=pygame.image.load("ResumeButton.png"), pos=(1140, 650), 
                            text_input="COMO JUGAR", font=get_font(54), base_color="#d7fcd4", hovering_color="White")
        SCREEN.blit(PAUSE_TEXT, PAUSE_RECT)

        for button in [RESUME_BUTTON, REINICIAR_BUTTON, MENU_BUTTON, COMOJUGAR_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if RESUME_BUTTON.checkForInput(MENU_MOUSE_POS):
                    paused = not paused
                    if not paused:
                        start_time = time.time() - paused_elapsed_time
                    game(sw, paused, start_time, elapsed_time)

        pygame.display.flip()

def game(sw, paused, start_time, elapsed_time):
    while True:
        SCREEN.fill(Whithe)

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        pygame.draw.rect(SCREEN, "Black", (x, y,  width_rect, height_rect), border_width)
        PAUSE_BUTTON = Button(image=pygame.image.load("PauseButton.png"), pos=(1515, 250), 
                            text_input="", font=get_font(55), base_color="#000000", hovering_color="White")
        Bandera = Button(image=imagen_redimensionada, pos=(650, 320), 
                            text_input="", font=get_font(15), base_color="#d7fcd4", hovering_color="White")
        Time = Button(image=None, pos=(870, 320), 
                            text_input=f"{elapsed_time}", font=get_font(35), base_color="#000000", hovering_color="White")
        Puntos = Button(image=None, pos=(1150, 320), 
                            text_input="PUNTOS", font=get_font(35), base_color="#000000", hovering_color="White")

        for button in [PAUSE_BUTTON, Bandera, Time, Puntos]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if sw == 0:
                    start_time = time.time()
                    sw = 1
                mousePressed()
                if PAUSE_BUTTON.checkForInput(MENU_MOUSE_POS):
                    paused = not paused
                    pausa(sw, paused, start_time, elapsed_time)


        
        if not paused:
            if sw == 1:            
                elapsed_time = math.floor(time.time() - start_time)

        draw()

        pygame.display.flip()

game(sw, paused, start_time, elapsed_time)
