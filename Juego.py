import pygame as pg
import sys
import math
import random
import time
from button import Button


sys.setrecursionlimit(10000)
pg.display.set_caption("MineVenture")
pg.display.set_icon(pg.image.load("MinaSinFondoCuadrada.png"))


cell_size = 18

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
WHITE2 = (245, 245, 245)
GREY = (215, 215, 215)
F_RED = (211, 73, 78)
L_GREEN = (144, 238, 144)
PURPLE1 = (195, 177, 225)
BLUE1 = (0, 150, 255)
GREEN1 = (50, 195, 50)
YELLOW1 = (255, 192, 0)
ORANGE = (242, 140, 40)
RED = (255, 15, 0)
P_YELLOW = (255, 255, 180)

cols = None
rows = None
grid = None


def draw():
    pg.draw.rect(screen1, P_YELLOW, (560, 390, 780, 480))
    pg.draw.rect(screen1, GREY, (560 + 4, 390 + 6, 780 - 8, 480 - 13))
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
            banderita = pg.image.load("bandera cuadrada.png")
            banderita = pg.transform.scale(
                banderita, (self.w * 1.01, self.w * 1.01))
            screen1.blit(banderita, (self.x + 563 - self.w *
                         0.05, self.y + 395 - self.w * 0.05))
            self.flagged = not self.flagged

    def show(self):
        if not self.revealed:
            pg.draw.rect(screen1, F_RED, (self.x + 563 + 1,
                         self.y + 395 + 1, self.w - 2, self.w - 2), 0)
        else:
            pg.draw.rect(screen1, F_RED, (self.x + 563 + 1,
                         self.y + 395 + 1, self.w - 2, self.w - 2), 1)
        if self.revealed:
            if self.bee:
                mina_1 = pg.image.load("MinaCuadrada.png")
                mina_1 = pg.transform.scale(
                    mina_1, (self.w * 1.01, self.w * 1.01))
                screen1.blit(mina_1, (self.x + 563 - self.w *
                             0.05, self.y + 395 - self.w * 0.05))
            else:
                pg.draw.rect(screen1, WHITE2, (self.x + 563 + 2,
                             self.y + 395 + 2, self.w - 4, self.w - 4), 0)
                pg.draw.rect(screen1, L_GREEN, (self.x + 563 + 1,
                             self.y + 395 + 1, self.w - 2, self.w - 2), 1)
                if self.neighborCount > 0:
                    font = pg.font.SysFont(None, 20)
                    if self.neighborCount == 1:
                        text = font.render(
                            str(self.neighborCount), True, BLUE1)
                    elif self.neighborCount == 2:
                        text = font.render(
                            str(self.neighborCount), True, GREEN1)
                    elif self.neighborCount == 3:
                        text = font.render(
                            str(self.neighborCount), True, YELLOW1)
                    elif self.neighborCount == 4:
                        text = font.render(
                            str(self.neighborCount), True, ORANGE)
                    elif self.neighborCount == 5:
                        text = font.render(str(self.neighborCount), True, RED)
                    else:
                        text = font.render(
                            str(self.neighborCount), True, WHITE)
                    text_rect = text.get_rect(
                        center=(self.x + 563 + self.w * 0.5, self.y + 395 + self.w * 0.5))
                    screen1.blit(text, text_rect)
        elif self.flagged:
            banderita = pg.image.load("bandera cuadrada.png")
            banderita = pg.transform.scale(
                banderita, (self.w * 1.01, self.w * 1.01))
            screen1.blit(banderita, (self.x + 563 - self.w *
                         0.05, self.y + 395 - self.w * 0.05))

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

    def reveal(self, tiempo_completado, cell_size, totalBees):
        if self.flagged:
            return None
        else:
            self.revealed = True
            if checkWin():
                resumen(tiempo_completado, 2, cell_size, totalBees)
            if self.neighborCount == 0:
                self.floodFill(tiempo_completado, cell_size, totalBees)

    def floodFill(self, tiempo_completado, cell_size, totalBees):
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
                    neighbor.reveal(tiempo_completado, cell_size, totalBees)


def make2DArray(cols, rows):
    arr = [[None for _ in range(rows)] for _ in range(cols)]
    return arr


def setup(cell_size, totalBees):
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


