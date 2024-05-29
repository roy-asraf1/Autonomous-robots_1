
class Painter:
    def __init__(self, algo):
        self.algo = algo

    def paint_component(self, g):
        self.algo.paint(g)
