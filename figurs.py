import pygame

class Glider():
    def __init__(self):
        self.mass = [[0, 1, 0], [0, 0, 1], [1, 1 , 1]]
        self.size = 75

    def draw_in_mass(self, x, y, screen, globals):
        for i in range(len(self.mass)):
            for j in range(len(self.mass[0])):
                if self.mass[i][j]:
                    pygame.draw.rect(screen, (255, 255, 255),
                        (x - x % globals.size + j*globals.size,
                         y - y % globals.size + i*globals.size, globals.size, globals.size))

    def new(self, x, y, mas, globals):
        mass = []
        for i in range(len(self.mass)):
            for j in range(len(self.mass[0])):
                if self.mass[i][j]:
                    if (x < globals.W):
                        mass.append([x + j * globals.size, y + i*globals.size])
        return mass

