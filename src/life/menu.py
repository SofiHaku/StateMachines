import pygame
from src.life.figurs import Figurs

class Menu():
    def __init__(self, globals):
        self.globals = globals

        # регулятор скорости
        self.coord_reg_x = 900
        self.coord_reg_y = 150
        self.reg_make = False
        self.dif = 0
        self.gl = Figurs()

        # Глайдер
        self.coord_x = 825
        self.coord_y = 400
        self.gla_t = False

        # Добавление иконок
        image = pygame.image.load("assets/start.png")
        clear_img = pygame.image.load("assets/clear.png")
        next_img = pygame.image.load("assets/next.png")

        self.image = pygame.transform.scale(image, (30, 30))
        self.clear_img = pygame.transform.scale(clear_img, (30, 30))
        self.next_img = pygame.transform.scale(next_img, (30, 30))

    def draw_all(self, screen):
        """Отображение объектов меню на экран"""
        self.draw_reg_speed(screen)
        self.gl.draw_in_mass(self.coord_x, self.coord_y, screen, self.globals, 1)
        pygame.draw.circle(screen, self.globals.COLOR_IC, (900, 75), 20)
        pygame.draw.circle(screen, self.globals.COLOR_IC, (900, 250), 20)
        pygame.draw.circle(screen, self.globals.COLOR_IC, (900, 300), 20)
        screen.blit(self.image, (885, 60))
        screen.blit(self.clear_img, (883, 235))
        screen.blit(self.next_img, (885, 285))

    def control(self, pos, clock, globals):
        """Обработка игровых событий"""
        clear = False # Параметр очистки экрана

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            # Обработка начала работы алгоритма
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.control_glider(pos, 20, 900, 75):
                if globals.start:
                    globals.start = False
                else:
                    globals.start = True

            # Обработка изменения скорости воспроизведения
            elif self.control_reg_speed(pos) and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.reg_make = True
            elif event.type == pygame.MOUSEMOTION and self.reg_make and pos[0] < 975 and pos[0] > 825:
                self.coord_reg_x = pos[0]
                globals.card += event.rel[0] * (-0.1)
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.reg_make:
                self.reg_make = False
                globals.card = max(1, round(globals.card))

            # Обработка фигур
            elif event.type == pygame.MOUSEBUTTONDOWN and self.control_glider(pos, 75, 940, 475):
                self.gla_t = True
                self.globals.down_figurs = True

            # Обработка переключения страниц
            elif event.type == pygame.MOUSEBUTTONDOWN and self.control_page(pos):
                self.gl.page += 1
                self.gl.page %= len(self.gl.mass)

            # Обработка удаления всего с полотна
            elif event.type == pygame.MOUSEBUTTONDOWN and self.control_clear(pos):
                clear = True

        clock.tick(60)
        return [self.gla_t, clear]

    # Блок функций регулироки скоростей и чистки экрана
    def draw_reg_speed(self, screen):
        """Отображение регулировки скорости"""
        pygame.draw.line(screen, self.globals.COLOR_IC, (825, self.coord_reg_y), (975, self.coord_reg_y), 5)
        pygame.draw.circle(screen,self.globals.COLOR_LI, (self.coord_reg_x, self.coord_reg_y), 8)

    def control_reg_speed(self, pos):
        """Проверка находится ли курсор в круге регулировки"""
        if pos[0] < self.coord_reg_x + 10 and pos[0] > self.coord_reg_x - 10:
            if pos[1] < self.coord_reg_y + 10 and pos[1] > self.coord_reg_y - 10:
                return True
        return False

    def control_page(self, pos):
        """Проверка находится ли курсор в круге регулировки"""
        if pos[0] < 900 + 20 and pos[0] > 900 - 20:
            if pos[1] < 300 + 20 and pos[1] > 300 - 20:
                return True
        return False

    def control_clear(self, pos):
        """Проверка находится ли курсор в круге регулировки"""
        if pos[0] < 900 + 20 and pos[0] > 900 - 20:
            if pos[1] < 250 + 20 and pos[1] > 250 - 20:
                return True
        return False

    # Блок фигур
    def control_glider(self, pos, size, x, y):
        """Проверка находится ли курсор в области взятия новой фигуры"""
        if pos[0] < x + size and pos[0] > x - size:
            if pos[1] < y + size and pos[1] > y - size:
                return True
        return False

    def control_figurs(self, pos, screen):
        """Контроль переноса фигуры, которую пользователь хочет поставить на экран"""
        self.gl.draw_in_mass(pos[0], pos[1], screen, self.globals, 0)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.globals.down_figurs = False
                return self.gl.new(pos[0], pos[1], self.globals.mas, self.globals)