def checkWin():
    cols = math.floor(780 / cell_size)
    rows = math.floor(480 / cell_size)
    for i in range(cols):
        for j in range(rows):
            if not grid[i][j].revealed and not grid[i][j].bee:
                return False
    return True


def gameOver(elapsed_time, cell_size, totalBees):
    for i in range(cols):
        for j in range(rows):
            grid[i][j].revealed = True
    resumen(elapsed_time, 1, cell_size, totalBees)


def mousePressed(elapsed_time, cell_size, totalBees):
    mouse_pos = pg.mouse.get_pos()
    mouse_button = pg.mouse.get_pressed()

    for i in range(cols):
        for j in range(rows):
            if grid[i][j].contains(mouse_pos[0], mouse_pos[1]):
                if mouse_button[0]:
                    if not grid[i][j].flagged:
                        grid[i][j].reveal(elapsed_time, cell_size, totalBees)
                        if grid[i][j].bee:
                            gameOver(elapsed_time, cell_size, totalBees)
                elif mouse_button[2]:
                    grid[i][j].flag()


# ---------------------------------------------------------------------------------------------------
start_time = 0
elapsed_time = 0
paused = False
sw = 0
x = 550
y = 380
width_rect = 800
height_rect = 500
border_width = 10

pg.init()
width = 1920
height = 1080
screen = pg.display.set_mode((width, height), pg.HWSURFACE)
screen1 = pg.display.set_mode((width, height), pg.HWSURFACE)
fondo = pg.image.load("FondoPrincipal.jpg").convert()
screen = pg.display.get_surface()
fondo = pg.transform.scale(fondo, (width, height))
play_button = pg.image.load("PlayButton.png")
nuevo_ancho = 40
nuevo_alto = 40
bandera = pg.image.load("bandera cuadrada.png")
imagen_redimensionada = pg.transform.scale(bandera, (nuevo_ancho, nuevo_alto))
x = 550
y = 380
width_rect = 800
height_rect = 500
border_width = 10

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (240, 50, 50)
BLUE = (50, 188, 204)
GREEN = (62, 199, 147, 100)
YELLOW = (250, 202, 62)
PURPLE = (100, 52, 211)

# Fuentes
font_title = pg.font.Font("pixel.ttf", 80)
font_play = pg.font.Font("pixel.ttf", 64)
font_button = pg.font.Font("pixel.ttf", 30)

# Texto del juego
game_title = font_title.render("MineVenture", True, BLACK)
game_title_rect = game_title.get_rect()
game_title_rect.centerx = width//2
game_title_rect.centery = 250

# Botón Cerrar
button_close = pg.Surface((170, 45), flags=0)
button_close.fill(RED)
button_close_rect = button_close.get_rect()
button_close_rect.midright = (1590, 230)

text_close = font_button.render("Cerrar", True, BLACK)
text_close_rect = text_close.get_rect()
text_close_rect.centerx = button_close_rect.centerx
text_close_rect.centery = button_close_rect.centery


# Botón Jugar
play_button = pg.image.load("PlayButton.png").convert_alpha()
play_button_rect = play_button.get_rect()
play_button_rect.center = screen.get_rect().center


# Botón Estadísticas
button_statistics = pg.Surface((235, 55))
button_statistics.fill(PURPLE)
button_statistics_rect = button_statistics.get_rect()
button_statistics_rect.midright = (width / 1.23, play_button_rect.centery)

text_statistics = font_button.render("Estadísticas", True, BLACK)
text_statistics_rect = text_statistics.get_rect()
text_statistics_rect.centerx = button_statistics_rect.centerx
text_statistics_rect.centery = button_statistics_rect.centery

# Botón Instrucciones
button_instructions = pg.Surface((250, 55))
button_instructions.fill(BLUE)
button_instructions_rect = button_instructions.get_rect()
button_instructions_rect.centerx = width // 2
button_instructions_rect.centery = height / 1.3

text_instructions = font_button.render("Instrucciones", True, BLACK)
text_instructions_rect = text_instructions.get_rect()
text_instructions_rect.centerx = button_instructions_rect.centerx
text_instructions_rect.centery = button_instructions_rect.centery

# Botón Créditos
button_credits = pg.Surface((165, 55))
button_credits.fill(GREEN)
button_credits_rect = button_credits.get_rect()
button_credits_rect.midleft = (350, button_instructions_rect.centery)

