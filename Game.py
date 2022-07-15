import pygame
from globals import Globals
from menu import Menu
from figurs import Glider

class Game():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Жизнь")

        self.globals = Globals()
        self.clock = pygame.time.Clock()
        self.menu = Menu(self.globals)

        self.mas = [[0] * (self.globals.H // self.globals.size + 2) for i in range(self.globals.W // self.globals.size + 2)]
        self.mas_new = [[0] * (self.globals.H // self.globals.size + 2) for i in range(self.globals.W // self.globals.size + 2)]
        self.screen = pygame.display.set_mode((self.globals.W_and_M, self.globals.H))
        self.count_card = 0
        self.make = False

    def lines(self):
        """Отрисовка клеток"""
        for coord_x in range(self.globals.W // self.globals.size + 1):
            pygame.draw.line(self.screen, (128, 128, 128), (coord_x * self.globals.size, 0),
                             (coord_x * self.globals.size, self.globals.H))
        for coord_y in range(self.globals.H // self.globals.size + 1):
            pygame.draw.line(self.screen, (128, 128, 128), (0, coord_y * self.globals.size),
                             (self.globals.W, coord_y * self.globals.size))

    def draw_rect(self):
        """Отрисовка прямоугольников"""
        for i in range(len(self.mas)):
            for j in range(len(self.mas[0])):
                if self.mas[i][j] != 0:
                    if (i * self.globals.size < self.globals.W):
                        pygame.draw.rect(self.screen, (255, 255, 255),
                                         (i * self.globals.size, j * self.globals.size, self.globals.size,
                                          self.globals.size))
                    # print(f"i = {i}, j = {j}, x = {i*size}, y = {j*size}")

    def is_alive(self, index_i, index_j):
        """Определяет будет ли жить клетка на следующем этапе"""
        # счетчик живых клеток рядом
        count = 0

        # диапазон, чтобы не вылезти за границы массива
        min_i, max_i = -1, 2
        min_j, max_j = -1, 2

        if index_i == 0:
            min_i = 0
        elif index_i == len(self.mas) - 1:
            max_i = 1

        if index_j == 0:
            min_j = 0
        elif index_j == len(self.mas[0]) - 1:
            max_j = 1

        for i in range(min_i, max_i):
            for j in range(min_j, max_j):
                if self.mas[index_i + i][index_j + j] == 1:
                    count += 1

        if (count == 3 and self.mas[index_i][index_j] == 0) or ((count == 4 or count == 3) and self.mas[index_i][index_j] == 1):
            return 1
        return 0

    def all_alive(self):
        """Проверяет все клетки на то, останутся ли они живы на следующем шаге"""
        for i in range(len(self.mas)):
            for j in range(len(self.mas[0])):
                self.mas_new[i][j] = self.is_alive(i, j)

    def copy(self):
        """Копирование массива c учетом частоты кадров для жизни"""
        if self.count_card >= self.globals.card:
            for i in range(len(self.mas)):
                for j in range(len(self.mas[0])):
                    self.mas[i][j] = self.mas_new[i][j]
            self.count_card = 0
        else:
            self.count_card += 1

    def illumation(self, coord_x, coord_y):
        """Подсветка клетки во время редактирования поля"""
        if (coord_x < self.globals.W):
            pygame.draw.rect(self.screen, (238, 232, 170),
                             (coord_x - coord_x % self.globals.size,
                              coord_y - coord_y % self.globals.size, self.globals.size,
                              self.globals.size))

    def new_pos(self, coord_x, coord_y):
        """Добавление клетки к живим"""
        if (coord_x < self.globals.W):
            self.mas[coord_x // self.globals.size][coord_y // self.globals.size] = 1


    def cont_in_game(self, pos):
        """Обработка игровых событий"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Для длительного нажатия
                self.make = True
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.make:
                self.make = False

        if self.make:
            self.new_pos(pos[0], pos[1])
        self.clock.tick(60)

    def draw(self, pos):
        """Вывод изображения"""
        self.draw_rect()
        self.illumation(pos[0], pos[1])
        self.lines()


    def run(self):
        """Запуск игры"""
        while True:
            pos = pygame.mouse.get_pos()

            # Блок отрисовки событий
            self.screen.fill((0, 0, 0))
            self.menu.draw_all(self.screen)
            self.draw(pos)

            if self.globals.gl:
                res = self.menu.control_figurs(pos, self.screen, self.globals.mas)
                if res:
                    for i in range(len(res)):
                        self.new_pos(res[i][0], res[i][1])
            elif pos[0] < self.globals.W:
                self.cont_in_game(pos)
            else:
                ret = self.menu.control(pos, self.clock, self.globals, self.screen)
                self.gl = ret[0]

            if self.globals.start:
                self.all_alive()
                self.copy()

            pygame.display.flip()