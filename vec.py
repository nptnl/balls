# vec.py
def cos(x):
    running = 1.0
    total = 0.0
    for term in range(1,8):
        total += running
        running *= -x*x  / (2*term) / (2*term-1)
    return total

def sin(x):
    running = x
    total = 0.0
    for term in range(1,8):
        total += running
        running *= -x*x / (2*term) / (2*term+1)
    return total

def sqrt(x):
    t1, t2 = 2.0, 1.0
    while abs(t2 - t1) > 0.0001:
        t1 = t2
        t2 -= 0.5*(t2*t2 - x) / t2
    return t2

class vec:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __repr__(self):
        return f"({self.x}, {self.y})"
    def __neg__(self):
        return vec(-self.x, -self.y)
    def __add__(s1, s2):
        return vec(s1.x + s2.x, s1.y + s2.y)
    def __sub__(s1, s2):
        return vec(s1.x - s2.x, s1.y - s2.y)
    def mag_square(self):
        return self.x*self.x + self.y*self.y
    def mag(self):
        return sqrt(self.x*self.x + self.y*self.y)