text_credits = font_button.render("Créditos", True, BLACK)
text_credits_rect = text_credits.get_rect()
text_credits_rect.centerx = button_credits_rect.centerx
text_credits_rect.centery = button_credits_rect.centery

BG = pg.image.load("FondoPausa.png")


def get_font(size):
    return pg.font.Font("pixel.ttf", size)


def menu_principal(cell_size, totalBees):

    clock = pg.time.Clock()
    running = True
    while running:
        screen.blit(fondo, [0, 0])
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pg.mouse.get_pos()
                    if button_instructions_rect.collidepoint(mouse_pos):
                        instrucciones()
                    elif button_credits_rect.collidepoint(mouse_pos):
                        creditos()
                    elif button_statistics_rect.collidepoint(mouse_pos):
                        estadisticas()
                    elif button_close_rect.collidepoint(mouse_pos):
                        pg.quit()
                        sys.exit()
                    elif play_button_rect.collidepoint(mouse_pos):
                        mode(cell_size)

        # RENDER YOUR GAME HERE

        screen.blit(game_title, game_title_rect)

        screen.blit(button_close, button_close_rect)
        screen.blit(text_close, text_close_rect)

        screen.blit(play_button, (width/2.5, height/2.6))

        screen.blit(button_statistics, button_statistics_rect)
        screen.blit(text_statistics, text_statistics_rect)

        screen.blit(button_instructions, button_instructions_rect)
        screen.blit(text_instructions, text_instructions_rect)

        screen.blit(button_credits, button_credits_rect)
        screen.blit(text_credits, text_credits_rect)

        # flip() the display to put your work on screen
        pg.display.flip()

        clock.tick(60)  # limits FPS to 60


def creditos():
    creditos_texto = "Créditos:\n\n" \
                     "        FutureForge Ltd. 2023\n\n" \
                     "        Iconos de minas:\n" \
                     "        - freepng.es\n\n" \
                     "        Iconos de banderas:\n" \
                     "        - ziddyengineering.com\n\n" \
                     "        Fuente de letras:\n" \
                     "        - dafont.com \n\n" \
                     "        Diseño de botones:\n" \
                     "        - pixelartmaker.com \n\n" \
                     "        Background Menú Principal:\n" \
                     "        tuexpertoapps.com\n\n" \
                     "        Equipo de desarrollo FutureForge Ltd: \n" \
                     "        - Juan David Romero Pemberthy: Gerente de Proyecto \n" \
                     "        - David Felipe García Porras: Director de Diseño \n" \
                     "        - Julián Alberto Fadul Neira: Director de UI \n" \
                     "        - Gabriel Elias Palencia Cure: Director de Pruebas \n" \
                     "        - Jairo Luis Moreno Gutierrez: Director de Documentación \n\n"

    font_creditos = pg.font.Font("pixel.ttf", 24)
    rect_creditos = pg.Rect(width/3.5, height/6, width, height)

    volver_button = font_button.render("VOLVER", True, BLACK)
    volver_button_rect = volver_button.get_rect()
    volver_button_rect.midbottom = screen.get_rect().midbottom
    volver_button_rect.y -= height/5.5

    while True:
        screen.blit(fondo, [0, 0])
        render_textrect(creditos_texto, font_creditos,
                        rect_creditos, BLACK, None, justification=0)
        screen.blit(volver_button, volver_button_rect)
        pg.draw.line(screen, BLACK, (volver_button_rect.x, volver_button_rect.y + 30),
                     (volver_button_rect.x + width * 0.057, volver_button_rect.y + 30), 3)
        pg.display.flip()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pg.mouse.get_pos()
                    if volver_button_rect.collidepoint(mouse_pos):
                        return


