class Globals():
    def __init__(self):
        self.W = 800
        self.H = 600
        self.W_and_M = 1000
        self.size = 5
        self.card = 8
        self.start = False
        self.gl = False

        self.mas = [[0] * (self.H // self.size + 2) for i in
                    range(self.W // self.size + 2)]
        self.mas_new = [[0] * (self.H // self.size + 2) for i in
                        range(self.W // self.size + 2)]