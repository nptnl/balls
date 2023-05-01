# main.py
from frame import frame
from objects import Ball
from vec import vec
import random

def pastel_colors():
    r = random.uniform(0.5, 1.0)
    g = random.uniform(0.5, 1.0)
    b = random.uniform(0.5, 1.0)
    return int(r * 255), int(g * 255), int(b * 255)


setframe = frame(
    [
        Ball(vec(100, 100), vec(0.2, 0), 20, 20, pastel_colors()),
        Ball(vec(500, 400), vec(-0.2, 0), 20, 20, pastel_colors()),
        Ball(vec(200, 500), vec(0.3, 0), 20, 20, pastel_colors()),
        Ball(vec(1100, 200), vec(0, 0.1), 20, 20, pastel_colors()),
        Ball(vec(900, 200), vec(0, -0.1), 20, 20, pastel_colors()),
    ],
    0
)

setframe.display()