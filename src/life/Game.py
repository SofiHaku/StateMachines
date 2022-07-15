import pygame
from src.life.globals import Globals
from src.life.menu import Menu

class Game():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Жизнь")

        self.globals = Globals()
        self.clock = pygame.time.Clock()
        self.menu = Menu(self.globals)
        self.screen = pygame.display.set_mode((self.globals.W_and_M, self.globals.H))

        # Массивы с данными о клетках
        self.list_life = [[0] * (self.globals.H // self.globals.size + 2) for i in range(self.globals.W // self.globals.size + 2)]
        self.list_life_new = [[0] * (self.globals.H // self.globals.size + 2) for i in range(self.globals.W // self.globals.size + 2)]

        self.count_card = 0 # Счетчик кадров
        self.make_new_cell = False # Флаг, чтобы проверить создание новых живых клеток пользователем
        self.cl_flag = False # Флаг, чтобы проверить очистку экрана

    def lines(self):
        """Отрисовка клеток"""
        for coord_x in range(self.globals.W // self.globals.size + 1):
            pygame.draw.line(self.screen,self.globals.COLOR_LI, (coord_x * self.globals.size, 0),
                             (coord_x * self.globals.size, self.globals.H))
        for coord_y in range(self.globals.H // self.globals.size + 1):
            pygame.draw.line(self.screen, self.globals.COLOR_LI, (0, coord_y * self.globals.size),
                             (self.globals.W, coord_y * self.globals.size))

    def draw_rect(self):
        """Отрисовка прямоугольников"""
        for i in range(len(self.list_life)):
            for j in range(len(self.list_life[0])):
                if self.list_life[i][j] != 0:
                    if (i * self.globals.size < self.globals.W):
                        pygame.draw.rect(self.screen, (255, 255, 255),
                                         (i * self.globals.size, j * self.globals.size, self.globals.size,
                                          self.globals.size))

    def is_alive(self, index_i, index_j):
        """Определяет будет ли жить клетка на следующем этапе"""
        # счетчик живых клеток рядом
        count = 0

        # диапазон, чтобы не вылезти за границы массива
        min_i, max_i = -1, 2
        min_j, max_j = -1, 2

        if index_i == 0:
            min_i = 0
        elif index_i == len(self.list_life) - 1:
            max_i = 1

        if index_j == 0:
            min_j = 0
        elif index_j == len(self.list_life[0]) - 1:
            max_j = 1

        for i in range(min_i, max_i):
            for j in range(min_j, max_j):
                if self.list_life[index_i + i][index_j + j] == 1:
                    count += 1

        if (count == 3 and self.list_life[index_i][index_j] == 0) or ((count == 4 or count == 3) and self.list_life[index_i][index_j] == 1):
            return 1
        return 0

    def all_alive(self):
        """Проверяет все клетки на то, останутся ли они живы на следующем шаге"""
        for i in range(len(self.list_life)):
            for j in range(len(self.list_life[0])):
                self.list_life_new[i][j] = self.is_alive(i, j)

    def copy(self):
        """Копирование массива c учетом частоты кадров для жизни"""
        if self.count_card >= self.globals.card:
            for i in range(len(self.list_life)):
                for j in range(len(self.list_life[0])):
                    self.list_life[i][j] = self.list_life_new[i][j]
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
            self.list_life[coord_x // self.globals.size][coord_y // self.globals.size] = 1

    def delete_pos(self, coord_x, coord_y, index_i, index_j):
        """Убийство клеток"""
        if coord_x == -1:
            self.list_life[index_i][index_j] = 0
        else:
            if (coord_x < self.globals.W):
                self.list_life[coord_x // self.globals.size][coord_y // self.globals.size] = 0

    def clear(self):
        """Очистка всего экрана от живых клеток"""
        for i in range(len(self.list_life)):
            for j in range(len(self.list_life[0])):
                self.delete_pos(-1, -1, i, j)


    def cont_in_game(self, pos):
        """Обработка игровых событий"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Для длительного нажатия
                self.make_new_cell = True
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.make_new_cell:
                self.make_new_cell = False

        if self.make_new_cell:
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
            self.screen.fill(self.globals.COLOR_BC)
            self.menu.draw_all(self.screen)
            self.draw(pos)

            # Проверяем взята ли какая-нибудь фигура
            if self.globals.down_figurs:
                res = self.menu.control_figurs(pos, self.screen)
                if res:
                    for i in range(len(res)):
                        self.new_pos(res[i][0], res[i][1])
            # Проверяем проводится ли очистка экрана
            elif self.cl_flag:
                self.clear()
                self.cl_flag = False
            # Проверяем в меню игрок или на главном экране
            elif pos[0] < self.globals.W:
                self.cont_in_game(pos)
            else:
                ret = self.menu.control(pos, self.clock, self.globals)
                self.gl = ret[0]
                self.cl_flag = ret[1]

            # Перехом на следующий этап жизни
            if self.globals.start:
                self.all_alive()
                self.copy()

            pygame.display.update()