def instrucciones():
    instrucciones_texto = "Intrucciones de juego:\n\n"\
        "    MineVenture te permitirá jugar al clásico juego de buscaminas donde deberás\n"\
        "    usar todo tu ingenio en descubrir las minas en el tablero.\n\n"\
        "    - Mecánicas o controles:\n"\
        "      Para las casillas podrás hacer dos cosas:\n"\
        "        1. Descubrir la casilla: Si das clic izquierdo al mouse sobre una casilla, esta\n"\
        "           se abrirá y descubrirás lo que hay en ella, sean espacios vacíos, números o MINAS.\n\n"\
        "        2. Marcar la casilla: Si das clic derecho al mouse sobre una casilla, esta se \n"\
        "           marcará, o lo que es lo mismo, la identificarás como una casilla donde se encuentra\n"\
        "           una mina y no quieres abrirla por accidente.\n\n"\
        "    -Jugabilidad:\n"\
        "       1. Los números alrededor de casillas representan el número de minas que hay en sus\n"\
        "          8 casillas inmediatamente circundantes.\n"\
        "       2. Mediante lógica y patrones podrás identificar cada vez más rápido las casillas\n"\
        "          peligrosas que contienen MINAS."

    font_instrucciones = pg.font.Font("pixel.ttf", 24)
    rect_instrucciones = pg.Rect(width*0.17, height/5, width, height)

    volver_button = font_button.render("VOLVER", True, BLACK)
    volver_button_rect = volver_button.get_rect()
    volver_button_rect.midbottom = screen.get_rect().midbottom
    volver_button_rect.y -= height/5.5

    while True:
        screen.blit(fondo, [0, 0])
        render_textrect(instrucciones_texto, font_instrucciones,
                        rect_instrucciones, BLACK, None, justification=0)
        screen.blit(volver_button, volver_button_rect)
        pg.draw.line(screen, BLACK, (volver_button_rect.x, volver_button_rect.y + 30),
                     (volver_button_rect.x + width * 0.057, volver_button_rect.y + 30), 3)

        pg.display.flip()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pg.mouse.get_pos()
                    if volver_button_rect.collidepoint(mouse_pos):
                        return


def estadisticas():
    estadisticas_texto = ""
    try:
        with open('Registros.txt', 'r') as file:
            # Leer cada línea del archivo hasta que no haya más
            linea = file.readline()
            while linea:
                # Procesar la línea como un registro
                registro = linea.strip().split(',')
                # Hacer algo con el registro
                estadisticas_texto += ', '.join(registro) + ' segundos' '\n'

                # Leer la siguiente línea
                linea = file.readline()

    except FileNotFoundError:
        estadisticas_texto = "Actualmente no hay registros de partidas anteriores"

    font_estadisticas = pg.font.Font("pixel.ttf", 24)
    rect_estadisticas = pg.Rect(width*0.25, height * 0.25, width, height)

    volver_button = font_button.render("VOLVER", True, BLACK)
    volver_button_rect = volver_button.get_rect()
    volver_button_rect.midbottom = screen.get_rect().midbottom
    volver_button_rect.y -= height/5.5

    while True:
        screen.blit(fondo, [0, 0])
        render_textrect(estadisticas_texto, font_estadisticas,
                        rect_estadisticas, BLACK, None, justification=0)
        screen.blit(volver_button, volver_button_rect)
        pg.draw.line(screen, BLACK, (volver_button_rect.x, volver_button_rect.y + 30),
                     (volver_button_rect.x + width * 0.057, volver_button_rect.y + 30), 3)

        pg.display.flip()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pg.mouse.get_pos()
                    if volver_button_rect.collidepoint(mouse_pos):
                        return


def render_textrect(text, font, rect, text_color, background_color, justification=0):
    lines = text.splitlines()
    line_surfaces = []
    max_width = rect.width

    for line in lines:
        line_surf = font.render(line, True, text_color, background_color)
        line_rect = line_surf.get_rect()
        line_surfaces.append((line_surf, line_rect))

        if line_rect.width > max_width:
            max_width = line_rect.width

    accumulated_height = 0
    for line_surf, line_rect in line_surfaces:
        if justification == 0:
            line_rect.topleft = (rect.x, rect.y + accumulated_height)
        elif justification == 1:
            line_rect.midtop = (rect.centerx, rect.y + accumulated_height)
        elif justification == 2:
            line_rect.topright = (rect.right, rect.y + accumulated_height)
        screen.blit(line_surf, line_rect)
        accumulated_height += line_rect.height


