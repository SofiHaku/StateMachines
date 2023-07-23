class Globals():
    def __init__(self):
        # Ширина и высота игровой части
        self.W = 800
        self.H = 600
        # Ширина вместе с меню
        self.W_and_M = 1000

        # Размер клетки
        self.size = 10
        # Количество кадров, которые показываются на одну позу жизни
        self.card = 8

        # Флаги управления контролем игрок
        self.start = False
        self.down_figurs = False

        # Цвета игры
        self.COLOR_LI = (162, 181, 205)
        self.COLOR_IC = (198, 226, 255)
        self.COLOR_BC = (108, 123, 139)

        self.mas = [[0] * (self.H // self.size + 2) for i in
                    range(self.W // self.size + 2)]
        self.mas_new = [[0] * (self.H // self.size + 2) for i in
                        range(self.W // self.size + 2)]