class Point:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x:.3f},{self.y:.3f})"

    @classmethod
    def from_point(cls, p):
        return cls(p.x, p.y)