def resumen(tiempo_completado, aux, cell_size, totalBees):
    # Crear los rectángulos para los elementos
    rect_felicidades = pg.Rect(100, 200, width - 200, 100)
    rect_tiempo = pg.Rect(100, rect_felicidades.bottom + 80, width - 200, 50)
    rect_nombre = pg.Rect(100, rect_tiempo.bottom + 80, width - 200, 50)
    rect_volver = pg.Rect(100, rect_nombre.bottom + 80, width*0.25, 50)
    rect_volver.centerx = width // 2

    # Variables para almacenar el nombre del jugador y el mensaje de felicitaciones
    nombre_jugador = ""
    nombre_ingresado = False
    
    if aux == 1:
        mensaje_felicidades = "Sigue Intentando..."
    else:
        mensaje_felicidades = "¡FELICIDADES!"

    while True:
        screen.blit(fondo, [0, 0])

        # Renderizar los rectángulos
        pg.draw.rect(screen, BLUE, rect_volver)

        # Renderizar el texto en los rectángulos
        texto_felicidades = font_button.render(
            mensaje_felicidades, True, BLACK)
        texto_tiempo = font_button.render(
            "Tiempo: " + str(tiempo_completado) + " segundos", True, BLACK)
        texto_nombre = font_button.render(
            "Nombre: " + nombre_jugador, True, BLACK)
        texto_volver = font_button.render(
            "Volver al Menú Principal", True, BLACK)

        screen.blit(texto_felicidades, texto_felicidades.get_rect(
            center=rect_felicidades.center))
        screen.blit(texto_tiempo, texto_tiempo.get_rect(
            center=rect_tiempo.center))
        if aux != 1:
            screen.blit(texto_nombre, texto_nombre.get_rect(
            center=rect_nombre.center))
        screen.blit(texto_volver, texto_volver.get_rect(
            center=rect_volver.center))

        pg.display.flip()

        # Obtener la posición del mouse y los eventos
        mouse_pos = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if rect_volver.collidepoint(mouse_pos):
                    if aux == 2:
                        guardar_registro(
                            nombre_jugador, int(tiempo_completado))
                    # Lógica para volver al menú principal
                    menu_principal(cell_size, totalBees)

            elif event.type == pg.KEYDOWN:
                if not nombre_ingresado:
                    if event.key == pg.K_BACKSPACE:
                        nombre_jugador = nombre_jugador[:-1]
                    elif event.key == pg.K_RETURN:
                        nombre_ingresado = True
                    else:
                        nombre_jugador += event.unicode

start_time = 0
elapsed_time = 0
paused = False
sw = 0
x = 550
y = 380
width_rect = 800
height_rect = 500
border_width = 10

def guardar_registro(nombre, puntuacion):
    # Crear el registro con el formato "nombre,puntuacion"
    registro = f"{nombre},{puntuacion}"

    try:
        # Abrir el archivo en modo lectura
        with open('Registros.txt', 'r') as file:
            # Leer los registros existentes
            registros = file.readlines()

        # Agregar el nuevo registro a la lista
        registros.append(registro + '\n')

        # Ordenar los registros de mayor a menor
        registros.sort(key=lambda x: int(x.split(',')[1]), reverse=False)

        # Tomar solo los primeros 5 registros si hay más de 5
        registros = registros[:5]

        # Abrir el archivo en modo escritura
        with open('Registros.txt', 'w') as file:
            # Escribir los registros ordenados en el archivo
            file.writelines(registros)

        print("Registro guardado correctamente.")
    except FileNotFoundError:
        with open('Registros.txt', 'w') as file:
            # Escribir el nuevo registro en el archivo vacío
            file.write(registro + '\n')
        print("Archivo creado y registro guardado correctamente.")


def mode(cell_size):
    while True:
        screen1.blit(BG, (0, 0))

        MENU_MOUSE_POS = pg.mouse.get_pos()

        PAUSE_TEXT = get_font(75).render(
            "Selecciona el modo de juego", True, "#000000")
        PAUSE_RECT = PAUSE_TEXT.get_rect(center=(960, 300))

        EASY_BUTTON = Button(image=pg.image.load("ResumeButton.png"), pos=(750, 550),
                             text_input="AVENTURERO", font=get_font(53), base_color="#d7fcd4", hovering_color="White")
        HARD_BUTTON = Button(image=pg.image.load("ResumeButton.png"), pos=(1140, 550),
                             text_input="DESAFIO", font=get_font(55), base_color="#d7fcd4", hovering_color="White")
        screen1.blit(PAUSE_TEXT, PAUSE_RECT)

        for button in [EASY_BUTTON, HARD_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen1)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if EASY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    totalBees = 100
                    setup(cell_size, totalBees)
                    game(0, 0, 0, 0, cell_size, totalBees)
                elif HARD_BUTTON.checkForInput(MENU_MOUSE_POS):
                    totalBees = 150
                    setup(cell_size, totalBees)
                    game(0, 0, 0, 0, cell_size, totalBees)

        pg.display.flip()


