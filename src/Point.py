
class Point:
    import decimal

    def __init__(self, x=0.0, y=0.0):
        if isinstance(x, Point):
            self.x = x.x
            self.y = x.y
        else:
            self.x = x
            self.y = y

    def __str__(self):
        return f"({self.x:.3f},{self.y:.3f})"
