import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))


W = 800
H = 600
size = 25

mas = [[0] * (H//size + 2) for i in range(W//size + 2)]
mas_new = [[0] * (H//size + 2) for i in range(W//size + 2)]

    # число кадров в секунду
clock = pygame.time.Clock()

def lines():
    """Отрисовка клеток"""
    for coord_x in range(W//size):
         pygame.draw.line(screen, (128, 128, 128), (coord_x * size, 0), (coord_x * size, H))
    for coord_y in range(H//size):
         pygame.draw.line(screen, (128, 128, 128), (0, coord_y * size), (W, coord_y * size))

def draw_rect():
    """Отрисовка прямоугольников"""
    for i in range(len(mas)):
        for j in range(len(mas[0])):
            if mas[i][j] != 0:
                pygame.draw.rect(screen, (255, 255, 255), (i*size, j*size, size, size))
                #print(f"i = {i}, j = {j}, x = {i*size}, y = {j*size}")


def is_alive(index_i, index_j):
    """Определяет будет ли жить клетка на следующем этапе"""
    count = 0

    min_i = -1
    max_i = 2
    min_j = -1
    max_j = 2

    if index_i == 0:
        min_i = 0
    elif index_i == len(mas) - 1:
        max_i = 1

    if index_j == 0:
        min_j = 0
    elif index_j == len(mas[0]) - 1:
        max_j = 1

    for i in range(min_i, max_i):
        for j in range(min_j, max_j):
            if mas[index_i + i][index_j + j] == 1:
                count += 1

    if index_i == 2 and index_j == 1:
        print(f"min_i = {min_i } max_i = {max_i} min_j = {min_j } max_j = {max_j} count = {count}")

    if (count == 3 and mas[index_i][index_j] == 0) or ((count == 4 or count == 3) and mas[index_i][index_j] == 1):
        return 1
    return 0

def all_alive():
    for i in range(len(mas)):
        for j in range(len(mas[0])):
            mas_new[i][j] = is_alive(i, j)

def copy():
    for i in range(len(mas)):
        for j in range(len(mas[0])):
            mas[i][j] = mas_new[i][j]

def illumation(coord_x, coord_y):
    pygame.draw.rect(screen, (238, 232, 170), (coord_x - coord_x % 25, coord_y - coord_y % 25, size, size))

def new_pos(coord_x, coord_y):
    mas[coord_x//size][coord_y//size] = 1

start = False

while True:
    screen.fill((0, 0, 0))
    draw_rect()
    lines()

    pos = pygame.mouse.get_pos()
    illumation(pos[0], pos[1])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not start:
                    start = True
                else:
                    start = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            new_pos(pos[0], pos[1])


    if start:
        all_alive()
        copy()
        clock.tick(5)
    else:
        clock.tick(60)

    pygame.display.flip()