def pausa(sw, paused, start_time, elapsed_time, cell_size, totalBees):
    paused_elapsed_time = elapsed_time
    while True:
        screen1.blit(BG, (0, 0))

        MENU_MOUSE_POS = pg.mouse.get_pos()

        PAUSE_TEXT = get_font(120).render("PAUSA", True, "#000000")
        PAUSE_RECT = PAUSE_TEXT.get_rect(center=(960, 300))

        RESUME_BUTTON = Button(image=pg.image.load("ResumeButton.png"), pos=(750, 500),
                               text_input="REANUDAR", font=get_font(55), base_color="#d7fcd4", hovering_color="White")
        REINICIAR_BUTTON = Button(image=pg.image.load("ResumeButton.png"), pos=(1140, 500),
                                  text_input="REINICIAR", font=get_font(55), base_color="#d7fcd4", hovering_color="White")
        MENU_BUTTON = Button(image=pg.image.load("ResumeButton.png"), pos=(750, 650),
                             text_input="MENÚ", font=get_font(55), base_color="#d7fcd4", hovering_color="White")
        COMOJUGAR_BUTTON = Button(image=pg.image.load("ResumeButton.png"), pos=(1140, 650),
                                  text_input="COMO JUGAR", font=get_font(54), base_color="#d7fcd4", hovering_color="White")
        screen1.blit(PAUSE_TEXT, PAUSE_RECT)

        for button in [RESUME_BUTTON, REINICIAR_BUTTON, MENU_BUTTON, COMOJUGAR_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen1)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if RESUME_BUTTON.checkForInput(MENU_MOUSE_POS):
                    paused = not paused
                    if not paused:
                        start_time = time.time() - paused_elapsed_time
                    game(sw, paused, start_time,
                         elapsed_time, cell_size, totalBees)
                if REINICIAR_BUTTON.checkForInput(MENU_MOUSE_POS):
                    sw = 0
                    elapsed_time = 0
                    setup(cell_size, totalBees)
                if MENU_BUTTON.checkForInput(MENU_MOUSE_POS):
                    menu_principal(cell_size, totalBees)
                if COMOJUGAR_BUTTON.checkForInput(MENU_MOUSE_POS):
                    instrucciones()

        pg.display.flip()


def game(sw, paused, start_time, elapsed_time, cell_size, totalBees):
    while True:

        screen1.fill(PURPLE1)

        MENU_MOUSE_POS = pg.mouse.get_pos()

        pg.draw.rect(screen1, "Black",
                     (x, y,  width_rect, height_rect), border_width)
        PAUSE_BUTTON = Button(image=pg.image.load("PauseButton.png"), pos=(1515, 250),
                              text_input="", font=get_font(55), base_color="#000000", hovering_color="White")
        Bandera = Button(image=imagen_redimensionada, pos=(650, 320),
                         text_input="", font=get_font(15), base_color="#d7fcd4", hovering_color="White")
        Time = Button(image=None, pos=(1230, 320),
                      text_input=f"{elapsed_time}", font=get_font(35), base_color="#000000", hovering_color="White")
        Puntos = Button(image=None, pos=(940, 320),
                        text_input="TIEMPO", font=get_font(35), base_color="#000000", hovering_color="White")

        for button in [PAUSE_BUTTON, Bandera, Time, Puntos]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen1)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if sw == 0:
                    start_time = time.time()
                    sw = 1
                mousePressed(elapsed_time, cell_size, totalBees)
                if PAUSE_BUTTON.checkForInput(MENU_MOUSE_POS):
                    paused = not paused
                    pausa(sw, paused, start_time,
                          elapsed_time, cell_size, totalBees)

        if not paused:
            if sw == 1:
                elapsed_time = math.floor(time.time() - start_time)

        draw()

        pg.display.flip()


menu_principal(cell_size, 0)
